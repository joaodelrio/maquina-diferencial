#Entra o polinomio
#Exemplo: 2x^2 - 3x + 2
#X = 0 -> 2
#Ai incrementamos 0,1 no x
#X = 0,1 → 1,72
#A partir disso temos que calcular a diferença_1 que seria 2-1,72 = 0,28
#Ai incrementamos 0,1 no x
#X = 0,2 → 1,48
#A partir disso temos que calcular a diferença_1 que seria 1,72-1,48 = 0,24
#E por fim a diferença_2 que seria 0,28-0,24 = 0,04

#Importa a biblioteca para trabalhar com polinomios
from sympy import symbols
from sympy import poly
from sympy import solve
import pandas as pd
import numpy as np

def mostra_tabela(x, px, difs):
    # Cria uma tabela com pandas
    df = pd.DataFrame(columns=['x', 'p(x)', 'Dif_1', 'Dif_2'])
    for i in range(0, len(x)):
        dados = pd.DataFrame({'x': [x[i]], 'p(x)': [px[i]], 'Dif_2': [difs[1][i]]})
        df = pd.concat([df, dados], ignore_index=True)
        if len(x)-1 > i:
            dados = pd.DataFrame({'Dif_1': [difs[0][i]]})
            df = pd.concat([df, dados], ignore_index=True)
    print(df)

def calculo(polinomio,x, tamanho_tabela):
    # Analisa qual o grau do polinomio
    grau = polinomio.degree()

    # Cria uma lista para armazenar os valores de p(x)
    pxs = []

    # Cria uma lista para armazenar as diferenças
    difs = []
    dif_final = 0

    # Cria a quantidade de listas de acordo com o grau do polinomio
    for i in range(grau):
        difs.append([])

    j = 0
    # Calcula os valores de p(x) e as diferenças até achar a ultima diferença que é a diferença que repete
    for i in np.arange(0, 1, 0.1):
        # Pega o resultado de p(x)
        px = polinomio.subs(x, i)
        # Salva na tabela
        pxs.append(px)
        # Se tiver mais que um valor de p(x) calcula a diferença
        if len(pxs) > 1:
            difs[0].append(pxs[-2] - pxs[-1])

        # Se tiver mais que um valor na primeira diferença calcula a segunda diferença
        if len(pxs) > 2:
            # Salva a diferença que ira repetir
            dif_final = difs[0][-2] - difs[0][-1]
            difs[1].append(dif_final)
            # Pega da onde parou 
            j = i+0.1
            break

    for i in np.arange(j, tamanho_tabela, 0.1):
        difs[1].append(dif_final)
        difs[0].append(difs[0][-1] - dif_final)
        pxs.append(pxs[-1] - difs[0][-1])

    while(len(difs[1]) < len(pxs)):
        difs[1].append(dif_final)
        print("teste")

    x = np.arange(0, tamanho_tabela, 0.1)
    mostra_tabela(x, pxs, difs)




def main():
    x = symbols('x')
    polinomio = poly( 2*x**2- 3*x + 2)
    calculo(polinomio, x, 0.7)

if __name__ == '__main__':
    main()
