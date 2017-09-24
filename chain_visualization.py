# For visualization
import os
# import matplotlib.pyplot as plt
 
import graphviz as gv
 
#########
#
# NOTE: Blockhash arguments only work with epochs (B) so the blockhash of the last epoch seen not B1, B10
# 
#######

class ChainVisualization:
	def __init__(self):
 

		# Initiate Subgraphs
		self.legend = self.global_chain = self.main_chain \
		 = self.main_chain_context = self.global_chain_context = None # Cry ;_;  

		self.validators = {} # {validator: currentNode} keep track of last node drawn
		self.last_global_node = '' 
		self.G = gv.Digraph('G')

		self.blockhash_to_ids = {} # temporary way to rid of warning, assign blockhash to unique integer ids
		self.global_blockhash = []

		self.current_block_id = 0 
		self.current_global_id = 0

		self.init_main_chain()
		self.init_global_chain()

 

	def init_main_chain(self):
 		# Can't use with block so we need to manually open and close with __enter__ and __exit__
		self.main_chain_context = self.G.subgraph(name='cluster_main_chain')
		self.main_chain = self.main_chain_context.__enter__()
		self.main_chain.attr(color='white')
  
	def init_global_chain(self):
		self.global_chain_context = self.G.subgraph(name='cluster_global_chain')
		self.global_chain = self.global_chain_context.__enter__()
		self.global_chain.attr(label="Global Blockchain")

	def draw_legend(self):
		with self.G.subgraph(name='cluster_legend') as l:
			self.legend = l
			self.legend.attr(label='Legend')
			self.legend.attr(color='lightgrey')
			legend_msg = "- Square: Prepare \n \- Circle: Prepare & Commit \n \- Diamond: Slashed \n - Purple: Saved Checkpoint"
			self.legend.node('legend', label=legend_msg, color='white', nojustify='false')
			 

	def new_block_id(self, validator_token, block_hash):
		self.blockhash_to_ids[validator_token + str(block_hash)] =  self.current_block_id
		self.current_block_id += 1
		return str(self.blockhash_to_ids[validator_token + str(block_hash)])

	def get_block_id(self, validator_token, block_hash):
		return str(self.blockhash_to_ids[validator_token + str(block_hash)])

	def draw_epoch(self,  block_hash, epoch, is_last_epoch_finalized): 
	 
		ascii_A = 65

		# Draw a new block node on the main chain
		for key, value in self.validators.items():
			block_id = self.new_block_id(key, block_hash)
			B_token = chr(ascii_A + epoch - 1)
			self.main_chain.node(block_id, color='gray', style='filled', label=B_token)
			self.main_chain.edge(block_id, value, style="dashed")
			self.validators[key] = block_id	

		# Draw finalized nodes on the global chain prob better way to do this
		if is_last_epoch_finalized and (epoch - 1 not in self.global_blockhash):	
			G_token = chr(ascii_A + epoch - 1)
			self.global_chain.node("G" + str(self.current_global_id), color='gray', style='filled', label= G_token) #uhh change block_hash		

			if self.last_global_node != '':
				self.global_chain.edge("G" + str(self.current_global_id), "G" + str(self.last_global_node))
			
			self.last_global_node = self.current_global_id
			self.current_global_id += 1
			self.global_blockhash.append(epoch - 1)



	def draw_prepare(self, validator_index, block_hash):
		#hacky way to change color of block
		J_token = "Validator" + str(validator_index)
		block_id = self.get_block_id(J_token, block_hash)
		self.main_chain.node(block_id, color='blue', shape="square")
		self.validators[J_token] = block_id

	def draw_commit(self, validator_index, block_hash):
		J_token = "Validator" + str(validator_index)
		block_id = self.get_block_id(J_token, block_hash)
		self.main_chain.node(block_id, color='orange', shape="circle")
		self.validators[J_token] = block_id

	def draw_validator(self, validator_index):
		J_token = "Validator" + str(validator_index)
		self.main_chain.node(J_token, color='white', style='filled')
		self.validators[J_token] = J_token
 
	def draw_slash_double_prepare(self, validator_index, block_hash_1, block_hash_2):
		# Draw the DP node and add edges to the nodes that violated slashing conditions
		J_token = "Validator" + str(validator_index)
		block_id_1 = self.get_block_id(J_token, block_hash_1)
		block_id_2 = self.get_block_id(J_token, block_hash_2)
		slash_id = "DP" + block_id_1 + block_id_2
		self.main_chain.node(slash_id, color='red', style='filled', shape="diamond", label="DP")
		self.main_chain.edge(slash_id, block_id_1, style="dashed" )
		self.main_chain.edge(slash_id, block_id_2, style="dashed" )

	def draw_slash_commit_inconsistency(self, validator_index, prepare_block_hash, commit_block_hash):
		# Draw a PCC node and add edges
		J_token = "Validator" + str(validator_index)	
		prepare_id = self.get_block_id(J_token, prepare_block_hash)
		commit_id = self.get_block_id(J_token, commit_block_hash)
		slash_id = "PCC" + prepare_id + commit_id
		self.main_chain.node(slash_id, color='red', style='filled', shape="diamond", label="PCC")
		self.main_chain.edge(slash_id, prepare_id, style="dashed" )
		self.main_chain.edge(slash_id, commit_id, style="dashed" )
 
	def draw_save_block(self, block_hash):
		# Change color of block node to indicate this node was saved
 		for key, value in self.validators.items():
 			block_id = self.get_block_id(key, block_hash)
 			self.main_chain.node(block_id, color='purple')

	def draw_revert_block(self, block_hash):
 		for key in self.validators:
 			self.validators[key] = self.get_block_id(key, block_hash)
	
	def slash_validator(self, validator_index):
		J_token = "Validator" + str(validator_index)
		self.validators.pop(J_token) #Do not continue building on chain if slashed

	# Save drawing
	def saveToDotGraph(self, filename):
 
		self.global_chain_context.__exit__(None, None, None)
		self.main_chain_context.__exit__(None, None, None)
		self.draw_legend()
		self.G.render(filename=filename)


 
 	 