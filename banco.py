
import sqlite3


def conectar():
    conexao = sqlite3.connect("sgf_industrial.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    # Tabela de empresas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cnpj TEXT,
            telefone TEXT,
            email TEXT
        )
    """)

    # Tabela de clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            documento TEXT,
            telefone TEXT,
            email TEXT,
            endereco TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
    """)

      # Tabela de produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            codigo TEXT NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT,
            preco_venda REAL DEFAULT 0,
            quantidade_estoque INTEGER DEFAULT 0,
            estoque_minimo INTEGER DEFAULT 0,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id),
            UNIQUE (empresa_id, codigo)
        )
    """)
    
    # Tabela de movimentações de estoque
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            motivo TEXT,
            data_movimentacao TEXT NOT NULL,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)


    # Atualização de produtos já cadastrados
    colunas_produtos = [
        coluna["name"]
        for coluna in cursor.execute("PRAGMA table_info(produtos)").fetchall()
    ]

    if "codigo" not in colunas_produtos:
        cursor.execute("ALTER TABLE produtos ADD COLUMN codigo TEXT")

    if "estoque_minimo" not in colunas_produtos:
        cursor.execute("""
            ALTER TABLE produtos
            ADD COLUMN estoque_minimo INTEGER DEFAULT 0
        """)
    # Tabela de equipamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            marca TEXT,
            modelo TEXT,
            numero_serie TEXT,
            tipo_gas TEXT,
            situacao TEXT DEFAULT 'Disponível',
            valor_diaria REAL DEFAULT 0,
            valor_semanal REAL DEFAULT 0,
            valor_mensal REAL DEFAULT 0,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
    """)
        # Tabela de locações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            cliente_id INTEGER NOT NULL,
            equipamento_id INTEGER NOT NULL,
            modalidade TEXT NOT NULL,
            data_retirada TEXT NOT NULL,
            data_prevista_devolucao TEXT NOT NULL,
            data_devolucao TEXT,
            valor REAL DEFAULT 0,
            situacao TEXT DEFAULT 'Ativa',
            observacoes TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
        )
    """)
        # Tabela de contas a receber
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas_receber (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            cliente_id INTEGER,
            locacao_id INTEGER,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data_emissao TEXT,
            data_vencimento TEXT NOT NULL,
            data_recebimento TEXT,
            situacao TEXT DEFAULT 'Pendente',
            observacoes TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (locacao_id) REFERENCES locacoes(id)
        )
    """)

    # Tabela de contas a pagar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas_pagar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT,
            fornecedor TEXT,
            valor REAL NOT NULL,
            data_emissao TEXT,
            data_vencimento TEXT NOT NULL,
            data_pagamento TEXT,
            situacao TEXT DEFAULT 'Pendente',
            observacoes TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
    """)
        # Tabela de contas a receber
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas_receber (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            cliente_id INTEGER,
            locacao_id INTEGER,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data_emissao TEXT,
            data_vencimento TEXT NOT NULL,
            data_recebimento TEXT,
            situacao TEXT DEFAULT 'Pendente',
            observacoes TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (locacao_id) REFERENCES locacoes(id)
        )
    """)

    # Tabela de contas a pagar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas_pagar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT,
            fornecedor TEXT,
            valor REAL NOT NULL,
            data_emissao TEXT,
            data_vencimento TEXT NOT NULL,
            data_pagamento TEXT,
            situacao TEXT DEFAULT 'Pendente',
            observacoes TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
    """)
    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados do SGF Industrial criado com sucesso!")
