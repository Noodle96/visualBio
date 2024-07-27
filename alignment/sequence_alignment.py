import sys
from collections import deque

# Definimos las variables globales
diag = 0
up = 0
leftt = 0
ans = deque()
dp = []
cantidadCadenas = 0
alineacionesTotales = []

# Matriz de direcciones
# 0 -> Diagonal
# 1 -> Up
# 2 -> Left
dp_direcciones = []

def reset_globals():
    global diag, up, leftt, ans, dp, cantidadCadenas, alineacionesTotales, dp_direcciones
    diag = 0
    up = 0
    leftt = 0
    ans = deque()
    dp = []
    cantidadCadenas = 0
    alineacionesTotales = []
    dp_direcciones = []

def dfs(x, y, secuenciaOne, secuenciaTwo):
    global cantidadCadenas, ans, alineacionesTotales
    if x == 0 and y == 0:
        cantidadCadenas += 1
        first, second = "", ""
        for e in range(len(ans) - 1, -1, -1):
            first += ans[e][0]
        for e in range(len(ans) - 1, -1, -1):
            second += ans[e][1]
        alineacionesTotales.append((first, second))
        return

    if dp_direcciones[x][y][0]:
        if x > 0 and y > 0:
            ans.append((secuenciaOne[x - 1], secuenciaTwo[y - 1]))
            dfs(x - 1, y - 1, secuenciaOne, secuenciaTwo)
            ans.pop()

    if dp_direcciones[x][y][1]:
        if x > 0:
            ans.append((secuenciaOne[x - 1], '-'))
            dfs(x - 1, y, secuenciaOne, secuenciaTwo)
            ans.pop()

    if dp_direcciones[x][y][2]:
        if y > 0:
            ans.append(('-', secuenciaTwo[y - 1]))
            dfs(x, y - 1, secuenciaOne, secuenciaTwo)
            ans.pop()

def solve(secuenciaOne, secuenciaTwo):
    reset_globals()  # Reiniciar variables globales
    global dp, dp_direcciones

    if len(secuenciaOne) < len(secuenciaTwo):
        secuenciaOne, secuenciaTwo = secuenciaTwo, secuenciaOne

    sizeOne = len(secuenciaOne)
    sizeTwo = len(secuenciaTwo)

    dp = [[0] * (sizeTwo + 1) for _ in range(sizeOne + 1)]
    dp_direcciones = [[[0, 0, 0] for _ in range(sizeTwo + 1)] for _ in range(sizeOne + 1)]

    val = 0
    for e in range(sizeOne + 1):
        dp[e][0] = val
        val -= 2
        if e != 0:
            dp_direcciones[e][0][1] = 1

    val = 0
    for e in range(sizeTwo + 1):
        dp[0][e] = val
        val -= 2
        if e != 0:
            dp_direcciones[0][e][2] = 1

    for e in range(1, sizeOne + 1):
        for j in range(1, sizeTwo + 1):
            diag = dp[e - 1][j - 1] + (1 if secuenciaOne[e - 1] == secuenciaTwo[j - 1] else -1)
            up = dp[e - 1][j] - 2
            leftt = dp[e][j - 1] - 2
            dp[e][j] = max(diag, up, leftt)
            if dp[e][j] == diag:
                dp_direcciones[e][j][0] = 1
            if dp[e][j] == up:
                dp_direcciones[e][j][1] = 1
            if dp[e][j] == leftt:
                dp_direcciones[e][j][2] = 1

    print(f"Score Optimo: {dp[sizeOne][sizeTwo]}\n")

    print("Matrix")
    for e in range(sizeOne + 1):
        for j in range(sizeTwo + 1):
            print(dp[e][j], end=" ")
        print()
    print()

    i = sizeOne
    j = sizeTwo
    print("Alineamientos Generados")
    dfs(sizeOne, sizeTwo, secuenciaOne, secuenciaTwo)
    print(f"Cantidad de alineamientos producidos: {cantidadCadenas}")
    print("Alineaciones Totales")
    for alineacion in alineacionesTotales:
        print(alineacion[0])
        print(alineacion[1])
        print()
    return dp, cantidadCadenas, alineacionesTotales
