# For visualization
import os
# import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import graphviz

class ChainVisualization:
	def __init__(self):
		# initialize graph
		self.G = nx.DiGraph()
		self.validators = {} # {validator: currentNode} keep track of last node drawn

	def draw_epoch(self, block_number, block_hash): 
		B_token = "B" + str(block_number)
		for key, value in self.validators.items():
			block_id = key + str(block_hash)
			self.G.add_node(block_id, color='orange', style='filled', label=B_token)
			self.G.add_edge(block_id, value, style="dashed")
			self.validators[key] = block_id
		 

	def draw_prepare(self, validator_index, block_hash):
		#hacky way to change color of block
		J_token = "J" + str(validator_index)
		block_id = J_token + str(block_hash)
		self.G.add_node(block_id, color='blue', shape="square")
		self.validators[J_token] = block_id

	def draw_commit(self, validator_index, block_hash):
		J_token = "J" + str(validator_index)
		commit_block_id = J_token + "C" + str(block_hash) #probably need a better identifier
		self.G.add_node(commit_block_id, color='orange', style='filled', label="C")
		self.G.add_edge(commit_block_id, self.validators[J_token], style="dashed")
		self.validators[J_token] = commit_block_id

	def draw_validator(self, validator_index):
		J_token = "J" + str(validator_index)
 
		self.G.add_node(J_token, color='orange', style='filled')
		self.validators[J_token] = J_token
 
	def draw_slash_double_prepare(self):
		return
	      
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

 