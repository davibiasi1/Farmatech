"""from utilidades import cab, pausa

# Importação dos comandos reais para dentro dos submenus
from comandos.cadastro import cadastrar_item
from comandos.carrinho import carrinho
from comandos.estoque import alterar_info, repor_est, desativar_item, descarte_lote, relatorio, repor_lote
from comandos.filtros import buscar, ordenar
from comandos.financeiro import promo, nota_f, painel_bi, exportar_txt


def menu_vend():
    while True:
        cab()
        print("\nMENU DE VENDAS")
        print("=-=" * 20)

        print("[ 1 ] Realizar uma Venda")
        print("[ 2 ] Consultar o Carrinho")
        print("[ 3 ] Cancelar Venda")
        print("[ 0 ] Voltar")

        opc = input("\n Escolha uma opção do menu: ").strip()

        if opc == "0":
            break
        elif opc == "1":
            # Chama a função real de venda e atualiza o processo
            carrinho() 
        elif opc == "2" or opc == "3":
            print("\nGerenciamento direto pelo módulo de carrinho.")
            pausa()
        else:
            print("\nOpção inválida!")
            pausa()


def menu_ctlg():  # Catalogo
    while True:
        cab()
        print("\nCATALOGO")
        print("=-=" * 20)

        print("[ 1 ] Exibir catalogo")
        print("[ 2 ] pesquisar por nome")
        print("[ 3 ] pesquisar por Laboratorio")
        print("[ 4 ] Ordenar por nome")
        print("[ 5 ] Ordenar por preço")
        print("[ 0 ] Voltar")

        opc = input("\n Escolha uma opção: ").strip()

        if opc == "0":
            break
        elif opc == "1":
            buscar()  # Exibe os itens sem filtro específico
        elif opc in ["2", "3"]:
            buscar()  # Aciona barramento de filtros de busca
        elif opc in ["4", "5"]:
            ordenar() # Chama o script de ordenação por nome ou preço
        else:
            print("\nOpção inválida!")
            pausa()


def menu_painel():
    while True:
        cab()
        print("\nVendas e faturamento")
        print("=-=" * 20)

        print("[ 1 ] Total de vendas")
        print("[ 2 ] Faturamento")
        print("[ 3 ] Mais vendidos")
        print("[ 4 ] Estoque baixo")
        print("[ 5 ] Lista de produtos ativos ou desativados")
        print("[ 0 ] Voltar")

        opc = input("\n Escolha uma opção do menu: ").strip()

        if opc == "0":
            break
        elif opc in ["1", "2", "3", "5"]:
            painel_bi()  # Estatísticas financeiras e BI
        elif opc == "4":
            relatorio()  # Verifica itens críticos no estoque
        else:
            print("\nOpção inválida!")
            pausa()


def menu_relat():
    while True:
        cab()
        print("\nRELATORIOS")
        print("=-=" * 20)

        print("[ 1 ] Relatorio de vendas ")
        print("[ 2 ] Relatorios de Estoque")
        print("[ 3 ] Relatorio de Remedios")
        print("[ 4 ] Exportar relatorio ")
        print("[ 0 ] Voltar")

        opc = input("\n Escolha uma opção do menu: ").strip()

        if opc == "0":
            break
        elif opc in ["1", "2", "3"]:
            relatorio()   # Puxa o relatório selecionado do banco
        elif opc == "4":
            exportar_txt() # Executa a exportação física do arquivo txt
        else:
            print("\nOpção inválida!")
            pausa()
"""