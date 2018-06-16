import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form,  parse_to_fpi,add_identity_matrix,put_canonical_form
from primal_simplex import verify_state_primal_simplex,find_c_negative,find_pivot_primal_simplex
from primal_simplex import primal_simplex as solve_primal_simplex  
from printing_solutions import unlimited_certificate,optimal_situation,non_viability_certificate

def transform_b_positive(matrix):
	for index in range(1,(matrix.shape[0])):
		if matrix[index,-1] < 0:
			matrix[index,:] = (-1)*matrix[index,:] 
	return matrix

def zero_vector_c(matrix):
	matrix[0,:] = 0
	return matrix

def prepare_for_primal_simplex(matrix,original_matrix,base_columns):
	
	end_c = matrix.shape[1]-matrix.shape[0]-1
	original_matrix = parse_to_fpi(original_matrix)


	original_matrix = put_tableux_form(original_matrix)
	original_matrix[1:original_matrix.shape[0], 0:end_c ] = matrix[1:matrix.shape[0], 0:end_c ]
	original_matrix[1:original_matrix.shape[0], -1 ] = matrix[1:matrix.shape[0], -1]
	
	original_matrix = put_canonical_form(original_matrix,base_columns)

	solve_primal_simplex(original_matrix,base_columns)

def primal_simplex_auxiliar_pl(matrix,base_columns,original_matrix):

	c_index = find_c_negative(matrix) 
	unlimited_control = 0

	if (c_index is not None): # We still have negative (-c) entries in tableaux
		line_index =  find_pivot_primal_simplex(matrix,c_index)

		if (line_index is not None): # We have, in column c_index chosen, positive values in matrix A
			pivoting(matrix,line_index,c_index)
			base_columns[line_index] = c_index
		elif(matrix[0,c_index] < 0 ): #situação de pl ilimitada
			pass
			unlimited_control = 1
		else:
			raise "Error - Choose c_index = 0, with an entire column less than or equal to zero"

	if(unlimited_control != 1):
		simplex_state = verify_state_primal_simplex(matrix)
		if(simplex_state): 
			if ( (matrix[0,-1]) == 0 ):
				prepare_for_primal_simplex(matrix,original_matrix,base_columns)
			else:
				non_viability_certificate( matrix,base_columns)
			return
		elif(simplex_state is None):
			# Do simple dual
			pass	
		else:
			primal_simplex_auxiliar_pl(matrix,base_columns,original_matrix)


def solve(matrix):
	
	original_matrix = matrix
	base_columns = np.zeros(matrix.shape[0])
	
	matrix = parse_to_fpi(matrix)
	
	matrix = zero_vector_c(matrix)

	matrix = put_tableux_form(matrix)

	matrix = transform_b_positive(matrix)

	matrix = add_identity_matrix(matrix,matrix.shape[1]-1,matrix.shape[0]-1,1)

	end_c = matrix.shape[1]-matrix.shape[0]
	for index in range(1,(matrix.shape[0])):
		base_columns[index] = end_c
		end_c = end_c+1


	matrix = put_canonical_form(matrix,base_columns)

	primal_simplex_auxiliar_pl(matrix,base_columns,original_matrix)

