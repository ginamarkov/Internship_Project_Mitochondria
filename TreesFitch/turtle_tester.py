from Bio import AlignIO
from parsimony_tree import Parsimony_Tree
from parsimony_node import Parsimony_Node
from turtle_helper_functions import *
import time

def main():
	newick_file = open('105treesOutgroupNamed.txt','rU')
	newick_trees = newick_file.readlines()

	score_dataset("morph_data.nex",newick_trees)
	score_dataset("RAG1_trimmed.nex",newick_trees)
	score_dataset("CYTB_trimmed.nex",newick_trees)


def score_dataset(file_name, newick_trees):
	print("Finding best tree for " + file_name + "...")

	nexus_file = AlignIO.read(open("nexus_files/"+file_name), "nexus")
	nexus_data = get_matrix_and_order(nexus_file)

	scores = score_all_trees(nexus_data,newick_trees)
	find_best_tree(scores, newick_trees)


def score_all_trees(nexus_data, newick_trees):
	parsimony_scores = []
	for newick in newick_trees:
		score = score_tree(nexus_data, newick)
		parsimony_scores.append(score)

	return parsimony_scores


def score_tree(nexus_data, newick):
	tree = Parsimony_Tree(newick)
	newick_taxa = tree.get_taxa_list()
	
	num_cols = len(nexus_data[1][0])
	total_parsimony_score = 0
	for i in range(num_cols):
		char_column = get_character(newick_taxa, nexus_data[1], i, nexus_data[0])
		node_list = tree.add_leaf_states(char_column)
		total_parsimony_score += fitch_bottom_up(node_list)
	return total_parsimony_score


def fitch_bottom_up(node_list):
	parsimony_score = 0
	for node in node_list:
		if not node.is_leaf():
			intersection = get_intersection(node.left.state, node.right.state)
			if intersection:
				node.state = intersection
			else:
				union = get_union(node.left.state, node.right.state)
				node.state = union
				parsimony_score += 1
	return parsimony_score

def find_best_tree(scores, newick_trees):
	best_score = min(scores)
	best_index = scores.index(best_score)
	print(best_index)
	print(newick_trees[best_index])

start_time = time.time()
main()
print("---", time.time()-start_time,"---")
