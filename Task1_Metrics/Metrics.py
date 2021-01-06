import numpy as np

d = -1
m = 1
s = -1


seq1 = "TTTCTGCCAGGACTCTTGATGATGTGCGGTTTGCTTTCAGGGATAGGAAGATAAAAACGCTAAAAGAAGACAAAAATATTAACACAATAATAAAAAAAAAAAGCCAGAAAAAATAGTAGTTTTTCAAGAACACTTCAGAATCCTGATACTTTACATGAACCAAGAAATATAGACATAAAAAAGAGACACACACCTGTAAGGAGAGATGAGACACAGGACTGGGTTACTTTTGATGAAGAGGCTTCTTACCAGTTACAACTGAAGTGAGTAAGAAGAAATTAGCTACTTTTTTCAAGATCTGTGGTAGATAAAATGTAGGTCAGTTTGAGTCTGAAATAAATGGAGGAGTGAAATACAGAAGTACAGGGATAGAGAGACAGAACATAAATCTAAGTTACCAACATCAGGAATAAAAAAGAGGACATTAATACAGACAGAAATTATGAATATCAGAATATAATAGATGTTATGAACAATTCTTTAGCACTAATTTTGACACTTTAATGAAGTGGACAAAATAGTTAACACACACACACACACAACTTATCA"
seq2 = "TGCTGTCTTGGCTGCTGCCATGTAAGATGTGACTTTGCTCCTCCTTGCCTTCCACAATGATTGTGAGGCCTCCCTAACCATGTGGAACTATGAGTCAATTAAACTTCTTTCCTTTATAAATCACTCAGACTCAGGTATATCTTTATTAGCAGTCTGAGAACAGACTAATACACTCTTTTTATATAACTAATCACCAAATTCTAGTTTTCCCCTTCCAGATGTCTCTAGATTTGTCCTTCTTTTGATATTTTTATCACCCTGTTTCAGCCTGCCATCCAGTGCACACTTATTGGACACCATCTCCTAGGAACAACATTAGCTGATGGGGGATATATCAAGGATTAACCCAATCCCTGCCTTCAGGGAGCTAACCAGCAGGGAGATGGTCAAGTAAACAGCAGCCATAAGCAGGGTGTGGTAAATGCTGTTTAGAGGCTGTGCAGGGGTGCTATGGAGCACAGAGAACTTGAAAACCTAGCCCTGAGGGGCCTCTGCACATAGAGGATTCAGATCTGGAGTC"

# Функция, создающая матрицу из нулей
def zeros(rows, cols):
    retval = []
    for x in range(rows):
        retval.append([])
        for y in range(cols):
            retval[-1].append(0)
    return retval

# сравнивает соответствующие элементы
def match_score(alpha, beta):
    if alpha == beta:
        return m
    elif alpha == '-' or beta == '-':
        return d
    else:
        return s

def needleman_wunsch(seq1, seq2):
    n = len(seq1)
    m = len(seq2)

    score = zeros(m + 1, n + 1)

    # Заполняем первый столбец
    for i in range(0, m + 1):
        score[i][0] = d * i

    # Заполняем первую строчку
    for j in range(0, n + 1):
        score[0][j] = d * j

    # Вычисляем табличку
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score[i - 1][j - 1] + match_score(seq1[j - 1], seq2[i - 1])
            delete = score[i - 1][j] + d
            insert = score[i][j - 1] + d
            # находим максимальный
            score[i][j] = max(match, delete, insert)


    for elem in score:
        print(elem)

    align1 = ""
    align2 = ""

    # Начинаем с нижнего правого конца матрицы
    i = m
    j = n

    # We'll use i and j to keep track of where we are in the matrix, just like above
    while i > 0 and j > 0:  # end touching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i - 1][j - 1]
        score_up = score[i][j - 1]
        score_left = score[i - 1][j]


        if score_current == score_diagonal + match_score(seq1[j - 1], seq2[i - 1]):
            align1 += seq1[j - 1]
            align2 += seq2[i - 1]
            i -= 1
            j -= 1
        elif score_current == score_up + d:
            align1 += seq1[j - 1]
            align2 += '-'
            j -= 1
        elif score_current == score_left + d:
            align1 += '-'
            align2 += seq2[i - 1]
            i -= 1


    while j > 0:
        align1 += seq1[j - 1]
        align2 += '-'
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i - 1]
        i -= 1


    align1 = align1[::-1]
    align2 = align2[::-1]

    return (align1, align2)


output1, output2 = needleman_wunsch(seq1, seq2)
size = 100
for i in range(len(output1)//size):
    print("1:", output1[i*size:min((i+1)*size, len(output1)-1)])
    print("2:", output2[i*size:min((i+1)*size, len(output2)-1)])
