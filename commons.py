import numpy as np
from fractions import Fraction
from decimal import Decimal

from pdb import set_trace	

def add_identity_matrix(matrix, position, size,value):
	adicional_row = np.zeros(size)
	adicional_row = adicional_row+value
	identity = np.identity(size)
	sub_matrix = np.insert(identity, 0, adicional_row, axis=0)

	arrays_list = []
	for line_index in range(matrix.shape[0]):
		extended_row = np.insert(matrix[line_index], position, sub_matrix[line_index])
		arrays_list.append(extended_row)
	return np.array(arrays_list)

def parse_to_fpi(matrix):
	position = (matrix.shape[1])-1
	size = matrix.shape[0]-1
	return add_identity_matrix(matrix,position,size,0)

def put_tableux_form(matrix):
	matrix_A_lines = (matrix.shape[0]-1)
	matrix = add_identity_matrix(matrix,0,matrix_A_lines,0) # adds array of operations 
	matrix[0,:] = (-1)*matrix[0,:] # Negative vector c
	return matrix

def pivoting(matrix, line_index, column_index):
	
	factor_line = (matrix[line_index,:]).copy()
	for index in range(0,matrix.shape[0]):#line
		factor = Fraction( Fraction( (-matrix[index,column_index])),Fraction( (factor_line[column_index]))).limit_denominator(1000000)
		
		if index == line_index:
			for column in range(0,matrix.shape[1]):
				matrix[index,column] = Fraction(Fraction((matrix[index,column]))  , Fraction((factor_line[column_index]))).limit_denominator(1000000)
			
		else:
			for column in range(0,matrix.shape[1]):#column
				matrix[index,column] = Fraction( (factor_line[column]*factor)+ matrix[index,column]	).limit_denominator(1000000)

	f = open('primeiro.txt', 'r')
	conteudo = f.readlines()
	
	for index in range(0,matrix.shape[0]):
		conteudo.append(str(matrix[index,:].tolist())+"\n")
	conteudo.append("\n\n")	
	f = open('primeiro.txt', 'w')
	f.writelines(conteudo)
	f.close()

def canonical_form(matrix,base_columns):
	if(not verify_canonical_form(matrix,base_columns)):
		put_canonical_form(matrix,base_columns)

def verify_canonical_form(matrix,base_columns):

	begin_A_columns = matrix.shape[0]-1
	for index in range(begin_A_columns,matrix.shape[1]):
		count_ones = 0
		base = None
		if (matrix[0,index] == 0):
			for line in range(1,matrix.shape[0]):				
				if(matrix[line,index] == 1):
					count_ones+=1
					base = line
				elif(matrix[line,index] == 0):
					continue
				else:
					base = None
					break
		if(base is not None and count_ones == 1):
			base_columns[base] = index #to the base line of the 'base' line, my pivo is in the column base_columns [base]
	if(all( i >0 for i in base_columns)):
		return True
	else:
		return False

def put_canonical_form(matrix,base_columns):

	for linha in range(1 , base_columns.shape[0]):
		matrix[0,:] = matrix[linha,:]*( (-matrix[0,int(base_columns[linha])])/matrix[linha,int(base_columns[linha])])+matrix[0,:]	
	return matrix
