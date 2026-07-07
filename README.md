# 💊 Farmatech - Sistema de Gestão Farmacêutica

Um sistema de terminal robusto para gestão completa de uma farmácia, desenvolvido em Python com persistência em MySQL. Este projeto simula operações reais de negócio com foco extremo em **integridade de dados**, **resiliência a falhas** e **arquitetura limpa**.

## 🚀 Principais Funcionalidades

- **🛒 PDV e Carrinho de Compras:** Motor de vendas com validação de estoque em tempo real. Inclui travas de segurança operacionais (ex: exigência de CRM para medicamentos de tarja vermelha/preta).
- **📦 Catálogo Dinâmico (CRUD):** Gestão de 'Produtos Gerais' e 'Medicamentos' com buscas otimizadas e ordenação avançada.
- **🛡️ Sistema de Soft Delete:** Exclusão lógica de itens do catálogo, mantendo a integridade do histórico de vendas e permitindo reativação futura.
- **🔄 Operações em Lote:** Reposição de estoque e descarte de itens vencidos utilizando desempacotamento dinâmico de parâmetros (`*args`).
- **💰 Painel de Promoções:** Aplicação de descontos dinâmicos por item específico ou categorias inteiras de forma simultânea.
- **📊 Business Intelligence (BI):** Painel de estatísticas gerenciais e exportação automatizada de relatórios de fechamento de caixa em `.txt`.

## 🧠 Arquitetura e Boas Práticas (Destaques Técnicos)

Este projeto não é apenas um sistema funcional, mas uma demonstração de boas práticas de engenharia de software:

* **Separação de Responsabilidades (Modularização):** O código é fisicamente dividido. Arquivos de interface (menus e inputs) não se misturam com lógicas de banco de dados, respeitando padrões de arquitetura de software.
* **Transações Blindadas (ACID):** Operações que afetam múltiplas tabelas (como registrar uma venda e abater o estoque) são protegidas por `COMMIT` e `ROLLBACK`, evitando corrupção de dados caso o servidor caia no meio do processo.
* **Prevenção contra SQL Injection:** Uso estrito de *Prepared Statements* (marcadores `%s`) em todas as queries.
* **Resiliência Extrema:** Tratamento agressivo de exceções via blocos `try/except/finally`. O sistema é imune a falhas de digitação do usuário e gerencia conexões e cursores do banco de forma segura para evitar vazamento de memória.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Banco de Dados:** MySQL
* **Bibliotecas:** `mysql-connector-python`, `datetime`

---

## 👥 Desenvolvedores - Grupo 5

Este projeto foi desenvolvido pelos seguintes responsáveis:

* Davi Dória Biasi
* Maria Eduarda Vieira
* Christopher Magalhães
* Leticia Santos Joffre
* Jessica Borges
