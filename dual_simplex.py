import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form,  parse_to_fpi,canonical_form
from printing_solutions import optimal_situation,non_viability_certificate

# It uses the first negative input found as a heuristic
def find_b_negative(matrix):
	matrix_lines = matrix.shape[0]
	for index in range(1,matrix_lines):
		if matrix[index,-1] < 0:
			return index
	return None

def find_pivot_dual_simplex(matrix,b_index):
	min_value = math.inf
	min_index = None

	begin_A_columns = matrix.shape[0] -1

	for index in range(begin_A_columns,matrix.shape[1]-1):
		if matrix[b_index, index] >= 0:
			continue

		curr_value = matrix[0,index] / (-matrix[b_index,index])
		if curr_value < min_value:
			min_value = curr_value
			min_index = index

	return min_index


def verify_state_dual_simplex(matrix):	


	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	c_negative_in_PL = all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns])
	b_positive = all(i >=0 for i in matrix[1:matrix.shape[0],-1])


	# Vector C negative in PL and B Positive - (True) Optimal Situation  
	# Vectors C Negative in PL and B Non-Positive - (False) Continue Dual Simplex
	# Vector C Non-negative in PL  - (None) Pass to Auxiliary PL
	if ( c_negative_in_PL ) and ( b_positive ):
		return True
	elif ( c_negative_in_PL ):
		return False 
	else:
		return None


def dual_simplex(matrix,base_columns):

	inviability = False
	b_index = find_b_negative(matrix)

	if(b_index is not None): # We still have negative entries of b in tableaux
		column_index = find_pivot_dual_simplex(matrix,b_index)

		if(column_index is not None):# We have, in the line b_index chosen, negative values of A
			pivoting(matrix,b_index,column_index)
			base_columns[b_index] = column_index
		else: # Situation of inviability PL - positive A input with negative B input and X> = 0
			inviability = True
			non_viability_certificate(matrix,base_columns)
	
	if(not inviability):
		simplex_state = verify_state_dual_simplex(matrix)

		if(simplex_state):
			optimal_situation(matrix,base_columns)
			return
		elif(simplex_state is None):
			# Do Auxiliary PL
			pass	
		else: 
			dual_simplex(matrix,base_columns)

def solve(matrix):

	matrix = parse_to_fpi(matrix)
	matrix = put_tableux_form(matrix)
	base_columns = np.zeros(matrix.shape[0])
	canonical_form(matrix,base_columns)
	dual_simplex(matrix,base_columns)
	
