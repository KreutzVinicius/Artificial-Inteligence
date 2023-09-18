import random

class Ant:
    def __init__(self, row, col):
        self.position = (row, col)
        self.isCarrying = False

def imprime_matriz(matriz):
    for linha in matriz:
        for elemento in linha:
            if elemento == 0:
                print(" ", end="")
            else:
                print(elemento, end="")
            print(" ", end="")
        print()

ants = []
visionRange =  8
n  = 50 # tamanho da matriz
matriz = [[0]* n for _ in range(n)]

num_ants = 15
num_food = 200

for _ in range(num_food):
    while True:
        row = random.randint(0, n - 1)
        col = random.randint(0, n - 1)

        if matriz[row][col] == 0:
            matriz[row][col] = 1
            break

for _ in range(num_ants):
    while True:
        row = random.randint(0, n - 1)
        col = random.randint(0, n - 1)

        if matriz[row][col] == 0:
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

    comidas_proximas = 0
    posicoes_comida = []
    for dr, dc in movimentos_validos:
        if matriz[dr][dc] == 1:
            comidas_proximas += 1
            posicoes_comida.append((dr, dc))


    # Se não possui comida
    if not ant.isCarrying:
        probabilidade_pegar = 1 - (pow(comidas_proximas,2)/visionRange)
        rand = random.random()
        # Probabilidade de pegar comida dependendo da quantidade de comidas próximas
        if rand < probabilidade_pegar:
            # Se houver uma comida próxima, pegue-a
            if comidas_proximas == 1:
                proxima = posicoes_comida[0]
                ant.isCarrying = True
                matriz[proxima[0]][proxima[1]] = 0
                ant.position = proxima
            # Caso contrário, escolha aleatoriamente entre as comidas próximas
            else:
                if comidas_proximas > 1:
                    proxima = random.choice(posicoes_comida)
                    ant.isCarrying = True
                    matriz[proxima[0]][proxima[1]] = 0
                    ant.position = proxima
                else:
                # Se não houver comida próxima, escolha uma direção aleatória
                    proxima = random.choice(movimentos_validos)
                    ant.position = proxima
        else:
            proxima = random.choice(movimentos_validos)
            ant.position = proxima

    else:
        # Probabilidade de largar comida dependendo da quantidade de comidas próximas
        probabilidade_largar = pow(comidas_proximas,2)  / visionRange
        rand = random.random()
        if rand < probabilidade_largar:
            proxima = random.choice(movimentos_validos)

            #se na proxima posicao nao tem um corpo
            if (matriz[proxima[0]][proxima[1]] == 0):
                matriz[proxima[0]][proxima[1]] = 1
                ant.isCarrying = False
            ant.position = proxima

        else:
            proxima = random.choice(movimentos_validos)
            ant.position = proxima
    return ant, matriz

# Simule o movimento das formigas
for _ in range(500000):
    for i, ant in enumerate(ants):
        ant, matriz = proxima_posicao(ant)

for ant in ants:
    while ant.isCarrying:
        ant, matriz = proxima_posicao(ant)

print("matriz depois de andar")
imprime_matriz(matriz)




