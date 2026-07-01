import mysql.connector
from utilidades import conexao_bd
from utilidades import desativar_lote, itens_desativados

#Def para alterar as informações dos produtos/medicamentos
def alterar_info():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                          FARMATECH - ALTERAR DADOS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    while True:
        print("""
                           SELECIONE O TIPO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produtos Gerais      [2] Medicamentos
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        
        opcao = input("Digite uma opção(1, 2 ou 0 para voltar ao menu): ").strip()
        if opcao == '0':
            print("Voltando ao menu...")
            break
        elif opcao == '1':
            tabela = "produtos"
            tipo = "Produto"
        elif opcao == '2':
            tabela = "medicamentos"
            tipo = "Medicamento"
        else:
            print("ERRO: Opção inválida. Operação cancelada.")
            continue

        try:
            id_item = int(input(f"\nDigite o [ID] do {tipo.lower()}: "))
        except ValueError:
            print("ERRO: O [ID] deve ser um número inteiro.")
            continue
        
        try:
            # Conecta ao banco de dados
            conexao, cursor = conexao_bd()
            
            # Consulta o item em produtos
            if tabela == "produtos":
                cursor.execute("SELECT nome, tipo, marca, preco, qtd, validade FROM produtos WHERE id = %s AND ativo = 1", (id_item,))

            #consulta o item em medicamentos
            else:
                cursor.execute("SELECT nome, preco, qtd, lab, tarja, validade FROM medicamentos WHERE id = %s AND ativo = 1", (id_item,))
                
            item = cursor.fetchone()

            # Se não encontrar o item retorna ao início do loop
            if not item:
                print(f"ERRO: {tipo} não encontrado ou já desativado do sistema.")
                continue
            
            print(f"\nEditando {tipo.lower()}: {item[0]}")
            print("(Se não quiser alterar algum elemento, deixe em branco e aperte enter)")

            novo_nome = input(f"Alterar nome [{item[0]}] para: ").strip() or item[0]

            # ALtera a tabela produtos
            if tabela == "produtos":
        
                novo_tipo = input(f"Alterar tipo [{item[1]}] para: ").strip() or item[1]
                nova_marca = input(f"Alterar marca [{item[2]}] para: ").strip() or item[2]
                str_preco = input(f"Alterar preço [{item[3]}] para: ").strip()

                # validação do preco
                try:
                    novo_preco = float(str_preco) if str_preco else item[3]
                    if novo_preco < 0:
                        print("ERRO: O preço não pode ser um valor negativo. Alteração cancelada!")
                        continue
                except ValueError:
                    print("ERRO: O PREÇO PRECISA SER NUMÉRICO. Alteração cancelada!")
                    continue
                
                str_qtd = input(f"Alterar quantidade [{item[4]}] para: ").strip()

                #validação da quantidade
                try:
                    nova_qtd = int(str_qtd) if str_qtd else item[4]
                    if nova_qtd < 0:
                        print("ERRO: A quantidade não pode ser negativa.")
                        continue
                except ValueError:
                    print("ERRO: A QUANTIDADE PRECISA SER UM NÚMERO INTEIRO. Alteração cancelada!")
                    continue

                str_val = input(f"Alterar o ano de validade [{item[5]}] para: ").strip()

                #validação da validade
                try:
                    nova_val = int(str_val) if str_val else item[5]
                    if nova_val < 2026:
                        print("ERRO: PRODUTO VENCIDO.")
                        continue
                except ValueError:
                    print("ERRO: O ANO DE VALIDADE PRECISA SER UM NÚMERO INTEIRO. Alteração cancelada!")
                    continue

                #armazena o código sql na variável query
                query = """
                UPDATE produtos
                SET nome = %s, tipo = %s, marca = %s, preco = %s, qtd = %s, validade = %s
                WHERE id = %s
                """
                valores = (novo_nome, novo_tipo, nova_marca, novo_preco, nova_qtd, nova_val, id_item)

            # Altera a tabela medicamentos
            else:
                novo_lab = input(f"Alterar laboratório [{item[3]}] para: ").strip() or item[3]
                nova_tarja = input(f"Alterar tarja [{item[4]}] para: ").strip() or item[4]

                str_preco = input(f"Alterar preço [{item[1]}] para: ").strip()

                #validação do preço
                try:
                    novo_preco = float(str_preco) if str_preco else item[1]
                    if novo_preco < 0:
                        print("ERRO: O preço não pode ser um valor negativo. Alteração cancelada!")
                        continue
                except ValueError:
                    print("ERRO: O PREÇO PRECISA SER NUMÉRICO. Alteração cancelada!")
                    continue
                
                str_qtd = input(f"Alterar quantidade [{item[2]}] para: ").strip()

                #validação da quantidade
                try:
                    nova_qtd = int(str_qtd) if str_qtd else item[2]
                    if nova_qtd < 0:
                        print("ERRO: A quantidade não pode ser negativa.")
                        continue
                except ValueError:
                    print("ERRO: A QUANTIDADE PRECISA SER UM NÚMERO INTEIRO. Alteração cancelada!")
                    continue

                str_val = input(f"Alterar o ano de validade [{item[5]}] para: ").strip()

                #validação da validade
                try:
                    nova_val = int(str_val) if str_val else item[5]
                    if nova_val < 2026:
                        print("ERRO: PRODUTO VENCIDO.")
                        continue
                except ValueError:
                    print("ERRO: O ANO DE VALIDADE PRECISA SER UM NÚMERO INTEIRO. Alteração cancelada!")
                    continue

                #armazena o update da tabela medicamentos
                query = """
                UPDATE medicamentos
                SET nome = %s, preco = %s, qtd = %s, lab = %s, tarja = %s, validade = %s
                WHERE id = %s
                """
                valores = (novo_nome, novo_preco, nova_qtd, novo_lab, nova_tarja, nova_val, id_item)


            # Atualiza os valores
            cursor.execute(query, valores)
            conexao.commit()
            print(f"\n{tipo} alterado com sucesso!")
            break

        #medida de segurança caso de erro
        except mysql.connector.Error as erro:
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()
            print("\nERRO FATAL NO BANCO DE DADOS")
            print(f"Motivo técnico: {erro}")
            break

        #fecha o cursor e conexão para não destruir a minha RAM
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()




#Def para repor um só item
def repor_est():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                      FARMATECH - REPOR ESTOQUE
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    
    while True:
        print("""
                           SELECIONE O TIPO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produtos Gerais      [2] Medicamentos
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        #input do usuário
        opcao = input("Digite uma opção: ").strip()

        if opcao == '0':
            print("Voltando ao menu...")
            break
        
        elif opcao == '1':
            tabela = "produtos"
            tipo = "Produto"
        elif opcao == '2':
            tabela = "medicamentos"
            tipo = "Medicamento"
        else:
            print("ERRO: Opção inválida. Operação cancelada!")
            continue
        
        #input para digitar o ID, com validação usando o try/execpt
        try:
            id_item = int(input("\nDigite o [ID] do item: "))
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro.")
            continue
        
        try:
            #conecta ao banco de dados
            conexao, cursor = conexao_bd()

            cursor.execute(f"SELECT nome, qtd FROM {tabela} WHERE id = %s AND ativo = 1", (id_item,)) 
            item = cursor.fetchone()   

            #valida se o ID é inválido
            if not item:
                print(f"ERRO: {tipo} não encontrado com o ID informado.")
                continue

            #validação da quantidade
            try:
                qtd_repo = int(input(f"Quantas unidades de '{item[0]}' você deseja somar ao estoque? [Atual: {item[1]}]: "))
            except ValueError:
                print("ERRO: A quantidade deve ser um número inteiro.")
                continue

            #impede números menores que zero
            if qtd_repo <= 0:
                print("ERRO: A quantidade de reposição deve ser maior que zero.")

            #atualiza o banco de dados
            else:
                cursor.execute(f"UPDATE {tabela} SET qtd = qtd + %s WHERE id = %s AND ativo = 1", (qtd_repo, id_item))
                conexao.commit()
                print(f"\nEstoque de {tipo} atualizado com sucesso!")
                break

        #medida de segurança caso de erro
        except mysql.connector.Error as erro:
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()
            print("\nERRO FATAL NO BANCO DE DADOS")
            print(f"Motivo técnico: {erro}")
            break

        #encerra o cursor e conexao
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()

def repor_lote():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        FARMATECH - REPOR EM LOTE
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

    while True:# Mantém o menu ativo até finalizar a operação
        print("""
                           SELECIONE O TIPO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produtos Gerais      [2] Medicamentos
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

        opcao = input("Selecione uma opção: ").strip()

        if opcao == '0':
            print("Voltando ao menu...")
            break

        elif opcao == '1':# Seleciona a tabela conforme o tipo escolhido
            tabela = "produtos"
            tipo = "Produto"

        elif opcao == '2':
            tabela = "medicamentos"
            tipo = "Medicamento"

        else:
            print("ERRO: Opção inválida. Operação cancelada!!!")
            continue

        try:
            qtd_repo = int(input("Coloque a quantidade que deseja adicionar em cada item: "))

            if qtd_repo <= 0:
                print("A reposição aceita somente valores positivos.")
                continue

            entrada_ids = input("Digite os IDs dos itens do lote, separados por vírgula (ex: 1, 4, 7): ")

            if entrada_ids.strip() == "0":
                print("Operação cancelada. Voltando ao menu...")
                continue

            if not entrada_ids.strip():
                print("ERRO: Nenhum ID foi informado.")
                continue

            lista_ids = []# Armazena e valida os IDs informados
            ids_digitados = set()

            for id_item in entrada_ids.split(","):# Verifica se todos os IDs são válidos e únicos
                id_item = id_item.strip()

                if not id_item:
                    print("ERRO: Existem valores vazios na lista de IDs.")
                    lista_ids = []
                    break

                id_num = int(id_item)

                if id_num < 0:
                    print("ERRO: IDs não podem ser negativos.")
                    lista_ids = []
                    break

                if id_num in ids_digitados:
                    print(f"ERRO: O ID {id_num} foi informado mais de uma vez.")
                    lista_ids = []
                    break

                ids_digitados.add(id_num)
                lista_ids.append(id_num)

            if not lista_ids:
                continue

        except ValueError:
            print("Digite apenas números válidos!!!")
            continue

        try:
            conexao, cursor = conexao_bd()

            atualizados = 0

            for id_item in lista_ids:
                cursor.execute(f"SELECT nome, qtd FROM {tabela} WHERE id = %s AND ativo = 1", (id_item,))
                item = cursor.fetchone()

                if item:
                    cursor.execute(f"UPDATE {tabela} SET qtd = qtd + %s WHERE id = %s AND ativo = 1", (qtd_repo, id_item))
                    atualizados += 1
                    print(f"{tipo} '{item[0]}' atualizado")
                else:
                    print(f"ID {id_item} não encontrado ou inativo.")

            conexao.commit()

            if atualizados > 0:
                print("\nReposição em lote feita com sucesso!!!")
                break
            else:
                print("\nNenhum item foi atualizado.")#em caso de falha ao modificar os tabelas
                break

        except mysql.connector.Error as erro:

            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()

            print("\nERRO NO BANCO DE DADOS")
            print(f"Motivo técnico: {erro}")
            break

        finally:

            if 'cursor' in locals() and cursor is not None:
                cursor.close()

            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()

#Def para descarte em lote, usando args*, função 'desativar_lote' está em utilidades
def descarte_lote():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                      FARMATECH - DESCARTE DE LOTE
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    print("""
                           SELECIONE O TIPO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produtos Gerais      [2] Medicamentos
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    tabela = input("Digite uma opção: ").strip()
    
    if tabela == '0':
        return
    
    nome_tabela = "produtos" if tabela == '1' else "medicamentos"
    

    while True:
        entrada_ids = input("\nDigite os [IDs] dos itens vencidos separados por vírgula (ex: 1, 4, 7): ")
        
        try:
            # cconverte a entrada para uma lista de inteiros
            lista_ids = [int(numero.strip()) for numero in entrada_ids.split(',')]
            
            # Compara o tamanho da lista com o tamanho de um set (que ignora repetições)
            if len(lista_ids) != len(set(lista_ids)):
                print("ERRO: Você digitou IDs repetidos. Por favor, insira cada número apenas uma vez.")
                continue # Reinicia o loop, pedindo o input novamente
            
            # Se não houver erros, envia para a função e quebra o loop
            desativar_lote(nome_tabela, *lista_ids)
            break 
            
        except ValueError:
            print("ERRO DE DIGITAÇÃO: Certifique-se de digitar apenas números separados por vírgula.")
            # O loop continuará automaticamente e pedirá os dados novamente

#def para exibir relatórios        
def relatorio():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                          FARMATECH - RELATÓRIOS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    try:
        conexao, cursor = conexao_bd()

        #produtos com estoque baixo
        print("""
                            ALERTA DE ESTOQUE
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")  
        print("Produtos (menos que 5 unidades):")
        cursor.execute("SELECT nome FROM produtos WHERE qtd < 5 AND ativo = 1")
        prod_baixo = [linha[0] for linha in cursor.fetchall()]
        if not prod_baixo:
            print("Nenhum produto com estoque baixo.")
        else:
            print(",".join(prod_baixo))

        #medicamentos com estoque baixo
        print("\nMedicamentos em ALERTA DE ESTOQUE (menos que 5):")
        cursor.execute("SELECT nome FROM medicamentos WHERE qtd < 5 AND ativo = 1")
        med_baixo = [linha[0] for linha in cursor.fetchall()]
        if not med_baixo:
            print("Nenhum medicamento com estoque baixo.")
        else: 
            print(",".join(med_baixo))
        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                          ITENS ECONÔMICOS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        #medicamentos baratos
        print("\nMedicamentos abaixo de R$ 20,00: ")
        cursor.execute("SELECT nome FROM medicamentos WHERE preco <= 20.00 AND ativo = 1")
        med_barato =[linha[0] for linha in cursor.fetchall()]
        if not med_barato:
            print("Nenhum medicamento barato")
        else:
            print(",".join(med_barato))
        
        #produtos baratos
        print("\nProdutos abaixo de R$ 10,00: ")
        cursor.execute("SELECT nome FROM produtos WHERE preco <=10.00 AND ativo = 1")
        prod_barato = [linha[0] for linha in cursor.fetchall()]
        if not prod_barato:
            print("Nenhum produto barato")
        else:
            print(",".join(prod_barato))
    except mysql.connector.Error as erro:
        print(f"Motivo técnico: {erro}")
        print("Não foi possível gerar relatórios.")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()    
            




#def para desativar algum item do catálogo
def desativar_item():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                      FARMATECH - DESATIVAR ITEM
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    print("""
                           SELECIONE O TIPO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produtos Gerais      [2] Medicamentos
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    
    #input do usuário
    opcao = input("Digite uma opção: ").strip()
    
    if opcao == '1':
        tabela = "produtos"
        tipo = "Produto"
    elif opcao == '2':
        tabela = "medicamentos"
        tipo = "Medicamento"
    else:
        print("ERRO: Opção inválida. Operação cancelada.")
        return

    while True:
        try:
            id_item = int(input(f"\nDigite o [ID] do item (Ou 0 pra voltar ao menu): "))
        except ValueError:
            print("ERRO: O [ID] deve ser um número inteiro.")
            continue
        
        # Quebra o loop
        if id_item == 0:
            print("Operação cancelada. Voltando ao menu...")
            break

        try:
            conexao, cursor = conexao_bd()

            cursor.execute(f"SELECT nome FROM {tabela} WHERE id = %s AND ativo = 1", (id_item,))
            item = cursor.fetchone()

            #caso item esteja vazio, exibe mensagem de erro
            if not item:
                print(f"ERRO: {tipo} não encontrado ou já foi desativado.")
                continue

            print("(Digite 'N' pra cancelar e voltar ao menu)")
            confirmar = input(f"Tem certeza que deseja desativar '{item[0]}'? O histórico de vendas será mantido. (s/n): ").strip().lower()

            #sai do loop
            if confirmar == 'n':
                print("Operação cancelada. Voltando ao menu...")
                break

            
            elif confirmar == 's':
                cursor.execute(f"UPDATE {tabela} SET ativo = 0 WHERE id = %s", (id_item,))
                conexao.commit()
                print(f"\n{tipo} desativado do catálogo com sucesso!")
                break
            else:
                print("Opção inválida. Tente novamente.")
                continue

        except mysql.connector.Error as erro:
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()
            print("\nERRO FATAL NO BANCO DE DADOS")
            print(f"Motivo técnico: {erro}")
            break

        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()

def reativar_item():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                       FARMATECH - REATIVAR ITEM
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

    conexao, cursor = conexao_bd()

    # busca os itens desativados
    cursor.execute("SELECT id, nome, marca, tipo, preco, qtd FROM produtos WHERE ativo = 0")
    prod_desativados = cursor.fetchall()
    cursor.execute("SELECT id, nome, preco, qtd, lab, tarja FROM medicamentos WHERE ativo = 0")
    med_desativados = cursor.fetchall()

    # mostra os itens desativados
    itens_desativados(prod_desativados, med_desativados)

    # lógica para exibir esses itens
    if not prod_desativados and not med_desativados:
        print("Não há nenhum item desativado no momento para ser reativado.")
        return
    print("""
                           SELECIONE O TIPO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produtos Gerais      [2] Medicamentos
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    
    opcao = input("Digite uma opção: ").strip()
    
    if opcao == '1':
        tabela = "produtos"
        tipo = "Produto"
    elif opcao == '2':
        tabela = "medicamentos"
        tipo = "Medicamento"
    else:
        print("ERRO: Opção inválida. Operação cancelada.")
        return

    while True:
        try:
            id_item = int(input(f"\nDigite o [ID] do item (Ou 0 pra voltar ao menu): "))
        except ValueError:
            print("ERRO: O [ID] deve ser um número inteiro.")
            continue
        
        # Quebra o loop
        if id_item == 0:
            print("Operação cancelada. Voltando ao menu...")
            break

        try:
            conexao, cursor = conexao_bd()

            cursor.execute(f"SELECT nome FROM {tabela} WHERE id = %s AND ativo = 0", (id_item,))
            item = cursor.fetchone()

            if not item:
                print(f"ERRO: {tipo} não encontrado.")
                continue

            print("(Digite 'N' pra cancelar e voltar ao menu)")
            confirmar = input(f"Tem certeza que deseja reativar '{item[0]}'? (s/n): ").strip().lower()

            if confirmar == 'n':
                print("Operação cancelada. Voltando ao menu...")
                break

            elif confirmar == 's':
                cursor.execute(f"UPDATE {tabela} SET ativo = 1 WHERE id = %s", (id_item,))
                conexao.commit()
                print(f"\n{tipo} reativado ao catálogo com sucesso!")
                break
            else:
                print("Opção inválida. Tente novamente.")
                continue

        except mysql.connector.Error as erro:
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()
            print("\nERRO FATAL NO BANCO DE DADOS")
            print(f"Motivo técnico: {erro}")
            break

        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()
    





# def para alterar preço
def alterar_preco():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        FARMATECH - ALTERAR PREÇO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    
    # Abre o loop
    while True: 
        print("""
                           SELECIONE O TIPO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produtos Gerais      [2] Medicamentos
      -----------------------------------------------------------------
                          [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        
        opcao = input("Digite uma opção: ").strip()
        
        if opcao == '0':
            print("Operação cancelada. Voltando ao menu principal...")
            break # volta ao menu principal
            
        if opcao == '1':
            tabela = "produtos"
            tipo = "Produto"
        elif opcao == '2':
            tabela = "medicamentos"
            tipo = "Medicamento"
        else:
            print("ERRO: Opção inválida. Tente novamente.")
            continue # trocado pelo return, paraa respeitar o while true

        try:
            id_item = int(input(f"\nDigite o [ID] do {tipo.lower()} (ou 0 para cancelar): "))
            if id_item == 0:
                continue
        except ValueError:
            print("ERRO: O [ID] deve ser um número inteiro. Tente novamente.")
            continue
        
        try:
            conexao, cursor = conexao_bd()
            
            cursor.execute(f"SELECT preco FROM {tabela} WHERE id = %s AND ativo = 1", (id_item,))
            item = cursor.fetchone()

            if not item:
                print(f"ERRO: {tipo} não encontrado ou já desativado do sistema. Tente novamente.")
                continue
            
            str_preco = input(f"Alterar preço [R$ {item[0]:.2f}] para: ").strip()

            try:
                novo_preco = float(str_preco) if str_preco else item[0]
                if novo_preco < 0:
                    print("ERRO: O preço não pode ser um valor negativo. Tente novamente!")
                    continue
            except ValueError:
                print("ERRO: O PREÇO PRECISA SER NUMÉRICO (use ponto). Tente novamente!")
                continue
            
            query = f"UPDATE {tabela} SET preco = %s WHERE id = %s"
            valores = (novo_preco, id_item)

            # Atualiza o banco de dados
            cursor.execute(query, valores)
            conexao.commit()
            print(f"\nSucesso! Preço do {tipo.lower()} atualizado para R$ {novo_preco:.2f}!")
            
            break #volta ao menu principal

        except mysql.connector.Error as erro:
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()
            print("\nERRO FATAL NO BANCO DE DADOS")
            print(f"Motivo técnico: {erro}")
            break # sai do loop caso de erro

        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()