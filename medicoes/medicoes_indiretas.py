from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import math
from scipy import stats
import os.path
from resources import *

def MedicoesIndiretas():
    simbolos = []
    indicacaoMedia = []
    parametros = []

    try:
        funcao, variaveis, dados, incertezaPadrao, grausDeLiberdade = Entrada()
    except Exception:
        return "Não foi possível recuperar os dados.\n"

    for variavel in variaveis:
        simbolos.append(Symbol(variavel))

    for i in range(len(simbolos)):
        indicacaoMedia.append(sum(dados[i])/len(dados[i]))

        print("media(" + str(simbolos[i]) + "): " + str(indicacaoMedia[i]))
        print("u(" + str(simbolos[i]) + "): " + str(incertezaPadrao[i]))

        print()
        
        parametros.append((simbolos[i],indicacaoMedia[i]))

    resultadoCombinado = funcao.subs(parametros)
    incertezaCombinada = IncertezaCombinada(incertezaPadrao, funcao, simbolos, parametros, dados)
    grausDeLiberdadeEfetivos = GrausDeLiberdadeEfetivos(incertezaCombinada, resultadoCombinado, incertezaPadrao, indicacaoMedia, grausDeLiberdade)
    incertezaExpandida = IncertezaExpandida(incertezaCombinada, grausDeLiberdadeEfetivos)

    for i in range(len(simbolos)):
        PlotHistograma("Histograma das indicações para a variável " + str(simbolos[i]), dados[i])

    print("O resultado é: (" + str(resultadoCombinado) + "±" + str(incertezaExpandida) + ")\n")

def IncertezaCombinada(incertezaPadrao, funcao, simbolos, parametros, dados):
    somaDerivadaIncertezaQuadratica = 0
    somaDerivadaIncertezaCoeficiente = 0
        
    for i in range(len(simbolos)):
        derivada = diff(funcao, simbolos[i])
        resultadoDerivada = derivada.subs(parametros)

        somaDerivadaIncertezaQuadratica += (resultadoDerivada**2)*(incertezaPadrao[i]**2)

    if len(dados[0]) > 1:
        for i in range(len(simbolos)-1):
            j=i+1
            while j < len(simbolos):
                derivadaI = diff(funcao, simbolos[i])
                derivadaJ = diff(funcao, simbolos[j])

                resultadoDerivadaI = derivadaI.subs(parametros)
                resultadoDerivadaJ = derivadaJ.subs(parametros)

                somaDerivadaIncertezaCoeficiente += (
                                                    resultadoDerivadaI*
                                                    resultadoDerivadaJ*
                                                    incertezaPadrao[i]*
                                                    incertezaPadrao[j]*
                                                    Correlacao(dados[i], dados[j], len(dados[i])))

                j+=1
                
    uCombinada = (somaDerivadaIncertezaQuadratica+somaDerivadaIncertezaCoeficiente)**(1/2)

    return uCombinada

def GrausDeLiberdadeEfetivos(incertezaCombinada, resultadoCombinado, incertezaPadrao, indicacaoMedia, grausDeLiberdade):
    soma = 0
    
    for i in range(len(incertezaPadrao)):
        soma += ((incertezaPadrao[i]/indicacaoMedia[i])**4)/grausDeLiberdade[i]
        
    grausDeLiberdadeEfetivos = ((incertezaCombinada/resultadoCombinado)**4)/soma

    return math.floor(grausDeLiberdadeEfetivos)

def ParseEquacao(equacao):
    variaveis = []
    for char in equacao:
        if ord(char) >= 65 and ord(char) <= 122:
            variaveis.append(char)

    return variaveis

def Entrada():
    indicacoes = []
    coluna = []
    u = []
    v = []

    funcao = symbols('funcao', cls=Function)

    equacao = input("Informe a equação para a obtenção do resultado: ")
    funcao = parse_expr(equacao)
    
    print("Escolha a forma como deseja introduzir os valores das indicacoes:")
    print("1 - Entrada manual.")
    print("2 - Arquivo .csv.\n")

    opcaoEntrada = input()

    print()

    if opcaoEntrada == '1':
        variaveis = ParseEquacao(equacao)

        for i in range(len(variaveis)):
            coluna.append([])
        
        loop = True
        while loop:
            try:
                loop = False
                nIndicacoes = int(input("Informe a quantidade de valores a serem inseridos: "))
                print()
                if nIndicacoes <= 0:
                    raise ValueError()
            except ValueError:
                loop = True
                print("Quantidade inválida!\n")

        for i in range(nIndicacoes):
            for j in range(len(variaveis)):
                loop = True 
                while loop:
                    try:
                        indicacao = float(input("Informe a " + str(i+1) + "ª indicacao da variável " + variaveis[j] + ": "))
                        print()
                        if nIndicacoes == 1:
                            incertezaPadrao = float(input("Informe a incerteza-padrão da variável " + variaveis[j] + ": "))
                            print()
                            grauDeLiberdade = int(input("Informe o grau de liberdade da variável " + variaveis[j] + ": "))
                            print()
                            v.append(grauDeLiberdade)
                            u.append(incertezaPadrao)
                        coluna[j].append(indicacao)
                        loop = False
                    except ValueError:
                        print("Valor incorreto!\n")

        dados = coluna

    elif opcaoEntrada == '2':
        arquivo = input("Informe o caminha para o arquivo .csv desejado: ")
        print()

        dados = RecuperarDados(arquivo)

        if dados is None:
            return None

        if len(dados) < 2 or len(dados[1][0]) <= 0:
            print("Faltam informações no arquivo.\n")
            return None

        variaveis = dados[0]

        dados = dados[1]
        
        if len(set(variaveis).intersection(ParseEquacao(equacao))) != len(variaveis):
            print("Desculpe, não foi possível continuar a execução. A equação deve conter as mesmas vairáveis que o arquivo informado.")
            return None

        for i in range(len(variaveis)):
            v.append(len(dados[i]))
            incertezaPadrao = IncertezaPadrao(indicacoes=dados[i],nIndicacoes=len(dados))
            u.append(incertezaPadrao)
        
    else:
        print("Opção invalida!\n")
        return None

    return funcao, variaveis, dados, u, v
