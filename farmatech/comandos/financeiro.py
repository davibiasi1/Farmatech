import mysql.connector
from datetime import datetime
from utilidades import conexao_bd, fechar_bd


def promo():
    while True:
        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                          FARMATECH - PROMOÇÕES
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

        print("""
                      COMO DESEJA APLICAR O DESCONTO?
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            [1] Um item específico      [2] Uma categoria inteira
      -----------------------------------------------------------------
                         [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        
        try:
            opcao = int(input("Selecione uma opção:  "))
        except ValueError:
            print("ERRO: O tipo de promoção deve ser um número inteiro!")
            continue
        
    #Opção 1 --- Desconto em um item especifico ---
        if opcao == 0:
            print("Voltando ao menu principal...")
            break

        elif opcao == 1:
            print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                         ONDE APLICAR O DESCONTO?
     -----------------------------------------------------------------
                  [1] Produtos Gerais     [2] Medicamentos
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
            tipo = input("Escolha a categoria: ").strip()

            if tipo not in ["1", "2"]:
                print("ERRO: Categoria inválida.")
                continue
            
            tabela = "produtos" if tipo == "1" else "medicamentos"

            try:
                porcent = float(input("Qual a porcentagem (%) do desconto? Digite em número inteiro (Exemplo: 10) "))
                
                if porcent <= 0 or porcent > 100:
                    print("ERRO: A porcentagem deve ser maior que 0% e menor ou igual a 100%.")
                    continue

                id_item = int(input(f"Digite o [ID] do {tabela[:-1]}: "))
            except ValueError:
                print("ERRO: Porcentagem e ID devem ser números válidos.")
                continue

            fator_desc = (100 - porcent) / 100

            conexao = None
            cursor = None
            
            try:
                conexao, cursor = conexao_bd()

                cursor.execute(f"SELECT nome FROM {tabela} WHERE id = %s AND ativo = 1", (id_item,))
                resultado = cursor.fetchone()

                if not resultado:
                    print("ERRO: Ese ID não existe no banco de dados ou o item está desativado.")
                    continue
                nome_item = resultado[0] #Para puxar o nome ao invés de id

                cursor.execute(
                    f"UPDATE {tabela} SET preco = ROUND(preco * %s, 2) WHERE id = %s AND ativo = 1",
                    (fator_desc, id_item),
                )
                conexao.commit()
                print(f"Desconto de {porcent}% Aplicado com sucesso no {tabela[:-1]} | '{nome_item}' ! ")
                break
            
            except mysql.connector.Error as erro:
                print(f"ERRO no banco: {erro}")
                break
            finally:
                fechar_bd(cursor, conexao)

        #Opção 2 ---Desconto em todos os itens ---
        elif opcao == 2:
            print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        DESCONTO EM TODOS OS ITENS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        [1] Apenas Medicamentos      [2] Apenas Produtos Gerais
        [3] Todos os itens da loja
     -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
            tipo = input("Escolha a opção: ").strip()

            if tipo not in ["1", "2", "3"]:
                print("ERRO: Opção Inválida. ")
                continue
            
            try:
                porcent = float(input("Digite a porcentagem (%) para aplicar de desconto: (Exemplo: 10) "))

                if porcent <= 0 or porcent > 100:
                    print("ERRO: A porcentagem de desconto deve ser maior que 0% e menor ou igual a 100%.")
                    continue
                
            except ValueError:
                print("ERRO: Porcentagem (%) inválida")
                continue

            fator_desc = (100 - porcent) / 100

            conexao = None
            cursor = None

            try: 
                conexao, cursor = conexao_bd()

                if tipo == "1":
                    cursor.execute("UPDATE medicamentos SET preco = ROUND(preco * %s, 2) WHERE ativo = 1", (fator_desc,))
                    print(f"Desconto de {porcent}% aplicado em TODOS os Medicamentos!")

                elif tipo == "2":
                    cursor.execute("UPDATE produtos SET preco = ROUND(preco * %s, 2) WHERE ativo = 1", (fator_desc,))
                    print(f"Desconto de {porcent}% aplicado em TODOS os Produtos!")

                elif tipo == "3":
                    cursor.execute("UPDATE medicamentos SET preco = ROUND(preco * %s, 2) WHERE ativo = 1", (fator_desc,))
                    cursor.execute("UPDATE produtos SET preco = ROUND(preco * %s, 2) WHERE ativo = 1", (fator_desc,))
                    print(f"SUCESSO! Desconto de {porcent}% aplicado em TUDO na farmácia!")
                

                conexao.commit()
                break

            except mysql.connector.Error as erro:
                conexao.rollback()
                print(f"ERRO no banco: {erro}")
                break
            finally:
                if 'cursor' in locals() and cursor is not None:
                    cursor.close()
                if 'conexao' in locals() and conexao.is_connected():
                    conexao.close()
            
        else:
            print("ERRO: Comando Inválido")


def nota_f():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                               NOTA FISCAL
                          VENDAS DA SESSÃO ATUAL
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    conexao = None
    cursor = None

    try:
        conexao, cursor = conexao_bd()

        #INNER JOIN para medicamentos e juntamos (UNION ALL) com o INNER JOIN de produtos
        cursor.execute("""
            SELECT vendas.id, vendas.horario, medicamentos.nome, vendas.quantidade, vendas.valor_total
            FROM vendas
            INNER JOIN medicamentos ON vendas.id_medicamento = medicamentos.id
            WHERE vendas.id_medicamento IS NOT NULL
            
            UNION ALL
            
            SELECT vendas.id, vendas.horario, produtos.nome, vendas.quantidade, vendas.valor_total
            FROM vendas
            INNER JOIN produtos ON vendas.id_produto = produtos.id
            WHERE vendas.id_produto IS NOT NULL
            
            ORDER BY horario DESC
        """)
        
        historico = cursor.fetchall()
        
        if len(historico) == 0:
            print("Não foi realizada nenhuma venda ainda.")
        else:
            for venda in historico:
                print(f"[{venda[0]}] Data/Hora: {venda[1]} | {venda[2]} x{venda[3]} | Total venda R$ {venda[4]:.2f}")
   
    except mysql.connector.Error as erro:
        print(f"Motivo tecnico: {erro}")
    
    finally:
        # Fecha o banco 
        fechar_bd(cursor, conexao)

def painel_bi():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                   FARMATECH - BUSINESS INTELLIGENCE (BI)
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    conexao = None
    cursor = None

    try:
        conexao, cursor = conexao_bd()

        cursor.execute("SELECT COUNT(*) FROM vendas")
        if cursor.fetchone()[0] == 0:
            print("Sem dados de vendas realizadas ainda.")
            return
        
        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        faturamento = cursor.fetchone()[0]
        print(f"Histórico de faturamento Bruto: R$ {faturamento:.2f}")

        cursor.execute("SELECT COUNT(DISTINCT id) FROM vendas")
        total_cupons = cursor.fetchone()[0]
        ticket_medio = faturamento / total_cupons if total_cupons > 0 else 0
        print(f"=-=-=-= Ticket Médio por cupom: R$ {ticket_medio:.2f} =-=-=-=")

        # COALESCE junta id_produto e id_medicamento para criar o ranking geral correto
        cursor.execute(""" 
            SELECT COALESCE(id_produto, id_medicamento) AS id_item, SUM(quantidade) AS total_vendido
            FROM vendas
            GROUP BY id_item
            ORDER BY total_vendido DESC
            LIMIT 1
        """)
        resultado_campeao = cursor.fetchone()

        if resultado_campeao:
            id_item, maior_qtd = resultado_campeao

            # Primeiro testa se esse ID campeão é da tabela de medicamentos
            cursor.execute("SELECT nome FROM medicamentos WHERE id = %s", (id_item,))
            res_nome = cursor.fetchone()

            if not res_nome:
                # Se não achar em medicamentos, busca na tabela de produtos
                cursor.execute("SELECT nome FROM produtos WHERE id = %s", (id_item,))
                res_nome = cursor.fetchone()

            nome_campeao = res_nome[0] if res_nome else "Item Desconhecido"

            print(f"-> ITEM MAIS VENDIDO GERAL: {nome_campeao} ({maior_qtd} unidades vendidas)")

    except mysql.connector.Error as erro:
        print(f"ERRO ao processar BI: {erro}")
    finally:
        fechar_bd(cursor, conexao)


def exportar_txt():
        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                      FARMATECH - EXPORTAR RELATÓRIO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        
        conexao = None
        cursor = None
    
        try:
            conexao, cursor = conexao_bd()

            cursor.execute("""
                SELECT id, horario, id_produto, id_medicamento, quantidade, valor_total
                FROM vendas
                ORDER BY id ASC
            """)

            vendas_banco = cursor.fetchall()

            if not vendas_banco:
                print("Nenhuma venda registrada.")
                return
            
            # Faturamento total cálculo
            cursor.execute("SELECT SUM(valor_total) FROM vendas")
            faturamento_total = cursor.fetchone()[0] or 0.0

            # Ticket médio cálculo
            cursor.execute("SELECT COUNT(DISTINCT id) FROM vendas")
            total_cupons = cursor.fetchone()[0] or 1
            ticket_medio = faturamento_total / total_cupons

            # 2 COALESCE unifica os IDs para descobrir o campeão geral real
            cursor.execute("""
                SELECT COALESCE(id_produto, id_medicamento) AS id_item, SUM(quantidade) AS qtd 
                FROM vendas 
                GROUP BY id_item 
                ORDER BY qtd DESC 
                LIMIT 1
            """)
            res_campeao = cursor.fetchone()
            id_campeao = res_campeao[0] if res_campeao else 0
            maior_qtd = res_campeao[1] if res_campeao else 0

            # Buscar o nome do campeão de vendas
            cursor.execute("SELECT nome FROM medicamentos WHERE id = %s", (id_campeao,))
            busca_nome = cursor.fetchone()
            if not busca_nome:
                cursor.execute("SELECT nome FROM produtos WHERE id = %s", (id_campeao,))
                busca_nome = cursor.fetchone()
            nome_campeao = busca_nome[0] if busca_nome else "Nenhum"

            data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"relatorio_farmatech_{data_atual}.txt"

            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("==========================================================\n")
                arquivo.write("FARMATECH - RELATÓRIO EXPORTADO DE VENDAS E ESTATÍSTICAS\n")
                arquivo.write("==========================================================\n")
                arquivo.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                arquivo.write("--------------------------------------------------------------\n")
                
                arquivo.write("1. HISTÓRICO FINANCEIRO (BI)\n")
                arquivo.write(f"Faturamento Bruto Total: R$ {faturamento_total:.2f}\n")
                arquivo.write(f"Total de Cupons Emitidos: {total_cupons} cupons\n")
                arquivo.write(f"Ticket Médio por Cupom:   R$ {ticket_medio:.2f}\n\n")
                
                arquivo.write("2. DESEMPENHO DE PRODUTOS\n")
                arquivo.write("------------------------------------------------------------\n")
                arquivo.write(f"Item Mais Vendido Geral: {nome_campeao} ({maior_qtd} unidades)\n\n")
                
                arquivo.write("3. DETALHAMENTO DE TODAS AS VENDAS\n")
                arquivo.write("------------------------------------------------------------\n")

                for venda in vendas_banco:
                    # 3 Desestruturando a tupla capturando as duas colunas novas
                    cupom, horario, id_prod, id_med, qtd, total = venda

                    # 4 Se id_med não for nulo, busca na tabela de medicamentos. Caso contrário, produtos.
                    if id_med is not None:
                        cursor.execute("SELECT nome FROM medicamentos WHERE id = %s", (id_med,))
                    else:
                        cursor.execute("SELECT nome FROM produtos WHERE id = %s", (id_prod,))
                    
                    res_nome = cursor.fetchone()
                    nome_item = res_nome[0] if res_nome else "Item não encontrado"


                    arquivo.write(f"| Cupom: {cupom:<5} | Data: {data_atual} | Produto: {nome_item:<20} | Qtd: {qtd:<3} | Total: R$ {total:.2f}\n")

                arquivo.write("\n------------------------------------------------------------\n")
                arquivo.write("FIM DO RELATÓRIO -  FARMATECH \n")
                arquivo.write("============================================================\n")

            # Mensagem movida para fora do bloco "with open" para garantir que o arquivo já fechou e salvou fisicamente
            print(f"Sucesso!! Relatório exportado com o nome '{nome_arquivo}'!")

        except Exception as erro_geral:
            print(f"ERRO: Ao tentar gerar arquivo no sistema: {erro_geral}")

        finally:
            fechar_bd(cursor, conexao)
        