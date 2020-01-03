import csv
import os.path
from scipy import stats
import matplotlib.pyplot as plt

def ProbabilidadeDeAbrangencia():
    try:
        probabilidadeDeAbrangencia = float(input("Informe a probabilidade de abrangência(0 a 1) desejada: "))
        print()
        if probabilidadeDeAbrangencia > 1 or probabilidadeDeAbrangencia < 0:
            raise ValueError()
    except ValueError:
        print("Probabilidade inválida! O valor 0.975 será adotado.\n")
        probabilidadeDeAbrangencia = 0.975

    return probabilidadeDeAbrangencia

def RecuperarDados(arquivo):
    dados = []

    if os.path.isfile(arquivo) == False:
        print ("Desculpe, não foi possível encontrar o arquivo escolhido.\n")
        return None
    
    with open(arquivo) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=';')        

        coluna = []
        firstLine = True
        for row in csvReader:
            if firstLine:
                variaveisCSV = row

                firstLine = False
                for i in range(len(variaveisCSV)):
                    coluna.append([])
            else:
                try:
                    for i in range(len(variaveisCSV)):
                        coluna[i].append(float(row[i]))
                except ValueError:
                    print("Dados inconsistentes! Por favor verifique o arquivo de medições informado.")
                    return None

        return [variaveisCSV, coluna]

def IncertezaPadrao(**args):
    if "indicacoes" in args and "nIndicacoes" in args:
        somatorio = 0
        indicacaoMedia = sum(args['indicacoes'])/len(args['indicacoes'])
        for i in range(args['nIndicacoes']):
            somatorio += ((args['indicacoes'][i] - indicacaoMedia)**2)

        return ((somatorio/(args['nIndicacoes']-1))**(1/2))

    else:
        loop = True
        while loop:
            try:
                loop = False
                incertezaPadrao = float(input("Informe o valor da incerteza-padrão do sistema de medição utilizado: "))
                print()
                return incertezaPadrao
            except ValueError:
                loop = True
                print("Incerteza-padrão inválida!\n")

def Correcao(**args):
    if "vv" in args and "iMedia" in args:
        return args['vv'] - args['iMedia']
    
    else:
        loop = True
        while loop:
            try:
                loop = False
                correcao = float(input("Informe o valor de correção do sistema de medição utilizado: "))
                print()
                return correcao
            except ValueError:
                loop = True
                print("Correção inválida!\n")

def Precisao(**args):
    if "probabilidade" in args and "n" in args and "i" in args:
        coeficienteStudent = stats.t.ppf(args['probabilidade'], int(args['n']-1))
        incertezaPadrao = IncertezaPadrao(indicacoes=args['i'], nIndicacoes=args['n'])        
        return coeficienteStudent * incertezaPadrao

    else:
        loop = True
        while loop:
            try:
                loop = False
                precisao = float(input("Informe o valor de precisão do sistema de medição utilizado: "))
                print()
                return precisao
            except ValueError:
                loop = True
                print("Precisão inválida!\n")

def Correlacao(valoresX, valoresY, nIndicacoes):
    covarianca = 0
    desvioPadraoX = 0
    desvioPadraoY = 0
    
    xmedia = sum(valoresX)/len(valoresX)
    ymedia = sum(valoresY)/len(valoresY)
    
    for i in  range(nIndicacoes):
        covarianca += ((valoresX[i]-xmedia)*(valoresY[i]-ymedia))
        desvioPadraoX += ((valoresX[i]-xmedia)**2)
        desvioPadraoY += ((valoresY[i]-ymedia)**2)

    coeficienteDeCorrelacao = covarianca/((desvioPadraoX * desvioPadraoY)**(1/2))

    return coeficienteDeCorrelacao

def IncertezaExpandida(incertezaPadrão, vEfetivo):
    probabilidadeDeAbrangencia = ProbabilidadeDeAbrangencia();
    coeficienteStudent = stats.t.ppf(probabilidadeDeAbrangencia, int(vEfetivo))
    incertezaExpandida = incertezaPadrão * coeficienteStudent

    return incertezaExpandida

def PlotHistograma(titulo, medicoes):
    plt.hist(medicoes)
    plt.title(titulo)
    plt.grid()
    plt.show()
