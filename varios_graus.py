#Entra o polinomio
#Exemplo: 2x^2 - 3x + 2
#X = 0 -> P(x) = 2
#Ai incrementamos 0,1 no x
#X = 0,1 →P(x) = 1,72
#A partir disso temos que calcular a diferença_1 que seria 2-1,72 = 0,28
#Ai incrementamos 0,1 no x
#X = 0,2 → P(x) = 1,48
#A partir disso temos que calcular a diferença_1 que seria 1,72-1,48 = 0,24
#E por fim a diferença_2 que seria 0,28-0,24 = 0,04

#Importa a biblioteca para trabalhar com polinomios
from sympy import symbols
from sympy import poly
from sympy import solve
import pandas as pd
import numpy as np

def mostra_tabela(x, px, difs):
    def round_floats(val):
        val = float(val)
        val = round(val, 5)
        return val
    # Cria uma tabela vazia com pandas
    df = pd.DataFrame(columns=['x', 'p(x)'])
    
    # Adiciona as colunas x e p(x) com linhas em branco
    for i in range(0, len(x)):
        # Adiciona a linha com valores reais de x e p(x)
        px[i] = round_floats(px[i])
        dados = pd.DataFrame({'x': [x[i]], 'p(x)': [px[i]]})
        # Convert to <class 'sympy.core.numbers.Float'> to <class 'float'>
        
        df = pd.concat([df, dados], ignore_index=True)
        
        # Adiciona uma linha em branco
        linha_branca = pd.DataFrame({'x': [''], 'p(x)': ['']})
        df = pd.concat([df, linha_branca], ignore_index=True)

    # Função para expandir os valores de difs e inseri-los corretamente
    def expandir_difs(difs_col, inicio):
        dif_expanded = []
        for i in range(len(difs_col)):
            # Insere valores vazios até o início desejado
            for j in range(inicio):
                dif_expanded.append('')

            difs_col[i] = round_floats(difs_col[i])
            dif_expanded.append(difs_col[i])
            inicio = 1  # Depois da primeira inserção, sempre pula 1 linha

        # Garante que a coluna tenha o mesmo tamanho que o DataFrame
        while len(dif_expanded) < len(df):
            dif_expanded.append('')
        
        return dif_expanded
    # Insere as colunas de diferenças começando nas respectivas linhas
    for idx, dif in enumerate(difs):
        dif_expanded = expandir_difs(dif, idx + 1)  # A primeira começa na linha 1, a segunda na 2, etc.
        df.insert(2 + idx, f'Dif_{idx+1}', dif_expanded, True)

    print(df.to_string(index=False))

def babbage(polinomio,x, valor_inicial, valor_final, padrao):
    valor_final += padrao
    grau = polinomio.degree()

    pxs = []
    difs = []
    # Dif_final representa a diferença que sempre repete
    dif_final = 0

    # A quantidade de diferenças é igual ao grau do polinômio
    for i in range(grau):
        difs.append([])


    j = 0
    stop = False
    # Calcula os valores de p(x) e as diferenças até achar a ultima diferença que é a diferença que repete
    for i in np.arange(valor_inicial, valor_final, padrao):
        if stop:
            j = i
            break
        # Pega o resultado de p(x)
        px = polinomio.subs(x, i)
        pxs.append(px)
        # Calcula a diferença se tiver valores de px para calcular
        if len(pxs) > 1:
            difs[0].append(pxs[-2] - pxs[-1])

        # Calcula as diferenças restantes
        if len(pxs) > 2:
            for k in range(0, grau):
                #Quando chega na ultima diferença que é a diferença que repete para o codigo e salva o valor
                if len(difs[-2]) > 1:
                    dif_final = difs[-2][-2] - difs[-2][-1]
                    difs[-1].append(dif_final)
                    stop = True
                    break
                if len(difs[k]) > 1:
                    difs[k+1].append(difs[k][-2] - difs[k][-1])

    # Segunda parte do calculo de babbage
    # A partir da ultima diferença, pega o valor anterior, e vai subtraindo as diferenças
    # Fazendo o caminho inverso da direita para a esquerda
    for i in np.arange(j, valor_final, padrao):
        difs[-1].append(dif_final)
        for k in range(grau-1, 0, -1):
            difs[k-1].append(difs[k-1][-1] - difs[k][-1]) 
        pxs.append(pxs[-1] - difs[0][-1])
        
    x = np.arange(valor_inicial, valor_final, padrao)
    mostra_tabela(x, pxs, difs)

def main():
    x = symbols('x')
    
    #Primeiro caso
    polinomio = poly( 2*x**2- 3*x + 2)
    babbage(polinomio, x, -3,4,1)
    #Segundo caso
    babbage(polinomio, x, 0.73,0.79,0.01)
    #Terceiro caso
    polinomio_2 = poly(2*x**3+ 3*x**2- 5*x + 2)
    babbage(polinomio_2, x, -1,2.5,0.5)  
    
if __name__ == '__main__':
    main()
