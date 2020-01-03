from resources import *
from scipy import stats
import math

def MedicoesDiretas():
    print("Escolha o médoto de medição desejado:")
    print("1 - Com uma fonte de incerteza dominante.")
    print("2 - Com várias fontes de incerteza.\n")

    opcaoMetodo = input()

    print()

    if opcaoMetodo == '1':
        print(ResultadoIncertezaDominante())

    elif opcaoMetodo == '2':
        print(ResultadoMultiplasIncertezas())

    else:
        print("Opção inválida!\n")

def ResultadoIncertezaDominante():
    indicacoes = Entrada()

    if indicacoes is None:        
        return "Não foi possivel recuperar os dados.\n"

    nIndicacoes = len(indicacoes)
    indicacaoMedia = sum(indicacoes)/nIndicacoes

    print("Escolha o tipo do mensurando:")
    print("1 - Invariável.")
    print("2 - Variável.\n")

    opcaoMensurando = input()

    print()

    if nIndicacoes == 1:
        correcao = Correcao()
        precisao = Precisao()
        
    else:
        try:
            valorVerdadeiro = float(input("Informe o valor verdadeiro do mensurando utilizado: "))
            print()
        except ValueError:
            return "Valor inválido!\n"
        probabilidadeDeAbrangencia = ProbabilidadeDeAbrangencia();
        correcao = Correcao(vv=valorVerdadeiro, iMedia=indicacaoMedia)
        precisao = Precisao(probabilidade=probabilidadeDeAbrangencia, n=nIndicacoes, i=indicacoes)

    if opcaoMensurando == '1':
        print("Informe a forma desejada para o resultado:")
        print("1 - Com correção dos erros sistemáticos.")
        print("2 - Sem correção dos erros sistemáticos.\n")

        opcaoCorrecao = input()


        if opcaoCorrecao == '1':
            PlotHistograma("Histograma das indicações", indicacoes)
            return "O resultado é: (" + str(indicacaoMedia+correcao) + "±" + str((precisao)/(nIndicacoes**(1/2))) + ")\n"
            
        elif opcaoCorrecao == '2':
            PlotHistograma("Histograma das indicações", indicacoes)
            return "O resultado é: (" + str(indicacaoMedia) + "±" + str(abs(correcao)+precisao) + ")\n"
            
        else:
            return "Opção inválida!\n"
        
    elif opcaoMensurando == '2':
        if nIndicacoes == 1:
            print("Resultado assumindo que o valor informado é a média das medições.\n")

        print("Informe a forma desejada para o resultado:")
        print("1 - Com correção dos erros sistemáticos.")
        print("2 - Sem correção dos erros sistemáticos.\n")

        opcaoCorrecao = input()

        print()

        if opcaoCorrecao == '1':
            PlotHistograma("Histograma das indicações", indicacoes)
            return "O resultado é: (" + str(indicacaoMedia+correcao) + "±" + str(precisao) + ")\n"

        elif opcaoCorrecao == '2':
            PlotHistograma("Histograma das indicações", indicacoes)
            return "O resultado é: (" + str(indicacaoMedia) + "±" + str((abs(correcao)+precisao)+precisao) + ")\n"
        
        else:
            return "Opção inválida!"
    else:
        return "Opção inválida!"

