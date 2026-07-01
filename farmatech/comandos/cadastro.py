import mysql.connector
from utilidades import conexao_bd, entrada
from datetime import datetime

def cadastrar_item():
    while True: 
        #menu inicial de cadastro
        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                         FARMATECH - CADASTRO
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                         O QUE DESEJA CADASTRAR?
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                [1] Produto Geral      [2] Medicamento
     -----------------------------------------------------------------
                       [0] Voltar ao menu
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        escolha = input("Selecione uma opção: ").strip()

        #opção de voltar ao menu
        if escolha == "0":
            confirmar = input("Tem certeza que deseja voltar ao menu? (s/n)").strip().lower()
            if confirmar == "s":
                print("Voltando ao menu...")
                return
            else:
                print("Operação cancelada. Continuando no cadastro...")
                continue

        #validação da escolha
        if escolha not in ["1", "2"]:
            print("Opção inválida! Selecione 0, 1 ou 2. ")
            continue

        tipo_item = "produto" if escolha == "1" else "medicamento"
        print(f"\n---Cadastro de {tipo_item.capitalize()}---")

        try:
            conexao, cursor = conexao_bd()

            #campos básicos
            nome = entrada(f"Nome do {tipo_item}: ", str)
            if nome is None: break

            preco = entrada("Preço de venda: ", float, condicao=lambda x: x > 0, erro_condicao="O preço deve ser maior que zero.")
            if preco is None: break

            qtd = entrada("Quantidade inicial do estoque: ", int, condicao=lambda x: x >= 0, erro_condicao="A quantidade não pode ser negativa.")
            if qtd is None: break

            validade = entrada("Data de validade (AAAA): ", int, condicao=lambda x: x >= datetime.now().year, erro_condicao="O ano de validade não pode ser anterior ao atual.")
            if validade is None: break

            tabela = "produtos" if tipo_item == "produto" else "medicamentos"

            #cadastro de produto
            if tipo_item == "produto":
                tipo = entrada("Qual o tipo de produto? (ex: Higiene) ", str)
                if tipo is None: break

                marca = entrada("Qual a marca do produto? ", str)
                if marca is None: break

                #verifica duplicidade
                cursor.execute(f"SELECT ativo FROM {tabela} WHERE nome=%s AND marca=%s", (nome, marca))
                resultado = cursor.fetchone()
                if resultado:
                    print(f"Erro: Produto '{nome}' da marca '{marca}' já existe.")
                    break

                #insere no banco
                cursor.execute("""
                    INSERT INTO produtos (nome, tipo, marca, preco, qtd, validade)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nome, tipo, marca, preco, qtd, validade))
           
            #cadastro de medicamento
            else: 
                lab = entrada("Laboratório fabricante: ", str)
                if lab is None: break

                tarja = entrada("Tarja do medicamento (ex: vermelha, preta, amarela, livre) ", str).lower()
                if tarja is None: break

                #lista de tarjas válidas
                tarjas_validas = ["preta", "vermelha", "amarela", "livre"]
                
                #validação da tarja
                if tarja not in tarjas_validas:
                    print(f"Erro: A tarja '{tarja}' não existe. Use apenas: {', '.join(tarjas_validas)}.")
                    break

                #aviso para tarjas controladas
                if tarja in ["preta", "vermelha"]:
                    print(f"Atenção: Medicamento de tarja {tarja.upper()} cadastrado. Venda somente com receita médica!")

                #verifica duplicidade
                cursor.execute(f"SELECT ativo FROM {tabela} WHERE nome=%s AND lab=%s", (nome, lab))
                resultado = cursor.fetchone()
                if resultado:
                    print(f"Erro: Medicamento '{nome}' já existe.")
                    break

                #insere no banco
                cursor.execute("""
                    INSERT INTO medicamentos (nome, preco, qtd, lab, tarja, validade)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nome, preco, qtd, lab, tarja, validade))

            conexao.commit()
            print(f"\nSucesso! {tipo_item.capitalize()} cadastrado com sucesso!")

        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"Motivo técnico: {erro}")
            print(f"Falha ao cadastrar {tipo_item}.")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

        #saí do loop após um cadastro ou um cancelamento
        break