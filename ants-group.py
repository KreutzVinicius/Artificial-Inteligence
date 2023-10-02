import random
import math

class Ant:
    def __init__(self, row, col):
        self.position = (row, col)
        self.isCarrying = False
        self.carryingData = None

def imprime_matriz(matriz):
    for linha in matriz:
        for elemento in linha:
            if elemento == (0,0,0):
                print(" ", end="")
            else:
                print(elemento[-1] , end="")
            print(" ", end="")
        print()

def imprime_formigas(ants):
    for ant in ants:
        print("position",ant.position,", carring:", ant.isCarrying, end="\n")
    print()


def get_distance(i,j,x, y):
    result =  math.dist((i,j) ,(float(x),float(y)))
    return result


def get_similarity(ant, movimentos):
    dist = 0
    sum = 0
    alpha = 5

    if (ant.isCarrying):
        x,y ,z = ant.carryingData
        for i,j in movimentos:
            dist = get_distance(i,j, x,y)
            sum += dist


    else:
        antPos = matriz[ant.position[0]][ant.position[1]]
        x,y,z = antPos
        if (x,y,z )!= (0,0,0):
            for i,j in movimentos:
                dist = get_distance(i,j, x,y)
                sum += dist

    if (movimentos == []):
        return 0
        
    return 1/pow(len(movimentos),2)*(1-(sum/alpha))        


ants = []
visionRange =  8
n  = 50 # tamanho da matriz
matriz = [[(0,0,0)]* n for _ in range(n)]

num_ants = 15

with open("dataset1.txt", "r") as arquivo:
    conteudo = arquivo.read()
    #divide o conteudo em linhas
    conteudo = conteudo.split("\n")
    #divide cada linha em suas variaveis
    for(i, linha) in enumerate(conteudo):
        conteudo[i] = linha.split("\t")
        conteudo[i][0] = conteudo[i][0].replace(',', '.')
        conteudo[i][1] = conteudo[i][1].replace(',', '.')
        # print(linha)

# num_food = 200

for i, _ in enumerate(conteudo):
    while True:
        row = random.randint(0, n - 1)
        col = random.randint(0, n - 1)

        if matriz[row][col] == (0,0,0):
            matriz[row][col] = conteudo[i]
            break

for _ in range(num_ants):
    while True:
        row = random.randint(0, n - 1)
        col = random.randint(0, n - 1)

        if matriz[row][col] == (0,0,0):
            ant = Ant(row, col)
            ants.append(ant)
            break

print("Matriz Inicial:\n")
imprime_matriz(matriz)
        
def proxima_posicao(ant):
    row, col = ant.position
    movimentos = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1),                       (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    movimentos_validos = []
    for dr, dc in movimentos:
        if 0 <= dr < n and 0 <= dc < n:
            movimentos_validos.append((dr, dc))

    value = 0
    posicoes_comida = []
    for dr, dc in movimentos_validos:
        if matriz[dr][dc] != (0,0,0):
            posicoes_comida.append((dr, dc))
    
    value = get_similarity(ant, posicoes_comida)


    # Se não possui comida
    if not ant.isCarrying:
        probabilidade_pegar = value
        rand = random.random()
        if (probabilidade_pegar > 0):
            print("random", rand, "< probabilidade", probabilidade_pegar)
        if rand < probabilidade_pegar:
 
            # Caso contrário, escolha aleatoriamente entre as comidas próximas
                if posicoes_comida != []:
                    proxima = random.choice(posicoes_comida)
                    ant.isCarrying = True
                    ant.carryingData = matriz[proxima[0]][proxima[1]]
                    matriz[proxima[0]][proxima[1]] = (0,0,0)
                    ant.position = proxima
                else:
                # Se não houver comida próxima, escolha uma direção aleatória
                    proxima = random.choice(movimentos_validos)
                    ant.position = proxima
        else:
            proxima = random.choice(movimentos_validos)
            ant.position = proxima

    else:
        probabilidade_largar = value
        rand = random.random()
        if (probabilidade_largar > 0):
            print("random", rand, "< probabilidade largar", probabilidade_largar)
        if rand < probabilidade_largar:
            proxima = random.choice(movimentos_validos)

            #se na proxima posicao nao tem um corpo
            if (matriz[proxima[0]][proxima[1]] == (0,0,0)):
                matriz[proxima[0]][proxima[1]] = ant.carryingData
                ant.carryingData = None
                ant.isCarrying = False
            ant.position = proxima

        else:
            proxima = random.choice(movimentos_validos)
            ant.position = proxima
    return ant, matriz

# Simule o movimento das formigas
for _ in range(10000):
    for i, ant in enumerate(ants):
        ant, matriz = proxima_posicao(ant)
# imprime_formigas(ants)


for ant in ants:
    while ant.isCarrying:
        ant, matriz = proxima_posicao(ant)

print("matriz depois de andar")
imprime_matriz(matriz)
# imprime_formigas(ants)



