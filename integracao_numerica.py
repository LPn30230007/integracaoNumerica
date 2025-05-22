# Exercícios de 1 a 7

import math

from fontTools.misc.bezierTools import epsilon


def abs(x):
    if x > 0:
        return (x)
    else:
        return (-x)

a = 3
b = 12

f1 = lambda x: math.log(1 + x) * math.sin(0.1 * x) / (x * (1 + x)) * math.exp(x)
f2 = lambda x: math.sin(x) * math.exp(x / 10) * math.cos(1 / x)
f3 = lambda x: x ** 2 + 2
f4 = lambda x: math.log(1 + x) * math.sin(0.1 * x) / (x * (1 + x)) * math.exp(x)
f5 = lambda x: math.exp(2 ** x) - x ** 10

'''
# TEST 0:
f=input("Qual é a função? ")
x=float(input("Qual é o valor? "))
print(f,"(",x,")=",eval(f)(x))     
'''


# 1º Exercício
def T(f, c, d):
    if c > d or c < a or d > b:
        print("Limites são ilegais!")
        return (None)
    return ((d - c) * (f(c) + f(d)) / 2)


'''
# TEST 1:
c=float(input("Limite esquerda: "))
d=float(input("Limite direita: "))
f=input("A função: ")
print("T(",f,",",c,",",d,")=",T(eval(f),c,d))     
'''


# 2º Exercício
def Ti(f, c, d, i):
    if i == 0:
        #        print("Parcial recursivo: ",c,d,T(c,d))
        return T(f, c, d)
    return (Ti(f, c, (c + d) / 2, i - 1) + Ti(f, (c + d) / 2, d, i - 1))


# 3º Exercício
def Tn(f, c, d, n):
    soma = 0
    unidade = (d - c) / n
    for i in range(0, n):
        soma = soma + T(f, c + i * unidade, c + (i + 1) * unidade)
    return (soma)


# 4º Exercício
def TiForcaBruta(f, c, d):
    last = T(f, c, d)
    actual = Ti(f, c, d, 1)
    i = 1
    while last != actual:
        i = i + 1
        last = actual
        actual = Ti(f, c, d, i)
        print("etapa ", i, " --> Area: ", actual)
    return (actual)


# 5º Exercício
def S(f, c, d):
    return ((d - c) / 6 * (f(c) + 4 * f((c + d) / 2) + f(d)))


'''
# TEST 5:
c=float(input("Limite esquerda: "))
d=float(input("Limite direita: "))
f=input("A função: ")
print("S(",f,",",c,",",d,")=",S(eval(f),c,d), " versus ","T(",f,",",c,",",d,")=",T(eval(f),c,d))     
'''


# 6º Exercício
def Sn(f, c, d, n):
    if n == 0: return (S(f, c, d))
    return Sn(f, c, (c + d) / 2, n - 1) + Sn(f, (c + d) / 2, d, n - 1)


'''
# TEST 6:
c=float(input("Limite esquerda: "))
d=float(input("Limite direita: "))
n=int(input("Nº das etapas: "))
f=input("A função: ")
print("Si(",f,",",c,",",d,",",n,")=",Sn(eval(f),c,d,n), " versus ","S(",f,",",c,",",d,")=",S(eval(f),c,d))     
print(" versus ","Ti(",f,",",c,",",d,",",n,")=",Ti(eval(f),c,d,n),)     
'''


# 7º Exercício
def TGreedy(f, c, d, epsilon):
    last = T(f, c, d)
    actual = Ti(f, c, d, 1)
    i = 1
    while i < 31:
        if abs(last - actual) > epsilon:
            if abs(actual - Sn(f, c, d, i)) > epsilon:
                return (actual)

        i = i + 1
        last = actual
        actual = Ti(f, c, d, i)
    #    print(i)
    return (None)


'''
# TEST 7:
c=float(input("Limite esquerda: "))
d=float(input("Limite direita: "))
epsilon=float(input("Precição: "))
f=input("A função: ")
print("Ti=",Ti(eval(f),c,d,i)," vs. T=",T(eval(f),c,d))     
'''



# Exercicio 8

'''
É mais vantajoso usar Tn(f,c,d) e Sn(f,c,d) de forma iterativa porque se podem aproveitar valores já calculados, 
enquanto a forma recursiva acumula os valores de cada chamada, independentemente de já terem sido calculados. 
No exemplo do enunciado, ao dobrar o número de intervalos (n -> 2n), metade dos pontos já foi calculada, sendo apenas 
necessário calcular os pontos intermédios (no caso de Tn).

O método forward aumenta o número de intervalos de forma progressiva até que o erro seja menor que o valor determinado 
para a precisão. Já o método backtracking começa com um número elevado de intervalos e vai diminuindo até que o erro 
seja maior que o determinado para a precisão, voltando depois para o valor anterior. Assim, o forward é mais vantajoso 
porque evita cálculos desnecessários.

No método do trapézio iterativo, os valores calculados em Tn são reaproveitados e apenas os novos pontos médios são 
calculados em T2n. No método que utiliza a regra de Simpson, os extremos e pontos médios em Sn são reaproveitados e 
apenas os novos pontos são calculados em S2n.
'''

# Exercicio 9

def I_dinamica(f, c, d, epsilon, n=0):
    '''
    Função dinâmica para calcular a integral de forma recursiva, utilizando os métodos do trapézio e a regram de
    Simpson.
    :param f: função fornecida
    :param c: valor mínimo
    :param d: valor máximo
    :param epsilon: valor da precisão
    :param n: valor do subintervalo, iniciado a zero
    :return: valor da integral
    '''
    meio = (c + d) / 2 # calcula o meio do intervado [c,d]

    T_valor = T(f, c, d)  # aplica o método do trapézio no intervalo [c,d]
    S_valor = S(f, c, d)  # aplica a regra de Simpson no intervalo [c,d]

    # testa se diferença entre os dois valores é menor que o limite (epsilon dividido por 2^(n+1))
    if abs(S_valor - T_valor) > epsilon / (2 ** (n + 1)): # se maior, subdivide o intervalo

        # chama a função recursivamente para cada nova metade
        esquerda = I_dinamica(f, c, meio, epsilon, n + 1)
        direita = I_dinamica(f, meio, d, epsilon, n + 1)

        return esquerda + direita  # Soma as duas partes para obter o resultado final

    return S_valor # se menor, retorna o valor calculado pela regra de Sinpsom

'''
# TEST 9:
c = float(input("Limite esquerda: "))
d = float(input("Limite direita: "))
epsilon = float(input("Precisão: "))
f_str = input("Função: ")
f = eval(f_str)
print(f"\nO valor aproximado da integral da função {f_str} entre {c} e {d} é: {I_dinamica(f, c, d, epsilon):.3f}")
'''


