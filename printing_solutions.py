import numpy as np 
from pdb import set_trace
import math

def unlimited_certificate(matrix,c_index,base_columns):

	# Build certificate
	begin_A_columns = matrix.shape[0]-1
	certificate = np.zeros(matrix.shape[1] - (begin_A_columns+1))
	for index in range(1,len(base_columns)): 
		certificate[(int(base_columns[index])-begin_A_columns)] = -matrix[index,c_index]
	certificate[c_index-begin_A_columns] = 1
	
	conteudo = []
	conteudo.append("1"+'\n')
	conteudo.append(str((np.around( np.array(certificate,dtype=float), decimals=6).tolist() )))
	f = open('conclusao.txt', 'w')
	f.writelines(conteudo)
	f.close()
    


def optimal_situation(matrix,base_columns):
	#calcula solução 
	begin_A_columns = matrix.shape[0]-1
	solution = (np.zeros(matrix.shape[1] - (begin_A_columns))).astype('object')
	for index in range(1,len(base_columns)): #percorre quantidade de linhas 
		solution[(int(base_columns[index])-begin_A_columns)] = matrix[index,matrix.shape[1]-1]

	conteudo = []
	conteudo.append("2"+'\n')
	conteudo.append(str(np.around(np.array(solution[0:-(matrix.shape[0])],dtype=float), decimals=5).tolist())+'\n')
	conteudo.append(str(np.around(float(matrix[0,-1]) , decimals=5))+'\n')
	conteudo.append(str(np.around( np.array(matrix[0,0:(matrix.shape[0]-1)],dtype=float), decimals=6).tolist()))
	f = open('conclusao.txt', 'w')
	f.writelines(conteudo)
	f.close()

def non_viability_certificate(matrix,base_columns):
	
    conteudo = []
    conteudo.append("0"+'\n')
    conteudo.append(str((np.around(np.array((matrix[0,0:(matrix.shape[0]-1)]) ,dtype=float), decimals=5)).tolist()))
    f = open('conclusao.txt', 'w')
    f.writelines(conteudo)
    f.close()



