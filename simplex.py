# -*- coding: utf-8 -*-
import os, sys
import numpy as np 
from pdb import set_trace
import math

from primal_simplex import solve as solve_primal_simplex
from dual_simplex import solve as solve_dual_simplex
from auxiliary_lp import solve as solve_auxiliary_lp

def verify_method(matrix):
	begin_C_columns = 0
	end_C_columns = matrix.shape[1]-2

	# Positive vectors C and B - (0) Simplex Primal  
	# Vector C Negative and B Non-positive - (1) Simplex Dual
	# Vectors C Non-negative and B Non-positive - (2) PL Auxiliar

	if (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns])) and (all(i >=0 for i in matrix[1:,-1]) ):
		return 0
	elif (all( i <=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (not (all(i >=0 for i in matrix[1:,-1]))) :
		return 1
	elif (not all( i <=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (not (all(i >=0 for i in matrix[1:,-1]))) :
		return 2 

def main():
	f = open(sys.argv[1], 'r')
	
	lines = int(f.readline()) + 1		#Wrong test input. Sum +1 was required
	columns = int(f.readline()) + 1 
	
	matrix_str = f.readline()
	matrix = np.array(np.mat(matrix_str).reshape(lines,columns),dtype=float)
	matrix = matrix.astype('object')
	
	method = verify_method(matrix)

	if(method == 0):
		solve_primal_simplex(matrix)
	elif(method==1):
		solve_dual_simplex(matrix)
	else:
		solve_auxiliary_lp(matrix)
	f.close()

main()