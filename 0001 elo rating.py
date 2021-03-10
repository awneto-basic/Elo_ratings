from random import randint
import re

file_name = "elo.csv"


class Filme:
    def __init__(self, index, title, elo_rating):
        self.index = index
        self.title = title
        self.elo_rating = elo_rating


def get_expected_rating(A, B):
    return (1 / (1 + 10 ** ((B - A) / 400)))

def update_rating(result,A,B,K):
    if result == "win":
        return (A + K * (1 - get_expected_rating(A, B)))
    if result == "lose":
        return (A + K * (0 - get_expected_rating(A, B)))
    if result == "tie":
        return (A + K * (0.5 - get_expected_rating(A, B)))




K = 32 # reajuste máximo por jogo

# lendo o arquivo contendo os filmes
with open(file_name, 'r', encoding="utf8") as reader:
    # Further file processing goes here
    linhas_lidas = reader.readlines()

#formatando os dados lidos em uma matrix Nx3, em que N é o número de linhas lidas
linhas_lidas[:] = [linha.split(';') for linha in linhas_lidas]
linhas_lidas[:] = [[entrada.strip('\ufeff\n') for entrada in linha] for linha in linhas_lidas]

N = len(linhas_lidas)

print("\tCOMPARADOR DE FILMES\t")
print("\n")
while (True):
    print("Compare os filmes abaixo.")
    print("Selecione o melhor filme entre as duas opções (A ou B)")
    print("Digite E no caso de empate")
    print("(Digite Q para sair)")

    index_A = randint(1, N) - 1
    index_B = index_A
    while (index_B == index_A):
        index_B = randint(1, N) - 1

    filmeA = Filme(index_A, linhas_lidas[index_A][1], float(linhas_lidas[index_A][2]))
    filmeB = Filme(index_B, linhas_lidas[index_B][1], float(linhas_lidas[index_B][2]))

    print("Filme A:\t{}".format(linhas_lidas[index_A][1]))
    print("Filme B:\t{}".format(linhas_lidas[index_B][1]))

    rule = r"^[AaBbEeQqPp]{1}$"
    key = input()
    while (not re.match(rule, key)):
        print("Entrada incorreta.\n")
        print("Compare os filmes abaixo.")
        print("Selecione o melhor filme entre as duas opções (A ou B)")
        print("Digite E no caso de empate")
        print("Digite P para pular")
        print("(Digite Q para sair)")
        print("Filme A:\t{}".format(filmeA.title))
        print("Filme B:\t{}".format(filmeB.title))
        key = input()

    if (key in {'Q', 'q'}):
        break
    elif (key in {'A', 'a'}):
        filmeA.elo_rating = update_rating("win",filmeA.elo_rating,filmeB.elo_rating,K)
        filmeB.elo_rating = update_rating("lose", filmeB.elo_rating, filmeA.elo_rating, K)

    elif (key in {'B', 'b'}):
        filmeA.elo_rating = update_rating("lose", filmeA.elo_rating, filmeB.elo_rating, K)
        filmeB.elo_rating = update_rating("win", filmeB.elo_rating, filmeA.elo_rating, K)

    elif (key in {'E', 'e'}):
        filmeA.elo_rating = update_rating("tie", filmeA.elo_rating, filmeB.elo_rating, K)
        filmeB.elo_rating = update_rating("tie", filmeB.elo_rating, filmeA.elo_rating, K)
    if (key in {'P', 'p'}):
        continue
    print("\n")
    print("O filme \"{}\" agora possui um índice ELO de {}.".format(filmeA.title, filmeA.elo_rating))
    print("O filme \"{}\" agora possui um índice ELO de {}.".format(filmeB.title, filmeB.elo_rating))
    print("\n")

    linhas_lidas[index_A][2] = str(filmeA.elo_rating)
    linhas_lidas[index_B][2] = str(filmeB.elo_rating)

#Fim do laço de repetição
linhas_lidas[:] = [";".join(linha) for linha in linhas_lidas]
linhas_lidas[:] = [linha + "\n" for linha in linhas_lidas]
print(linhas_lidas)
#Salva o arquivo texto
with open(file_name, 'w',encoding="utf8") as writer:
    # Further file processing goes here
    writer.seek(0) #retorna o arquivo para o início
    writer.writelines(linhas_lidas)

#fim do programa
