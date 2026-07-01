import mysql.connector
# Importação do módulo de conexão centralizado criado por nós 
from utilidades import conexao_bd


def inicializar_banco():
    
    try:
        # Abre a conexão com o servidor MySQL e obtém o ponteiro de execução (cursor)
        conexao, cursor = conexao_bd()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                tipo VARCHAR(255) NOT NULL,
                marca VARCHAR(255) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                qtd INT NOT NULL,
                validade INT NOT NULL,
                ativo INT DEFAULT 1  
                )
             """)

        #Separada de produtos por possuir campos específicos de controle sanitário (lab e tarja)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicamentos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                qtd INT NOT NULL,
                lab VARCHAR(255) NOT NULL,
                tarja VARCHAR(20) NOT NULL,
                validade INT NOT NULL, 
                ativo INT DEFAULT 1
                )
        """)

       # Chave estrangeira ligando ao cadastro de produtos e medicamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (                    
                id INT PRIMARY KEY AUTO_INCREMENT,
                horario DATETIME NOT NULL,
                id_produto INT NULL,
                id_medicamento INT NULL,
                quantidade INT NOT NULL,
                valor_total DECIMAL(10, 2) NOT NULL,  
                FOREIGN KEY (id_produto) REFERENCES produtos (id),   
                FOREIGN KEY (id_medicamento) REFERENCES medicamentos (id)   

            )
        """)

          # Verifica se a tabela está completamente vazia antes de inserir, evitando duplicidade
        cursor.execute("SELECT COUNT(*) FROM produtos")
        
        if cursor.fetchone()[0] == 0:
            prod_inicial = [
                ("Pasta de dente", "Higiene", "Colgate", 10.00, 300, 2028),
                ("Sabonete", "Higiene", "Lux", 3.50, 500, 2026) ,

            ]

           # executemany: insere em lote com um único comando SQL
            cursor.executemany("""
                INSERT INTO produtos (nome, tipo, marca, preco, qtd, validade)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, prod_inicial)

        cursor.execute("SELECT COUNT(*) FROM medicamentos")
        
        if cursor.fetchone()[0] == 0:
            med_inicial = [
                ("Dipirona", 15.00, 500, "EMS", "Livre",2025),
                ("Amoxilina", 30.00 , 800, "Medley", "Vermelha", 2027) ,

            ]

            cursor.executemany("""
                INSERT INTO medicamentos (nome, preco, qtd, lab, tarja, validade)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, med_inicial)
            
        
        # Confirma e salva em definitivo todas as transações estruturais e dados inseridos no banco de dados
        conexao.commit()

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    
    # Encerramento seguro
    finally:

        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()