# For visualization
import os
# import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import graphviz

#########
#
# Weird Bug - to Fix: block_hash is too long and prints out weirdly  
# 					  so slicing block_hash[:10] for now ;(
# 
#######

class ChainVisualization:
	def __init__(self):
		# initialize graph
		self.G = nx.DiGraph()
		self.validators = {} # {validator: currentNode} keep track of last node drawn
 		
		#legend
		self.draw_legend()

	def draw_legend(self):
		H = self.G.subgraph([0,1,2]) 

	def draw_epoch(self, block_number, block_hash): 
		B_token = 'B' + str(block_number)
	 
		print(self.validators)
		for key, value in self.validators.items():
			block_id = key + str(block_hash[:10]) # without slicing block_hash too long prints out weirdly
		  
			self.G.add_node(block_id, color='orange', style='filled', label=B_token)
			self.G.add_edge(block_id, value, style="dashed")
			print(value)
			self.validators[key] = block_id
			 

	def draw_prepare(self, validator_index, block_hash):
		#hacky way to change color of block
		J_token = "J" + str(validator_index)
		block_id = J_token + str(block_hash[:10])
		self.G.add_node(block_id, color='blue', shape="square")
		self.validators[J_token] = block_id

	def draw_commit(self, validator_index, block_hash):
		J_token = "J" + str(validator_index)
		commit_block_id = J_token + "C" + str(block_hash[:10]) #probably need a better unique identifier
		self.G.add_node(commit_block_id, color='orange', style='filled', label="C")
		self.G.add_edge(commit_block_id, self.validators[J_token], style="dashed")
		self.validators[J_token] = commit_block_id

	def draw_validator(self, validator_index):
		J_token = "J" + str(validator_index)
 
		self.G.add_node(J_token, color='orange', style='filled')
		self.validators[J_token] = J_token
 
	def draw_slash_double_prepare(self, validator_index, block_hash_1, block_hash_2):
		J_token = "J" + str(validator_index)	
		slash_id = str(block_hash_1[:10]) + str(block_hash_2[:10])
		self.G.add_node(slash_id, color='red', style='filled', shape="diamond", label="DP")
		self.G.add_edge(slash_id, J_token + str(block_hash_1[:10]), style="dashed" )
		self.G.add_edge(slash_id, J_token + str(block_hash_2[:10]), style="dashed" )

	def draw_slash_commit_inconsistency(self, validator_index, prepare_block_hash, commit_block_hash):
		J_token = "J" + str(validator_index)	
		slash_id = J_token + "PCI" + str(prepare_block_hash[:10]) # PCI stands for prepare commit inconsistency ;(
		self.G.add_node(slash_id, color='red', style='filled', shape="diamond", label="PCI")
		self.G.add_edge(slash_id, J_token + str(prepare_block_hash[:10]), style="dashed" )
		self.G.add_edge(slash_id, J_token + "C" +  str(commit_block_hash[:10]), style="dashed" )
 
 
	      
	# For visualization
	def saveToDotGraph(self, filename):
	    """
	    Save a graph to a PNG file.
	    graph: G
	    str: filename
	    """

	    dotname = filename + '.dot'
	    write_dot(self.G, dotname)
 
	    pngname = filename + '.png'

	    cmd = 'dot -n -Tpng {} > {}'.format(dotname, pngname)
	    os.system(cmd)

 