import mysql.connector

def conexao_bd():
    conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="farmatech")
    cursor = conexao.cursor()
    return conexao,cursor

def entrada(mensagem, tipo=str, obrigatorio=True, condicao=None, erro_condicao="Valor inválido"):
    
    #Função genérica para pedir input com validação.
    
    while True:
        #mostra a mensagem e add a opção de voltar
        valor = input(mensagem + " (ou digite 0 para voltar ao menu): ").strip()

        # opção de voltar ao menu
        if valor == "0":
            confirmar = input("Tem certeza que deseja voltar ao menu? (S/N) ").strip().lower()
            if confirmar == "s":
                print("Voltando ao menu...")
                return None #sinaliza cancelamento
            else:
                print("Operação cancelada. Continuando...")
                continue #volta para pedir o campo novamente

        # validação de campo obrigatório
        if obrigatorio and not valor:
            print("Erro: este campo não pode ficar em branco.")
            continue
        if not valor and not obrigatorio:
            return None

        # conversão para tipo esperado (int, float..)
        try:
            valor = tipo(valor)
        except ValueError:
            print(f"Erro: digite um valor válido ({tipo.__name__}).")
            continue

        # validação de condição extra
        if condicao and not condicao(valor):
            print(erro_condicao)
            continue

        #se passou por todas as validações, retorna o valor
        return valor

def cab():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                              FARMATECH
                         Sistema Farmacêutico
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")

def pausa(): #para temporariamente o cod ate que o usuario aperte enter
    input("\nPressione ENTER para continuar... ")

def fechar_bd(cursor, conexao):#fecha o cursor e a conexao com o banco
    if cursor:
        cursor.close()
    if conexao and conexao.is_connected():
        conexao.close()

#Def que utiliza o *args, ela está referenciada na pasta estoque.py como 'descarte_lote
def desativar_lote(tabela, *ids_vencidos):
    try:
        conexao, cursor = conexao_bd()

        conexao.autocommit = False 
        
        # O *args 'ids_vencidos se comporta como uma tupla
        sucessos = 0
        for id_item in ids_vencidos:
            query = f"UPDATE {tabela} SET ativo = 0 WHERE id = %s"
            cursor.execute(query, (id_item,))
            
            # Conta se o ID existe
            if cursor.rowcount > 0:
                sucessos += 1

        conexao.commit()
        print(f"\nSUCESSO: {sucessos} itens foram desativados do catálogo na tabela '{tabela}'.")

    except mysql.connector.Error as erro:
        if 'conexao' in locals() and conexao.is_connected():
            conexao.rollback()
        print("\nERRO FATAL NO BANCO DE DADOS DURANTE O LOTE")
        print(f"Motivo técnico: {erro}")

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()




def itens_desativados(prod_desativados, med_desativados):

    print("PRODUTOS DESATIVADOS:\n")

    if not prod_desativados:#caso nn tenha produtos
        print("Nenhum produto encontrado.\n")
    else:
        for item in prod_desativados:
            print(
                f"[{item[0]}] {item[1]} ({item[3]})\n"
                f"    Marca: {item[2]} | R$ {item[4]:.2f} | Estoque: {item[5]}\n"
            )

    print("\nMEDICAMENTOS DESATIVADOS:\n")

    if not med_desativados:
        print("Nenhum medicamento encontrado.\n") #Esse bloco percorre os medicamentos do bd.
    else:
        for item in med_desativados:
            print(
                f"[{item[0]}] {item[1]}\n"
                f"    Laboratório: {item[4]} | Tarja: {item[5]}\n"
                f"    R$ {item[2]:.2f} | Estoque: {item[3]}\n"
            )

    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")