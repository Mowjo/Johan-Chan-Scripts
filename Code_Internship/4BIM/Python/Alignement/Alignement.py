#########################################
#   ALIGNEMENT :  NEEDELMAN-WUNCH
#
########################################
#


def compare(seq1,seq2,corresp,miss,i,j):
	score = 0
	if seq1[i] == seq2[j]:
		score = corresp
	else:
		score = miss
	return score


def initialisation(seq1,seq2):
	nouv_seq1 = "0" + seq1
	nouv_seq2 = "0" + seq2
	
	matrice = [[]]
	for i in range(len(nouv_seq1)):
		matrice[0].append(-i)
	for j in range(1,len(nouv_seq2)):
		matrice.append([])
		matrice[j].append(-j)
	return matrice,nouv_seq1,nouv_seq2
def affichage(matrice):
	for j in range(len(matrice)):

		ligne = ""
		for i in range(len(matrice[j])):
			ligne += str(matrice[j][i])+ "\t"
		print ligne

def score(seq1,seq2,matrice,i,j):
	list_score = []
	temp = matrice[j-1][i-1] + compare(seq1,seq2,0,1,i,j)# on pose 0 pour match et 1 pour mismatch 
	list_score.append(temp)
	temp = matrice[j][i-1] - 100 # theoriquement le gap est fixe a -inf
	list_score.append(temp)
	temp = matrice[j-1][i] - 100 # theoriquement le gap est fixe a -inf
	list_score.append(temp)
	return max(list_score)

def complete(aa1,aa2):
	matrice = initialisation(aa1,aa2)[0]
	seq1 = initialisation(aa1,aa2)[1]
	seq2 =initialisation(aa1,aa2)[2]
	for j in range(1,len(seq2)):
		for i in range(1,len(seq1)):
			result = score(seq1,seq2,matrice,i,j)
			matrice[j].append(result)
	affichage(matrice)
	return matrice[len(aa1)][len(aa2)] # retourne le nombre suppose de mutations



a = "AGACTAGTTAC"
b = "CGCCCAGGTAC"

#matrice = initialisation(a,b)
#affichage(matrice[0])

complete(a,b)
print complete(a,b)
