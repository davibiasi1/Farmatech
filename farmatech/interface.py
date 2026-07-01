def menu_princ(caixa_atual, est_prod, est_med):#busca os dados e a interface só mostra

    caixa_atual = caixa_atual or 0.0

    print(f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                             FARMATECH
                          Caixa: R$ {caixa_atual:.2f}
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

    print("PRODUTOS:\n")

    if not est_prod:#caso nn tenha produtos
        print("Nenhum produto encontrado.\n")
    else:
        for item in est_prod:
            print(
                f"[{item[0]}] {item[1]} ({item[3]})\n"
                f"    Marca: {item[2]} | R$ {item[4]:.2f} | Estoque: {item[5]}\n"
            )

    print("\nMEDICAMENTOS:\n")

    if not est_med:
        print("Nenhum medicamento encontrado.\n") #Esse bloco percorre os medicamentos do bd.
    else:
        for item in est_med:
            print(
                f"[{item[0]}] {item[1]}\n"
                f"    Laboratório: {item[4]} | Tarja: {item[5]}\n"
                f"    R$ {item[2]:.2f} | Estoque: {item[3]}\n"
            )

    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    print("""                       MENU DE OPÇÕES
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
   [0]  = Sair do Sistema              [9]  = Promoções
   [1]  = Carrinho de Compras          [10] = Nota Fiscal (Vendas)
   [2]  = Cadastrar Novo Item          [11] = Painel de Estatísticas (BI)
   [3]  = Editar Informações           [12] = Relatórios
   [4]  = Alterar Preço                [13] = Desativar Item
   [5]  = Repor Estoque Único          [14] = Reativar Item
   [6]  = Repor Estoque em Lote        [15] = Descartar Lote
   [7]  = Pesquisar Item               [16] = Exportar Relatório (TXT)
   [8]  = Visualizar Catálogo             
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")