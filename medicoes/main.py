## Projeto desenvolvido por: Murilo Rezende Montano 11611ECP011 ##

from medicoes_diretas import MedicoesDiretas
from medicoes_indiretas import MedicoesIndiretas
from resources import *

def main():
    loop = True
    while loop:
        print("Escolha a opção desejada:")
        print("1 - Medição Direta.")
        print("2 - Medição Indireta.")
        print("3 - Encerrar execução.\n")

        opcao = input()

        print()

        if opcao == '1':
            MedicoesDiretas()
            
        elif opcao == '2':
            MedicoesIndiretas()

        elif opcao == '3':
            loop = False
            print("Execução encerrada.\n")
            
        else:
            print("Opção inválida!\n")


if __name__ == "__main__":
    main()
