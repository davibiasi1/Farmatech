import mysql.connector
from utilidades import conexao_bd

def buscar():
    while True:
        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                           FARMATECH - BUSCA
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        print("""
                           SELECIONE O TIPO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produtos Gerais      [2] Medicamentos
                [3] Busca integrada
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
         # VALIDAÇÃO: Garante que o usuário digite apenas números, evitando que o Python quebre (Crash)
        try:
            escolha = int(input("Digite uma opção: "))
        except ValueError:
            print("ERRO: Opção deve ser um número inteiro (0, 1 ,2 ou 3) e não deve estar vazio.")
            print("-" * 50)
            continue

        # MECANISMO DE SEGURANÇA: Confirmação de saída para melhorar a experiência do usuário
        if escolha == 0:
            confirmar = input("Tem certeza que deseja sair do módulo de busca ? (S/N) ").strip().upper()
            if confirmar == "S":
                print("Voltando ao menu...")
                break  # Sai do loop while
            else:
                print("Operação cancelada. Continuando no catálogo...")
                continue 

        # FILTRO DE OPÇÕES INTERNAS: Bloqueia números fora do escopo (ex: se digitar 5)
        if escolha not in [1, 2, 3]:
            print("ERRO: Opção inválida! Escolha um número de 0 a 3.")
            continue

        # CAPTURA DO TERMO: O .strip() remove espaços inúteis e .lower() padroniza para a busca SQL
        termo = input("Digite o nome, marca/laboratório, tipo ou tarja que procura: ").strip().lower()

        # 1. Não permite buscas vazia 
        if not termo: 
            print("Busca cancelada. O termo não pode estar vazio.")
            continue 
            
       #Exige que tenha pelo menos 2 caracters para busca
        elif len(termo) < 2:
            print("Por favor, digite pelo menos 2 caracteres para realizar a busca.")
            continue

        #INTERAÇÃO COM O BLOCO DE MYSQL 
        try:
            conexao, cursor = conexao_bd() 

            # BUSCA EM PRODUTOS, EX: PROTETOR SOLAR, SABONETE
            if escolha == 1:
                cursor.execute("""
                    SELECT id, nome, tipo, marca, preco, qtd
                    FROM produtos
                    WHERE ativo = 1 AND (LOWER(nome) LIKE %s OR LOWER(tipo) LIKE %s OR LOWER(marca) LIKE %s)
                    ORDER BY tipo ASC, nome ASC
                """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

                resultados = cursor.fetchall()

                #Tratamento de retorno vazio
                if len(resultados) == 0:
                    print("Nenhum produto encontrado.")
                else:
                    print(f"\n {len(resultados)} produto(s) encontrado(s):")
                    print("=" * 80)

                    # Formatação de string avançada (:^3, :<25) para exibir os dados alinhados como tabela no terminal
                    for item in resultados: 
                        id, nome, tipo, marca, preco, qtd = item
                        print(f"     [{id:^3}] {nome:<25} │ R$ {preco:<6.2f} │ Estoque: {qtd:<3} un. │ Categoria: {tipo} │ Marca: {marca}")
                    print("=" * 80)

            # BUSCA EM MEDICAMENTOS 
            elif escolha == 2:
                cursor.execute("""
                    SELECT id, nome, preco, qtd, tarja, lab
                    FROM medicamentos
                    WHERE ativo = 1 AND (LOWER(nome) LIKE %s OR LOWER(lab) LIKE %s OR LOWER(tarja) LIKE %s)
                    ORDER BY tarja ASC, nome ASC
                """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

                resultados = cursor.fetchall()

                if len(resultados) == 0:
                    print("Nenhum medicamento encontrado.")
                else: 
                    print(f"\n{len(resultados)} medicamento(s) encontrado(s):")
                    print("=" * 80)
                    
                    for item in resultados: 
                        id, nome, preco, qtd, tarja, lab = item
                        print(f" [{id:^3}] {nome:<25} │ R$ {preco:<6.2f} │ Estoque: {qtd:<3} un. │ Tarja: {tarja:<10} │ Lab: {lab}")
                    print("=" * 80)

            #BUSCA DE MEDICAMENTOS E PRODUTOS
            elif escolha == 3:
                cursor.execute("""
                    SELECT 'Produto' AS origem, id, nome, preco, qtd, tipo AS detalhe_1, marca AS detalhe_2
                    FROM produtos
                    WHERE ativo = 1 AND (LOWER(nome) LIKE %s OR LOWER(tipo) LIKE %s OR LOWER(marca) LIKE %s)
                    
                    UNION ALL
                    
                    SELECT 'Medicamento' AS origem, id, nome, preco, qtd, tarja AS detalhe_1, lab AS detalhe_2
                    FROM medicamentos
                    WHERE ativo = 1 AND (LOWER(nome) LIKE %s OR LOWER(lab) LIKE %s OR LOWER(tarja) LIKE %s)
                    
                    ORDER BY origem ASC, nome ASC
                """, (f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%"))

                resultados = cursor.fetchall()

                if len(resultados) == 0:
                    print("Nenhum item encontrado em todo o catálogo.")
                else:
                    # Cabeçalho corrigido para não chamar tudo de medicamento
                    print(f"\n{len(resultados)} item(ns) encontrado(s):")
                    print("=" * 105)
                    
                    for item in resultados:
                        origem, id, nome, preco, qtd, d1, d2 = item
                        
                        # Formata as colunas finais dependendo de onde o item veio
                        if origem == 'Produto':
                            # d1 representa o tipo (Categoria) e d2 representa a marca
                            # <10 garante um espaçamento fixo à esquerda
                            detalhes = f"Categoria: {d1:<10} │ Marca: {d2}"
                        else:
                            detalhes = f"Tarja: {d1:<14} │ Lab: {d2}"
                            
                        print(f" [{origem:<11}] [{id:^3}] {nome:<22} │ R$ {preco:<6.2f} │ Estoque: {qtd:<3} un. │ {detalhes}")

        except mysql.connector.Error as erro:
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
            # Rollback: Se uma transação estivesse aberta e ocorresse um erro, desfazemos as alterações pendentes 
            # para garantir que o banco de dados não fique em um estado corrompido ou inconsistente.
            if 'conexao' in locals() and conexao.is_connected():
                    conexao.rollback()
            break


        # O finally garante o fechamento das conexões mesmo se ocorrer um erro no meio
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()


def ordenar():
    while True:
        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                          FARMATECH - FILTROS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        print("""
                          SELECIONE O CATÁLOGO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
               [1] Produtos Gerais        [2] Medicamentos
               [3] Catálogo Integrado
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

        #Garante que entradas inválidas (letras ou vazio) 
        # não quebrem o programa
        try: 
            cat_escolha = int(input("Deseja visualizar qual categoria? ").strip())
        except ValueError:
            print("ERRO: Opção deve ser um número inteiro (0, 1, 2 ou 3).")
            print("-" * 50)
            continue
            
        if cat_escolha == 0 :
            break

        if cat_escolha not in [1, 2, 3]:
            print("Opção inválida!")
            continue



        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                          VISUALIZAR CATÁLOGO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
          [1] Ordem Alfabética (A-Z)        [5] Próximos do Vencimento
          [2] Mais Baratos Primeiro         [6] Estoque Baixo (< 10)
          [3] Mais Caros Primeiro           [7] Vencendo em 2026
          [4] Maior Estoque Primeiro
     -----------------------------------------------------------------
                              [0] Voltar
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

        try: 

            comando_int = input("Escolha o metodo de organização desejada: ").strip()
        except ValueError:
             print("ERRO: Opção deve ser um número inteiro entre 0 e 7 e não deve estar vazio .")
             continue

        if comando_int == "0":
            confirmar = input("Tem certeza que deseja voltar ao menu? (S/N) ").strip().upper()
            if confirmar == "S":
                print("Voltando ao menu...")
                break
            else:
                print("Operação cancelada. Continuando no catálogo...")
                continue

        if comando_int not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("Opção inválida! Selecione um número de 0 a 7.")
            continue

        # Padroniza as colunas de tabelas diferentes usando ALIAS (AS)
        # Isso permite mesclar os dados de Medicamentos e Produtos sob as mesmas colunas genéricas ('categoria' e 'marca')
        base_med = "SELECT id, nome, preco, qtd, tarja AS categoria, lab AS marca, validade FROM medicamentos WHERE ativo = 1"
        base_prod = "SELECT id, nome, preco, qtd, tipo AS categoria, marca, validade FROM produtos WHERE ativo = 1"


        # (ETAPA 1: Definição da tabela alvo / Origem dos dados)
        if cat_escolha == 1:
            tabela_alvo = f"({base_prod})"

        elif cat_escolha == 2:
            tabela_alvo = f"({base_med})"

        else:
           # Une os resultados das duas tabelas em uma única visualização integrada
            tabela_alvo = f"({base_med} UNION ALL {base_prod})"


        # ETAPA 2: Aplicação dos filtros (WHERE) e ordenações (ORDER BY)
        filtro_where = ""
        ordenacao = ""

        if comando_int == "1":
            ordenacao = "ORDER BY LOWER(nome) ASC"
        elif comando_int == "2":
            ordenacao = "ORDER BY preco ASC"
        elif comando_int == "3":
            ordenacao = "ORDER BY preco DESC"
        elif comando_int == "4":
            ordenacao = "ORDER BY qtd DESC"
        elif comando_int == "5":
            ordenacao = "ORDER BY validade ASC"
        elif comando_int == "6":
            filtro_where = "WHERE qtd < 10"
            ordenacao = "ORDER BY qtd ASC"
        elif comando_int == "7":
            filtro_where = "WHERE validade = 2026"
            ordenacao = "ORDER BY LOWER(nome) ASC"

        # 4. Monta a query final com os blocos 
        query_base = f"SELECT * FROM {tabela_alvo} AS geral {filtro_where} {ordenacao}"
        try:
            conexao, cursor = conexao_bd()

            cursor.execute(query_base)
            estoque_ordenado = cursor.fetchall()

            if len(estoque_ordenado) == 0:
                print("Nenhum item atende aos critérios deste filtro.")
            else: 
                print(f"\n--- {len(estoque_ordenado)} item(ns) encontrado(s) ---")

                for item in estoque_ordenado:
                    # Regra de Negócio Visual: Alerta dinâmico de estoque crítico (< 10)
                    aviso_qtd = "BAIXO" if item[3] < 10 else "OK"
                    # Formatação Avançada de String: Alinhamento de colunas, centralização de IDs 
                    # e limitação de casas decimais para simular o comportamento de uma tabela de banco de dados no terminal
                    print(f"[{item[0]:^3}] {item[1]:<22} | R$ {item[2]:<6.2f} | Qtd: {item[3]:<3} ({aviso_qtd:<3}) | Validade: {item[6]} | Cat: {item[4]:<10} | Marca/Lab: {item[5]}")
                print("-" * 80)

        except mysql.connector.Error as erro:
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()
            break

        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()