def ResultadoMultiplasIncertezas():
    incertezaPadrao = []
    grausDeLiberdade = []
    
    indicacoes = Entrada()

    if indicacoes is None:        
        return "Não foi possivel recuperar os dados.\n"

    nIndicacoes = len(indicacoes)
    indicacaoMedia = sum(indicacoes)/nIndicacoes

    print("Escolha o tipo do mensurando:")
    print("1 - Invariável.")
    print("2 - Variável.\n")

    opcaoMensurando = input()

    print()

    if opcaoMensurando != '1' and opcaoMensurando != '2':
        return "Opção inválida!\n"

    if nIndicacoes == 1:
        correcao = Correcao()      
        incertezaPadrao.append(IncertezaPadrao())        
        try:
            grausDeLiberdade.append(int(input("Informe o grau de liberdade da medição informada: ")))
            print()
        except ValueError:
            return "Valor inválido!\n"
        
    else:
        try:
            valorVerdadeiro = float(input("Informe o valor verdadeiro do mensurando utilizado: "))
            print()
        except ValueError:
            return "Valor inválido!\n"
        correcao = Correcao(vv=valorVerdadeiro, iMedia=indicacaoMedia)

        if opcaoMensurando == '1':
            incertezaPadrao.append(IncertezaPadrao(indicacoes=indicacoes, nIndicacoes=nIndicacoes)/(nIndicacoes**(1/2)))
        else:
            incertezaPadrao.append(IncertezaPadrao(indicacoes=indicacoes, nIndicacoes=nIndicacoes))

        grausDeLiberdade.append(nIndicacoes-1)

    correcaoCombinada = correcao
    incertezaCombinadaQuadratica = incertezaPadrao[0]**2
    somaGrausEfetivos = ((incertezaPadrao[0]**4)/grausDeLiberdade[0])  

    try:
        nFontesIncerteza = int(input("Informe a quantidade fontes de incerteza além do sistema de medição: "))
        print()
        if nFontesIncerteza <= 0:
            raise ValueError()
    except ValueError:
        return "Quantidade inválida!\n"

    for i in range(nFontesIncerteza):
        try:
            correcaoCombinada += float(input("Informe a correção da " + str(i+1) + "ª fonte de incerteza: "))
            incertezaPadrao.append(float(input("Informe a incerteza-padrão da " + str(i+1) + "ª fonte de incerteza: ")))
            incertezaCombinadaQuadratica += (incertezaPadrao[i]**2)
            grausDeLiberdade.append(int(input("Informe o grau de liberdade usado na " + str(i+1) + "ª fonte de incerteza: ")))
            somaGrausEfetivos += ((incertezaPadrao[i]**4)/grausDeLiberdade[i])
            print()
        except ValueError:
            "Valor inválido!\n"

    probabilidadeDeAbrangencia = ProbabilidadeDeAbrangencia();

    incertezaCombinada = incertezaCombinadaQuadratica**(1/2)
    grausDeLiberdadeEfetivos = math.floor((incertezaCombinada**4)/(somaGrausEfetivos))
    coeficienteStudent = stats.t.ppf(probabilidadeDeAbrangencia, grausDeLiberdadeEfetivos)

    PlotHistograma("Histograma das indicações", indicacoes)
    return "O resultado é: (" + str(indicacaoMedia+correcaoCombinada) + "±" + str(incertezaCombinada*coeficienteStudent) + ")\n"

def Entrada():
    indicacoes = []
    
    print("Escolha a forma como deseja introduzir os valores das indicacoes:")
    print("1 - Entrada manual.")
    print("2 - Arquivo .csv.\n")

    opcaoEntrada = input()

    print()

    if opcaoEntrada == '1':
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
            loop = True
            while loop:
                try:   
                    indicacoes.append(float(input("Informe a " + str(i+1) + "ª indicacao: ")))
                    print()
                    loop = False
                except ValueError:
                    print("Valor de indicacao incorreto!\n")

    elif opcaoEntrada == '2':
        arquivo = input("Informe o caminho para o arquivo .csv desejado: ")
        print()
        
        dados = RecuperarDados(arquivo)

        if dados is None:
            return None

        if len(dados) < 2 or len(dados[1][0]) <= 0:
            print("Faltam informações no arquivo.\n")
            return None
        
        if len(dados[0]) > 1:
            print("Para medições diretas não podem haver mais de uma variável.\n")
            return None

        indicacoes = dados[1][0]
        
    else:
        print("Opção invalida!\n")
        return None

    return indicacoes
