from collections import defaultdict
from alignment.sequence_alignment import solve

matriz_scores = []
map_first_alignment = defaultdict(lambda: defaultdict(str))

def startAligmentFunction(sequences):
    global matriz_scores, map_first_alignment

    # Inicializar la matriz de scores con 0s
    matriz_scores = [[0] * len(sequences) for _ in range(len(sequences))]
    print("Matriz scores: ", matriz_scores)

    # Llenar la matriz con los scores
    for e in range(len(sequences)):
        for j in range(e, len(sequences)):
            if e == j:
                matriz_scores[e][j] = 0
            else:
                dp, cantidadCadenas, alineacionesTotales = solve(sequences[e], sequences[j], 2)
                bestScore = dp[-1][-1]
                # Seleccionamos la mejor alineación (la primera en la lista `alineacionesTotales`)
                alineacion = alineacionesTotales[0]

                # Concatenamos las dos partes de la alineación como una sola cadena para simplificar
                map_first_alignment[e][j] = f"{alineacion[0]}|{alineacion[1]}"
                map_first_alignment[j][e] = f"{alineacion[0]}|{alineacion[1]}"
                matriz_scores[e][j] = bestScore
                matriz_scores[j][e] = bestScore

    # Imprimir matriz de scores
    print("(i) print matriz scores")
    for e in range(len(sequences)):
        sumatoria = sum(matriz_scores[e])
        print(" ".join(map(str, matriz_scores[e])), "=", sumatoria)
    print()


    # Encontrar el centro de la matriz
    maximo = -float('inf')
    row_max = -1
    for e in range(len(sequences)):
        S_c = sum(matriz_scores[e])
        if S_c > maximo:
            maximo = S_c
            row_max = e
    print(f"El centro es: S{row_max + 1}: {sequences[row_max]}")

    print("row_max: ", row_max)

    # Encontrar alineamiento de cada secuencia con la estrella
    print("\n(ii) alineamiento de cada secuencia con la estrella")
    maximo_len_row = -1000000
    maximo_len_row = max(len(sequences[row_max]), max(len(aln.split("|")[0]) for _, aln in map_first_alignment[row_max].items()))
    #maximo_len_row = max(len(sequences[row_max]), maximo_len_row)
    print("al momento maximo_len_row: ", maximo_len_row)

    for e in range(len(sequences)):
        if e != row_max:
            alineamiento = map_first_alignment[e][row_max]
            print(alineamiento)
            seq1, seq2 = alineamiento.split("|")
            print(f"S{row_max + 1}| {seq1}")
            print(f"S{e + 1}| {seq2}\n")


    # Alineamiento múltiple
    print("\n(iii) alineamiento múltiple")
    multipleAligment_representation = [['-'] * maximo_len_row for _ in range(len(sequences))]
    print("multipleAligment_representation")
    print(multipleAligment_representation)
    # Para la cadena estrella
    for e, char in enumerate(sequences[row_max]):
        multipleAligment_representation[row_max][e] = char

    for e in range(len(sequences)):
        if e != row_max:
            alineamiento = map_first_alignment[e][row_max]
            _, seq2 = alineamiento.split("|")
            for j in range(len(seq2)):
                multipleAligment_representation[e][j] = seq2[j]

    # Imprimir alineamiento múltiple
    for e in range(len(sequences)):
        print(f"S{e + 1}| {''.join(multipleAligment_representation[e])}")

    return matriz_scores, row_max, multipleAligment_representation
