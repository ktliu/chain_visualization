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
		# initialize graph
		print("WTsssF")

		self.legend = None
		self.global_chain = None
		self.main_chain = None
		self.main_chain_context = None # Cry ;_; 
		self.validators = {} # {validator: currentNode} keep track of last node drawn
		self.G = gv.Digraph('G')
 

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

			legend_msg = "- Square: Prepare \n \- Circle: Prepare & Commit \n \- Diamond: Slashed"
			self.legend.node('legend', label=legend_msg, color='white', nojustify='false')
			# prepare_msg = "P = Prepare"
			# self.legend.node('P', color='blue', style='filled', shape='square')
			# self.legend.edge('P', 'p_edge', color='white', label=prepare_msg)

			# prepare_commit_msg = "C = Prepare and Commit"
			# self.legend.node('C', color='orange', style='filled')
			# self.legend.edge('C', 'c_edge', color="white", label=prepare_commit_msg)

			# block_msg = "B = epoch \n Bn where n represents \n the number of blocks \n(don't know what I'm doing)"
			# self.legend.node('B', color='orange', style='filled')
			# self.legend.edge('B', 'b_edge', color='white', label=block_msg)
			
			# slash_msg = "DP = Double Prepare \n PCC = Prepare Commit Consistency"
			# self.legend.node('DP / PCC', color='red', style='filled', shape='diamond')
			# self.legend.edge('DP / PCC', 'slash_edge', color='white', label=slash_msg)

	def draw_epoch(self, block_number, block_hash): 
		B_token = 'B' + str(block_number)
	 
		print(self.validators)
		for key, value in self.validators.items():
			block_id = key + str(block_hash[:10]) # without slicing block_hash too long prints out weirdly
		  
			self.main_chain.node(block_id, color='orange', style='filled', label=B_token)
			self.main_chain.edge(block_id, value, style="dashed")
			print(value)
			self.validators[key] = block_id
			 

	def draw_prepare(self, validator_index, block_hash):
		#hacky way to change color of block
		J_token = "J" + str(validator_index)
		block_id = J_token + str(block_hash[:10])
		self.main_chain.node(block_id, color='blue', shape="square")
		self.validators[J_token] = block_id

	def draw_commit(self, validator_index, block_hash):
		J_token = "J" + str(validator_index)
		commit_block_id = J_token + "C" + str(block_hash[:10]) #probably need a better unique identifier
		self.main_chain.node(commit_block_id, color='orange', style='filled', label="C")
		self.main_chain.edge(commit_block_id, self.validators[J_token], style="dashed")
		self.validators[J_token] = commit_block_id

	def draw_validator(self, validator_index):
		J_token = "J" + str(validator_index)
 
		self.main_chain.node(J_token, color='orange', style='filled')
		self.validators[J_token] = J_token
 
	def draw_slash_double_prepare(self, validator_index, block_hash_1, block_hash_2):
		J_token = "J" + str(validator_index)	
		slash_id = str(block_hash_1[:10]) + str(block_hash_2[:10])
		self.main_chain.node(slash_id, color='red', style='filled', shape="diamond", label="DP")
		self.main_chain.edge(slash_id, J_token + str(block_hash_1[:10]), style="dashed" )
		self.main_chain.edge(slash_id, J_token + str(block_hash_2[:10]), style="dashed" )

	def draw_slash_commit_inconsistency(self, validator_index, prepare_block_hash, commit_block_hash):
		J_token = "J" + str(validator_index)	
		slash_id = J_token + "PCC" + str(prepare_block_hash[:10]) # PCC stands for prepare commit consistency ;(
		self.main_chain.node(slash_id, color='red', style='filled', shape="diamond", label="PCC")
		self.main_chain.edge(slash_id, J_token + str(prepare_block_hash[:10]), style="dashed" )
		self.main_chain.edge(slash_id, J_token + "C" +  str(commit_block_hash[:10]), style="dashed" )
 

	      
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
 
 	 