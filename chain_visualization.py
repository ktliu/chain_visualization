# For visualization
import os
# import matplotlib.pyplot as plt
 
import graphviz as gv
 
#########
#
# Weird Bug Warning - to Fix: Sometimes blockhash is printed out ;(
# Example Warning: node J0b"'\x0cS, port \xb3\xdf\xd2\xb8({" unrecognized
# 
#######

class ChainVisualization:
	def __init__(self):
 

		#Subgraphs
		self.legend = None
		self.global_chain = None
		self.main_chain = None
		self.main_chain_context = None # Cry ;_;  

		self.validators = {} # {validator: currentNode} keep track of last node drawn
		self.G = gv.Digraph('G')

		self.blockhash_to_ids = {} # temporary way to rid of warning
		self.current_block_id = 0

		self.init_main_chain()
 
	def init_main_chain(self):
 		# Can't use with block so we need to manually open and close with __enter__ and __exit__
		self.main_chain_context = self.G.subgraph(name='cluster_main_chain')
		self.main_chain = self.main_chain_context.__enter__()
		self.main_chain.attr(color='white')
 

 
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

	def draw_epoch(self, block_number, block_hash): 
		B_token = 'B' + str(block_number)
 
		for key, value in self.validators.items():
			block_id = self.new_block_id(key, block_hash)
			self.main_chain.node(block_id, color='orange', style='filled', label=B_token)
			self.main_chain.edge(block_id, value, style="dashed")
			self.validators[key] = block_id		 

	def draw_prepare(self, validator_index, block_hash):
		#hacky way to change color of block
		J_token = "J" + str(validator_index)
		block_id = self.get_block_id(J_token, block_hash)
		self.main_chain.node(block_id, color='blue', shape="square")
		self.validators[J_token] = block_id

	def draw_commit(self, validator_index, block_hash):
		J_token = "J" + str(validator_index)
		commit_block_id = "C" + self.get_block_id(J_token, block_hash)
		self.main_chain.node(commit_block_id, color='orange', style='filled', label="C")
		self.main_chain.edge(commit_block_id, self.validators[J_token], style="dashed")
		self.validators[J_token] = commit_block_id

	def draw_validator(self, validator_index):
		J_token = "J" + str(validator_index)
		self.main_chain.node(J_token, color='orange', style='filled')
		self.validators[J_token] = J_token
 
	def draw_slash_double_prepare(self, validator_index, block_hash_1, block_hash_2):
		J_token = "J" + str(validator_index)
		block_id_1 = self.get_block_id(J_token, block_hash_1)
		block_id_2 = self.get_block_id(J_token, block_hash_2)
		slash_id = "DP" + block_id_1 + block_id_2
		self.main_chain.node(slash_id, color='red', style='filled', shape="diamond", label="DP")
		self.main_chain.edge(slash_id, block_id_1, style="dashed" )
		self.main_chain.edge(slash_id, block_id_2, style="dashed" )

	def draw_slash_commit_inconsistency(self, validator_index, prepare_block_hash, commit_block_hash):
		J_token = "J" + str(validator_index)	
		prepare_id = self.get_block_id(J_token, prepare_block_hash)
		commit_id = "C" + self.get_block_id(J_token, commit_block_hash)
		slash_id = "PCC" + prepare_id + commit_id
		self.main_chain.node(slash_id, color='red', style='filled', shape="diamond", label="PCC")
		self.main_chain.edge(slash_id, prepare_id, style="dashed" )
		self.main_chain.edge(slash_id, commit_id, style="dashed" )
 
	def draw_save_block(self, block_hash):
 		for key, value in self.validators.items():
 			block_id = self.get_block_id(key, block_hash)
 			self.main_chain.node(block_id, color='purple')

	def draw_revert_block(self, block_hash):
 		for key in self.validators:
 			self.validators[key] = self.get_block_id(key, block_hash)
	
	def slash_validator(self, validator_index):
		J_token = "J" + str(validator_index)
		self.validators.pop(J_token) #Do not continue building on chain if slashed

	# For visualization
	def saveToDotGraph(self, filename):
	    """
	    Save a graph to a PNG file.
	    graph: G
	    str: filename
	    """
	    self.main_chain_context.__exit__(None, None, None)
	    self.draw_legend()
	    self.G.render(filename=filename)
 
 	 