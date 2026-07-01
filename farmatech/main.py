import mysql.connector

from bd import inicializar_banco
from utilidades import conexao_bd
from utilidades import cab, pausa, desativar_lote
from interface import menu_princ

# Import dos comandos
from comandos.cadastro import cadastrar_item
from comandos.carrinho import carrinho
from comandos.estoque import alterar_info, repor_est, desativar_item, descarte_lote, relatorio, repor_lote, reativar_item, alterar_preco
from comandos.filtros import buscar, ordenar
from comandos.financeiro import promo, nota_f, painel_bi, exportar_txt

inicializar_banco()


while True:
    try:
        conexao, cursor = conexao_bd()
        
        # Busca do caixa
        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        result_caixa = cursor.fetchone()[0]
        caixa = result_caixa if result_caixa is not None else 0.0

        # Busca produtos
        cursor.execute("SELECT * FROM produtos WHERE ativo = 1")
        est_produtos = cursor.fetchall()
        
        # Busca medicamentos 
        cursor.execute("SELECT * FROM medicamentos WHERE ativo = 1")
        est_medicamentos = cursor.fetchall()
        
        # Junta tudo na mesma lista
        est = est_produtos + est_medicamentos

    except mysql.connector.Error as erro:
        print(f"ERRO DE CONEXÃO: {erro}")
        caixa = 0.0
        est = []
        
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

    # Puxa o menu da interface
    menu_princ(caixa, est_produtos, est_medicamentos)

    # Input para o usuário escolher o comando
    try:
        cmd = int(input("Digite o comando: "))
    except ValueError:
        print("ERRO: O COMANDO DEVE SER UM NÚMERO INTEIRO! ")
        input("Aperte ENTER para voltar ao menu...")
        continue

    # Quebra o laço
    if cmd == 0:
        print(f"Encerrando sistema. Total geral em caixa: R${caixa:.2f}")
        break

    elif cmd == 1:
        caixa = carrinho()

    elif cmd == 2:
        cadastrar_item()

    elif cmd == 3:
        alterar_info()

    elif cmd == 4:
        alterar_preco()

    elif cmd == 5:
        repor_est()

    elif cmd == 6:
        repor_lote()

    elif cmd == 7:
        buscar()

    elif cmd == 8:
        ordenar()

    elif cmd == 9:
        promo()

    elif cmd == 10:
        nota_f()
    
    elif cmd == 11:
        painel_bi()

    elif cmd == 12:
        relatorio()

    elif cmd == 13:
        desativar_item()

    elif cmd == 14:
        reativar_item()

    elif cmd == 15:
        descarte_lote()

    elif cmd == 16:
        exportar_txt()

    else:
        print("ERRO: COMANDO INEXISTENTE")
        input("Aperte ENTER para voltar ao menu...")
        continue

    # Bloco de pausa antes de voltar ao loop
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                      ENCERRAMENTO DO SISTEMA
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
             [1] Fechar sistema   [2] Voltar ao menu principal
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    try:
        resp = int(input("Digite sua opção: "))
        if resp == 1:
            print(f"Encerrando o sistema. Total geral em caixa: R$ {(caixa if caixa is not None else 0.0):.2f}")
            break
        elif resp == 2:
            continue
        else:
            print("ERRO: Resposta inválida!")
            input("Aperte ENTER para voltar ao menu...")
    except ValueError:
        print("ERRO: Resposta inválida!")
        input("Aperte ENTER para voltar ao menu...")
        pass
 