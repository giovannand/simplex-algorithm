import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form, parse_to_fpi,canonical_form
from printing_solutions import optimal_situation, unlimited_certificate

# It uses the first negative input found as a heuristic
def find_c_negative(matrix): 
	begin_A_columns = matrix.shape[0]-1
	end_A_columns = matrix.shape[1]
	for index in range(begin_A_columns, end_A_columns):
		if matrix[0,index] < 0:
			return index
	return None

def find_pivot_primal_simplex(matrix,c_index):
	min_value = math.inf
	min_index = None

	for index in range(1, matrix.shape[0]):
		if matrix[index, c_index] <= 0:
			continue

		curr_value = matrix[index, -1] / matrix[index,c_index]
		if curr_value < min_value:
			min_value = curr_value
			min_index = index

	return min_index 

def verify_state_primal_simplex(matrix):	
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1

	# Positive vectors C (in tableux) and B - (True) Optimal Situation  
	# Vector C positive (in tableux) and B Non-positive - (1) Pass to Dual Simplex 
	# Vectors C Non-positive (in tableux) - (False) Continue Primal Simplex

	if (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (all(i >=0 for i in matrix[1:,-1]) ):
		return True
	elif (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns]) ):
		return None
	else:
		return False 

def primal_simplex(matrix,base_columns):

	unlimited_control = False
	c_index = find_c_negative(matrix) 
	
	if (c_index is not None): # We still have negative (-c) entries in tableaux
		line_index =  find_pivot_primal_simplex(matrix,c_index) 

		if (line_index is not None): # We have, in column c_index chosen, positive values in matrix A
			pivoting(matrix,line_index,c_index)
			base_columns[line_index] = c_index
		elif(matrix[0,c_index] < 0 ): # We haven't positive values in matrix A
			unlimited_control = True
			unlimited_certificate(matrix,c_index,base_columns)
		else:
			raise "Error - Choose c_index = 0, with an entire column less than or equal to zero"

	if(not unlimited_control):
		simplex_state = verify_state_primal_simplex(matrix)

		if(simplex_state): 
			optimal_situation(matrix,base_columns) 
			return
		elif(simplex_state is None):
			# Do simple dual
			pass	
		else: 
			primal_simplex(matrix,base_columns)

def solve(matrix):
	matrix = parse_to_fpi(matrix)
	matrix = put_tableux_form(matrix)
	base_columns = np.zeros(matrix.shape[0])
	canonical_form(matrix,base_columns)
	primal_simplex(matrix,base_columns)
	