
from flask import Flask, render_template_string, request, redirect, url_for
from banco import conectar, criar_tabelas
from datetime import date

app = Flask(__name__)

# Prepara o banco de dados
criar_tabelas()


# ==========================================
# CADASTRO E LISTAGEM DE CLIENTES
# ==========================================

@app.route("/clientes", methods=["GET", "POST"])
def clientes():

    if request.method == "POST":

        nome = request.form["nome"]
        documento = request.form["documento"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        endereco = request.form["endereco"]

        conexao = conectar()

        conexao.execute("""
            INSERT INTO clientes
            (empresa_id, nome, documento, telefone, email, endereco)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (1, nome, documento, telefone, email, endereco))

        conexao.commit()
        conexao.close()

        return redirect(url_for("clientes"))

    conexao = conectar()

    lista_clientes = conexao.execute("""
        SELECT * FROM clientes
        WHERE empresa_id = 1
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Clientes - SGF Industrial</title>
            <style>
    * {
        box-sizing: border-box;
    }

    body {
        font-family: Arial, sans-serif;
        background: #F1F4F9;
        color: #263445;
        margin: 0;
        padding: 30px;
    }

    .container {
        max-width: 1200px;
        margin: auto;
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 3px 12px rgba(20, 45, 75, 0.06);
    }

    h1 {
        color: #17365D;
        margin: 0 0 25px;
        font-size: 28px;
    }

    h2 {
        color: #17365D;
        margin: 0 0 20px;
        font-size: 20px;
    }

    label {
        font-size: 13px;
        font-weight: bold;
        color: #46566A;
    }

    input {
        display: block;
        width: 100%;
        padding: 12px;
        margin: 7px 0 18px;
        border: 1px solid #DCE3EC;
        border-radius: 7px;
        font-size: 14px;
    }

    input:focus {
        outline: none;
        border-color: #2864A5;
        box-shadow: 0 0 0 3px rgba(40, 100, 165, 0.10);
    }

    button {
        background: #17365D;
        color: white;
        padding: 13px 22px;
        border: none;
        border-radius: 7px;
        font-weight: bold;
        cursor: pointer;
        font-size: 14px;
    }

    button:hover {
        background: #245184;
    }

    hr {
        border: 0;
        border-top: 1px solid #DCE3EC;
        margin: 30px 0;
    }

    .cliente {
        background: #E2EAF3;
        padding: 18px;
        margin-bottom: 12px;
        border: 1px solid #C5D2E0;
        border-radius: 7px;
        font-size: 14px;
        line-height: 1.8;
        overflow-wrap: anywhere;
    }

    .cliente strong {
        color: #17365D;
        font-size: 16px;
    }

    a {
        color: #17365D;
        font-weight: bold;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    .cliente a {
        display: inline-block;
        margin: 10px 12px 0 0;
    }

    @media (max-width: 650px) {
        body {
            padding: 15px;
        }

        .container {
            padding: 18px;
        }

        h1 {
            font-size: 23px;
        }
    }
</style>
        </head>

        <body>
            <div class="container">

               <style>
    .form-clientes {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px;
    }

    .campo-cliente {
        display: flex;
        flex-direction: column;
        gap: 7px;
    }

    .campo-cliente input {
        margin: 0;
    }

    .campo-inteiro {
        grid-column: 1 / -1;
    }

    .descricao-clientes {
        color: #718096;
        font-size: 13px;
        margin: 0 0 22px;
    }

    .acoes-cadastro {
        margin-top: 22px;
    }

    @media (max-width: 650px) {
        .form-clientes {
            grid-template-columns: 1fr;
        }
    }
        /* Cabeçalho padronizado de Clientes */
    .topo-clientes {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 25px;
        background: #DCE7F3;
        padding: 22px;
        border-left: 5px solid #17365D;
        border-radius: 9px;
    }

    .topo-clientes h1 {
        color: #17365D;
        margin: 0 0 6px;
        font-size: 28px;
    }

    .topo-clientes .subtitulo {
        color: #718096;
        margin: 0;
        font-size: 14px;
    }

    .voltar-clientes {
        display: inline-block;
        background: #FFFFFF;
        color: #17365D;
        padding: 11px 17px;
        border: 1px solid #DCE3EC;
        border-radius: 7px;
        font-weight: bold;
        text-decoration: none;
    }

    .voltar-clientes:hover {
        background: #EAF0F7;
        text-decoration: none;
    }
</style>

<div class="topo-clientes">
    <div>
        <h1>Gestão de Clientes</h1>
        <p class="subtitulo">
            Gerencie o cadastro e as informações dos seus clientes.
        </p>
    </div>

    <a href="/" class="voltar-clientes">← Voltar ao painel</a>
</div>

<h2>Adicionar novo cliente</h2>
<p class="descricao-clientes">
    Preencha as informações para cadastrar um cliente.
</p>

<form method="POST">
    <div class="form-clientes">
        <div class="campo-cliente">
            <label for="cliente-nome">Nome do cliente</label>
            <input id="cliente-nome" name="nome" required>
        </div>

        <div class="campo-cliente">
            <label for="cliente-documento">CPF/CNPJ</label>
            <input id="cliente-documento" name="documento">
        </div>

        <div class="campo-cliente">
            <label for="cliente-telefone">Telefone</label>
            <input id="cliente-telefone" name="telefone">
        </div>

        <div class="campo-cliente">
            <label for="cliente-email">E-mail</label>
            <input id="cliente-email" name="email" type="email">
        </div>

        <div class="campo-cliente campo-inteiro">
            <label for="cliente-endereco">Endereço</label>
            <input id="cliente-endereco" name="endereco">
        </div>
    </div>

    <div class="acoes-cadastro">
        <button type="submit">Salvar cliente</button>
    </div>
</form>
                <hr>

              <style>
    .tabela-clientes-container {
        overflow-x: auto;
    }

    .tabela-clientes {
        width: 100%;
        min-width: 650px;
        border-collapse: collapse;
    }

    .tabela-clientes th {
        background: #C5D5E8;
        color: #17365D;
        text-align: left;
        padding: 14px 12px;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .tabela-clientes td {
        background: #F4F7FB;
        padding: 16px 12px;
        border-bottom: 1px solid #C5D2E0;
        border-right: 1px solid #DCE4ED;
        font-size: 13px;
        overflow-wrap: anywhere;
    }

    .tabela-clientes tbody tr:hover td {
        background: #F8FAFD;
    }

    .nome-cliente {
        color: #17365D;
        font-weight: bold;
    }

    .acoes-cliente {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .acoes-cliente form {
        margin: 0;
    }

    .editar-cliente,
    .excluir-cliente {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 7px;
        font-size: 13px;
        font-weight: bold;
        white-space: nowrap;
    }

    .editar-cliente {
        background: white;
        color: #17365D;
        border: 1px solid #DCE3EC;
        text-decoration: none;
    }

    .editar-cliente:hover {
        background: #EAF0F7;
    }

    .excluir-cliente {
        background: #DC3545;
        color: white;
        border: none;
        cursor: pointer;
    }

    .excluir-cliente:hover {
        background: #B02A37;
    }

    .tabela-clientes .lista-vazia {
        text-align: center;
        padding: 35px;
        color: #718096;
        background: white;
    }
</style>

<h2>Clientes cadastrados</h2>

<div class="tabela-clientes-container">
    <table class="tabela-clientes">
        <thead>
            <tr>
                <th scope="col">Nome do cliente</th>
                <th scope="col">CPF/CNPJ</th>
                <th scope="col">Telefone</th>
                <th scope="col">Ações</th>
            </tr>
        </thead>

        <tbody>
            {% for cliente in lista_clientes %}
                <tr>
                    <td class="nome-cliente">
                        {{ cliente["nome"] }}
                    </td>
                    <td>
                        {{ cliente["documento"] or "Não informado" }}
                    </td>
                    <td>
                        {{ cliente["telefone"] or "Não informado" }}
                    </td>
                    <td>
                        <div class="acoes-cliente">
                            <a class="editar-cliente"
                               href="{{ url_for('editar_cliente', id=cliente['id']) }}">
                                Editar
                            </a>

                            <form method="POST"
                                  action="{{ url_for('excluir_cliente', id=cliente['id']) }}"
                                  onsubmit="return confirm('Tem certeza que deseja excluir este cliente?');">
                                <button class="excluir-cliente" type="submit">
                                    Excluir
                                </button>
                            </form>
                        </div>
                    </td>
                </tr>
            {% else %}
                <tr>
                    <td colspan="4" class="lista-vazia">
                        Nenhum cliente cadastrado.
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

                <p><a href="/">Voltar ao painel</a></p>
<h2
            </div>
        </body>
        </html>
    """, lista_clientes=lista_clientes)


# ==========================================
# EXCLUSÃO DE CLIENTES
# ==========================================

@app.route("/clientes/excluir/<int:id>", methods=["POST"])
def excluir_cliente(id):

    conexao = conectar()

    conexao.execute("""
        DELETE FROM clientes
        WHERE id = ? AND empresa_id = 1
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("clientes"))

# ==========================================
# EDIÇÃO DE CLIENTES
# ==========================================

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):

    conexao = conectar()

    if request.method == "POST":

        nome = request.form["nome"]
        documento = request.form["documento"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        endereco = request.form["endereco"]

        conexao.execute("""
            UPDATE clientes
            SET nome = ?,
                documento = ?,
                telefone = ?,
                email = ?,
                               endereco = ?
            WHERE id = ? AND empresa_id = 1
        """, (nome, documento, telefone, email, endereco, id))

        conexao.commit()
        conexao.close()

        return redirect(url_for("clientes"))

    cliente = conexao.execute("""
        SELECT * FROM clientes
        WHERE id = ? AND empresa_id = 1
    """, (id,)).fetchone()

    conexao.close()

    if cliente is None:
        return "Cliente não encontrado.", 404

    return render_template_string("""
        <!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar cliente - SGF Industrial</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: #F1F4F9;
            color: #263445;
            margin: 0;
            padding: 30px;
        }

        .container {
            max-width: 1000px;
            margin: auto;
        }

        .topo {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 25px;
        }

        h1 {
            color: #17365D;
            font-size: 28px;
            margin: 0 0 8px;
        }

        .subtitulo {
            color: #718096;
            font-size: 14px;
            margin: 0;
        }

        .voltar,
        .cancelar {
            display: inline-block;
            background: white;
            color: #17365D;
            border: 1px solid #DCE3EC;
            border-radius: 7px;
            padding: 12px 18px;
            font-size: 14px;
            font-weight: bold;
            text-decoration: none;
        }

        .voltar:hover,
        .cancelar:hover {
            background: #EAF0F7;
        }

        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 3px 12px rgba(20, 45, 75, 0.06);
            overflow: hidden;
        }

        .cabecalho-card {
            background: #C5D5E8;
            padding: 22px 25px;
            border-bottom: 1px solid #B8CBE0;
        }

        .cabecalho-card h2 {
            color: #17365D;
            font-size: 20px;
            margin: 0 0 6px;
            overflow-wrap: anywhere;
        }

        .cabecalho-card p {
            color: #46566A;
            font-size: 13px;
            margin: 0;
        }

        form {
            padding: 25px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 20px;
        }

        .campo {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        label {
            color: #46566A;
            font-size: 13px;
            font-weight: bold;
        }

        input {
            width: 100%;
            background: #F4F7FB;
            color: #263445;
            border: 1px solid #DCE3EC;
            border-radius: 7px;
            padding: 12px;
            font-family: inherit;
            font-size: 14px;
        }

        input:focus {
            outline: none;
            background: white;
            border-color: #2864A5;
            box-shadow: 0 0 0 3px rgba(40, 100, 165, 0.10);
        }

        .campo-completo {
            grid-column: 1 / -1;
        }

        .acoes {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 28px;
            padding-top: 22px;
            border-top: 1px solid #DCE3EC;
        }

        .salvar {
            background: #17365D;
            color: white;
            border: none;
            border-radius: 7px;
            padding: 13px 22px;
            font-family: inherit;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
        }

        .salvar:hover {
            background: #245184;
        }

        @media (max-width: 650px) {
            body {
                padding: 15px;
            }

            h1 {
                font-size: 23px;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            form,
            .cabecalho-card {
                padding: 18px;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="topo">
            <div>
                <h1>Editar cliente</h1>
                <p class="subtitulo">
                    Atualize as informações do cadastro.
                </p>
            </div>

            <a class="voltar" href="{{ url_for('clientes') }}">
                ← Voltar aos clientes
            </a>
        </div>

        <div class="card">
            <div class="cabecalho-card">
                <h2>{{ cliente['nome'] }}</h2>
                <p>Confira os dados antes de salvar as alterações.</p>
            </div>

            <form method="POST">
                <div class="form-grid">
                    <div class="campo">
                        <label for="nome">Nome do cliente (obrigatório)</label>
                        <input id="nome" name="nome"
                               value="{{ cliente['nome'] }}" required>
                    </div>

                    <div class="campo">
                        <label for="documento">CPF/CNPJ</label>
                        <input id="documento" name="documento"
                               value="{{ cliente['documento'] or '' }}">
                    </div>

                    <div class="campo">
                        <label for="telefone">Telefone</label>
                        <input id="telefone" name="telefone" type="tel"
                               value="{{ cliente['telefone'] or '' }}">
                    </div>

                    <div class="campo">
                        <label for="email">E-mail</label>
                        <input id="email" name="email" type="email"
                               value="{{ cliente['email'] or '' }}">
                    </div>

                    <div class="campo campo-completo">
                        <label for="endereco">Endereço</label>
                        <input id="endereco" name="endereco"
                               value="{{ cliente['endereco'] or '' }}">
                    </div>
                </div>

                <div class="acoes">
                    <button class="salvar" type="submit">
                        Salvar alterações
                    </button>

                    <a class="cancelar" href="{{ url_for('clientes') }}">
                        Cancelar
                    </a>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
    """, cliente=cliente)


# ==========================================
# CADASTRO DE EQUIPAMENTOS
# ==========================================

@app.route("/equipamentos", methods=["GET", "POST"])
def equipamentos():

    if request.method == "POST":

        nome = request.form["nome"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        numero_serie = request.form["numero_serie"]
        tipo_gas = request.form["tipo_gas"]
        situacao = request.form["situacao"]
        valor_diaria = request.form["valor_diaria"] or 0
        valor_semanal = request.form["valor_semanal"] or 0
        valor_mensal = request.form["valor_mensal"] or 0

        conexao = conectar()

        conexao.execute("""
            INSERT INTO equipamentos (
                empresa_id, nome, marca, modelo,
                numero_serie, tipo_gas, situacao,
                valor_diaria, valor_semanal, valor_mensal
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1, nome, marca, modelo, numero_serie,
            tipo_gas, situacao, valor_diaria,
            valor_semanal, valor_mensal
        ))

        conexao.commit()
        conexao.close()

        return redirect(url_for("equipamentos"))

    conexao = conectar()

    lista_equipamentos = conexao.execute("""
        SELECT * FROM equipamentos
        WHERE empresa_id = 1
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">

<title>Equipamentos - SGF Industrial</title>

<style>
    * {
        box-sizing: border-box;
    }

    body {
        font-family: Arial, sans-serif;
        background: #F1F4F9;
        color: #263445;
        margin: 0;
        padding: 30px;
    }

    .container {
        max-width: 1200px;
        margin: auto;
        background: #FFFFFF;
        padding: 30px;
        border: 1px solid #DCE3EC;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(23, 54, 93, 0.06);
    }

    .topo {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 25px;
    }

    .topo h1 {
        color: #17365D;
        margin: 0 0 6px;
        font-size: 28px;
    }

    .subtitulo {
        color: #718096;
        margin: 0;
        font-size: 14px;
    }

    .voltar {
        display: inline-block;
        background: #FFFFFF;
        color: #17365D;
        padding: 11px 17px;
        border: 1px solid #DCE3EC;
        border-radius: 7px;
        font-weight: bold;
        text-decoration: none;
    }

    .voltar:hover {
        background: #EAF0F7;
    }

    input, select {
        display: block;
        width: 100%;
        padding: 10px;
        margin: 8px 0 15px;
        border: 1px solid #CBD5E0;
        border-radius: 6px;
        background: #FFFFFF;
    }

    button {
        background: #2474B8;
        color: #FFFFFF;
        border: none;
        padding: 12px 20px;
        border-radius: 6px;
        cursor: pointer;
    }

    button:hover {
        background: #175A94;
    }

    .equipamento {
        padding: 15px;
        border-bottom: 1px solid #E2E8F0;
    }

    a {
        color: #2474B8;
        text-decoration: none;
    }

    .form-equipamentos {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px 24px;
    }

    .form-equipamentos .campo label {
        display: block;
        color: #34465B;
        font-size: 13px;
        font-weight: bold;
    }

    .form-equipamentos .campo input,
    .form-equipamentos .campo select {
        width: 100%;
        margin: 8px 0 0;
        padding: 12px;
        border: 1px solid #CBD5E0;
        border-radius: 7px;
    }

    .form-equipamentos .acoes {
        grid-column: 1 / -1;
    }

    @media (max-width: 700px) {
        .form-equipamentos {
            grid-template-columns: 1fr;
        }
    }

/* Fundo principal da página */

body {
    background: #F4F5F7;
}


/* Área principal */

.container {
    background: #F9FAFC;
    border: 1px solid #D8DEE6;
}


/* Cabeçalho destacado */
.topo {
    background: #DCE7F3;
    padding: 22px;
    border-left: 5px solid #17365D;
    border-radius: 9px;
}

/* Formulário de equipamentos */

.form-equipamentos {
    background: #FFFFFF;
    border: 1px solid #CCD9E7;
    border-radius: 10px;
    padding: 24px;
}


/* Campos de preenchimento */
.form-equipamentos input,
.form-equipamentos select {
    background: #FFFFFF;
    border: 1px solid #B8CADD;
}

/* Título dos equipamentos cadastrados */
h2 {
    color: #17365D;
    margin-top: 28px;
}

/* Equipamentos cadastrados em cartões */
.equipamento {
    background: #FFFFFF;
    padding: 18px;
    border: 1px solid #D5DFEA;
    border-left: 4px solid #2474B8;
    border-radius: 8px;
        margin-bottom: 14px;
}

.tabela-equipamentos {
    width: 100%;
    border-collapse: collapse;
    background: #FFFFFF;
}

.tabela-equipamentos th {
    background: #DCE7F3;
    color: #17365D;
    padding: 15px 12px;
    text-align: left;
    border: 1px solid #B8CADD;
}

.tabela-equipamentos td {
    padding: 15px 12px;
    border: 1px solid #D5DFEA;
    color: #263445;
}

.tabela-equipamentos tbody tr:nth-child(even) {
    background: #F1F5FA;
}

.tabela-equipamentos tbody tr:hover {
    background: #EAF0F7;
}

.tabela-container {
    overflow-x: auto;
    border-radius: 8px;
}

/* Área principal branca */
.container {
    background: #FFFFFF;
}

/* Cabeçalho mais claro */
.topo {
    background: #DCE7F3;
}



</style>

        </head>

        <body>
            <div class="container">


<div class="topo">
    <div>
        <h1>Cadastro de Equipamentos</h1>
        <p class="subtitulo">
            Gerencie seus equipamentos, disponibilidade e valores de locação.
        </p>
    </div>

    <a href="/" class="voltar">← Voltar ao painel</a>
</div>



<form method="POST" class="form-equipamentos">

    <div class="campo">
        <label>Nome do equipamento</label>
        <input type="text" name="nome" required>
    </div>

    <div class="campo">
        <label>Marca</label>
        <input type="text" name="marca">
    </div>

    <div class="campo">
        <label>Modelo</label>
        <input type="text" name="modelo">
    </div>

    <div class="campo">
        <label>Número de série</label>
        <input type="text" name="numero_serie">
    </div>

    <div class="campo">
        <label>Tipo de gás detectado</label>
        <input type="text" name="tipo_gas">
    </div>

    <div class="campo">
        <label>Situação</label>
        <select name="situacao">
            <option>Disponível</option>
            <option>Alugado</option>
            <option>Em manutenção</option>
        </select>
    </div>

    <div class="campo">
        <label>Valor da diária (R$)</label>
        <input type="number" step="0.01" min="0" name="valor_diaria">
    </div>

    <div class="campo">
        <label>Valor semanal (R$)</label>
        <input type="number" step="0.01" min="0" name="valor_semanal">
    </div>

    <div class="campo">
        <label>Valor mensal (R$)</label>
        <input type="number" step="0.01" min="0" name="valor_mensal">
    </div>

    <div class="acoes">
        <button type="submit">Salvar equipamento</button>
    </div>

</form>

                <hr>


<h2>Equipamentos cadastrados</h2>

<div class="tabela-container">
    <table class="tabela-equipamentos" style="min-width: 850px;">

        <thead>
            <tr>
                <th>Equipamento</th>
                <th>Marca</th>
                <th>Modelo</th>
                <th>Número de série</th>
                <th>Situação</th>
                <th>Ações</th>
            </tr>
        </thead>

        <tbody>
            {% for equipamento in lista_equipamentos %}
            <tr>
                <td>
                    <strong>{{ equipamento["nome"] }}</strong>
                </td>

                <td>
                    {{ equipamento["marca"] or "Não informada" }}
                </td>

                <td>
                    {{ equipamento["modelo"] or "Não informado" }}
                </td>

                <td>
                    {{ equipamento["numero_serie"] or "Não informado" }}
                </td>

                <td>
                    {{ equipamento["situacao"] }}
                </td>

                <td>
                    <a href="{{ url_for('editar_equipamento', id=equipamento['id']) }}"
                       style="display:inline-block; padding:8px 12px; background:#E8F0F8; color:#17365D; border-radius:6px; margin:3px; font-weight:bold;">
                        Editar
                    </a>

                    <form method="POST"
                          action="{{ url_for('excluir_equipamento', id=equipamento['id']) }}"
                          onsubmit="return confirm('Tem certeza que deseja excluir este equipamento?');"
                          style="display:inline;">

                        <button type="submit"
                                style="background:#DC3545; color:white; padding:8px 12px; border-radius:6px; margin:3px;">
                            Excluir
                        </button>

                    </form>
                </td>
            </tr>

            {% else %}
            <tr>
                <td colspan="6" style="text-align:center; padding:25px;">
                    Nenhum equipamento cadastrado.
                </td>
            </tr>
            {% endfor %}
        </tbody>

    </table>
</div>


                <p><a href="/">Voltar ao painel</a></p>

            </div>
        </body>
        </html>
    """, lista_equipamentos=lista_equipamentos)



# ==========================================
# EXCLUSÃO DE EQUIPAMENTOS
# ==========================================

@app.route("/equipamentos/excluir/<int:id>", methods=["POST"])
def excluir_equipamento(id):

    conexao = conectar()

    conexao.execute("""
        DELETE FROM equipamentos
        WHERE id = ? AND empresa_id = 1
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("equipamentos"))

# ==========================================
# EDIÇÃO DE EQUIPAMENTOS
# ==========================================

@app.route("/equipamentos/editar/<int:id>", methods=["GET", "POST"])
def editar_equipamento(id):

    conexao = conectar()

    if request.method == "POST":

        nome = request.form["nome"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        numero_serie = request.form["numero_serie"]
        tipo_gas = request.form["tipo_gas"]
        situacao = request.form["situacao"]
        valor_diaria = request.form["valor_diaria"] or 0
        valor_semanal = request.form["valor_semanal"] or 0
        valor_mensal = request.form["valor_mensal"] or 0

        conexao.execute("""
            UPDATE equipamentos
            SET nome = ?,
                marca = ?,
                modelo = ?,
                numero_serie = ?,
                tipo_gas = ?,
                situacao = ?,
                valor_diaria = ?,
                valor_semanal = ?,
                valor_mensal = ?
            WHERE id = ? AND empresa_id = 1
        """, (
            nome, marca, modelo, numero_serie,
            tipo_gas, situacao, valor_diaria,
            valor_semanal, valor_mensal, id
        ))

        conexao.commit()
        conexao.close()

        return redirect(url_for("equipamentos"))

    equipamento = conexao.execute("""
        SELECT * FROM equipamentos
        WHERE id = ? AND empresa_id = 1
    """, (id,)).fetchone()

    conexao.close()

    if equipamento is None:
        return "Equipamento não encontrado.", 404

    return render_template_string("""
        <h1>Editar equipamento</h1>

        <form method="POST">

            <p>Nome:</p>
            <input name="nome" value="{{ equipamento['nome'] }}" required>

            <p>Marca:</p>
            <input name="marca" value="{{ equipamento['marca'] or '' }}">

            <p>Modelo:</p>
            <input name="modelo" value="{{ equipamento['modelo'] or '' }}">

            <p>Número de série:</p>
            <input name="numero_serie" value="{{ equipamento['numero_serie'] or '' }}">

            <p>Tipo de gás:</p>
            <input name="tipo_gas" value="{{ equipamento['tipo_gas'] or '' }}">

            <p>Situação:</p>
            <select name="situacao">
                {% for opcao in ['Disponível', 'Alugado', 'Em manutenção'] %}
                    <option value="{{ opcao }}"
                    {% if equipamento['situacao'] == opcao %}selected{% endif %}>
                        {{ opcao }}
                    </option>
                {% endfor %}
            </select>

            <p>Valor da diária:</p>
            <input type="number" step="0.01" min="0" name="valor_diaria"
                   value="{{ equipamento['valor_diaria'] }}">

            <p>Valor semanal:</p>
            <input type="number" step="0.01" min="0" name="valor_semanal"
                   value="{{ equipamento['valor_semanal'] }}">

            <p>Valor mensal:</p>
            <input type="number" step="0.01" min="0" name="valor_mensal"
                   value="{{ equipamento['valor_mensal'] }}">

            <br><br>
            <button type="submit">Salvar alterações</button>

        </form>

        <p><a href="/equipamentos">Voltar aos equipamentos</a></p>
    """, equipamento=equipamento)

# ==========================================
# CADASTRO DE PRODUTOS
# ==========================================



@app.route("/produtos", methods=["GET", "POST"])
def produtos():

    conexao = conectar()

    if request.method == "POST":

        codigo = request.form["codigo"].strip()
        nome = request.form["nome"].strip()
        descricao = request.form["descricao"].strip()
        categoria = request.form["categoria"].strip()
        preco_venda = request.form["preco_venda"] or 0
        quantidade_estoque = request.form["quantidade_estoque"] or 0
        estoque_minimo = request.form["estoque_minimo"] or 0

        try:
            conexao.execute("""
                INSERT INTO produtos (
                    empresa_id, codigo, nome, descricao,
                    categoria, preco_venda,
                    quantidade_estoque, estoque_minimo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                1, codigo, nome, descricao,
                categoria, float(preco_venda),
                int(quantidade_estoque), int(estoque_minimo)
            ))

            conexao.commit()
            conexao.close()

            return redirect(url_for("produtos"))

        except Exception as erro:
            conexao.close()
            return f"Erro ao cadastrar produto: {erro}"

    busca = request.args.get("busca", "").strip()
    categoria_filtro = request.args.get("categoria", "").strip()

    consulta = """
        SELECT * FROM produtos
        WHERE empresa_id = 1
    """

    parametros = []

    if busca:
        consulta += " AND (nome LIKE ? OR codigo LIKE ?)"
        parametros.extend([f"%{busca}%", f"%{busca}%"])

    if categoria_filtro:
        consulta += " AND categoria = ?"
        parametros.append(categoria_filtro)

    consulta += " ORDER BY nome"

    lista_produtos = conexao.execute(
        consulta, parametros
    ).fetchall()

    categorias = conexao.execute("""
        SELECT DISTINCT categoria
        FROM produtos
        WHERE empresa_id = 1
        AND categoria IS NOT NULL
        AND categoria != ''
        ORDER BY categoria
    """).fetchall()

    conexao.close()

    return render_template_string("""

        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Produtos - SGF Industrial</title>

            <style>
                * {
                    box-sizing: border-box;
                }

                body {
                    font-family: Arial, sans-serif;
                    background: #F1F4F9;
                    margin: 0;
                    padding: 30px;
                    color: #263445;
                }

                .container {
                    max-width: 1200px;
                    margin: auto;
                }

                .topo {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 25px;
                    flex-wrap: wrap;
                    gap: 15px;
                    background: #DCE7F3;
                    padding: 22px;
                    border-left: 5px solid #17365D;
                    border-radius: 9px;
                }

                .topo h1 {
                    color: #17365D;
                    margin: 0 0 6px;
                    font-size: 28px;
                }

                .subtitulo {
                    color: #718096;
                    margin: 0;
                    font-size: 14px;
                }

                .voltar {
                    background: white;
                    color: #17365D;
                    text-decoration: none;
                    padding: 11px 17px;
                    border-radius: 7px;
                    border: 1px solid #DCE3EC;
                    font-weight: bold;
                }

                .voltar:hover {
                    background: #EAF0F7;
                }

                .card {
                    background: white;
                    padding: 25px;
                    border-radius: 12px;
                    box-shadow: 0 3px 12px rgba(20, 45, 75, 0.06);
                    margin-bottom: 25px;
                }

                .card h2 {
                    color: #17365D;
                    margin: 0 0 8px;
                    font-size: 20px;
                }

                .descricao-card {
                    color: #718096;
                    font-size: 13px;
                    margin: 0 0 22px;
                }
                .titulo-secao {
    background: #F4F7FB;
    border-left: 4px solid #17365D;
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 22px;
}

.titulo-secao h2 {
    color: #17365D;
    margin: 0 0 6px;
    font-size: 22px;
}

.titulo-secao p {
    color: #718096;
    margin: 0;
    font-size: 13px;
}

.titulo-lista {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 15px;
    flex-wrap: wrap;
    margin-bottom: 18px;
}

.titulo-lista .titulo-secao {
    flex: 1;
    margin-bottom: 0;
}

.titulo-lista .badge {
    background: #EAF0F7;
    color: #17365D;
    padding: 8px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: bold;
}

                .form-grid {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 18px;
                }

                .campo {
                    display: flex;
                    flex-direction: column;
                    gap: 7px;
                }

                .campo label {
                    font-size: 13px;
                    font-weight: bold;
                    color: #46566A;
                }

                .campo input {
                    width: 100%;
                    padding: 12px;
                    border: 1px solid #DCE3EC;
                    border-radius: 7px;
                    font-size: 14px;
                    outline: none;
                }

                .campo input:focus {
                    border-color: #2864A5;
                    box-shadow: 0 0 0 3px rgba(40, 100, 165, 0.10);
                }

                .campo-completo {
                    grid-column: 1 / -1;
                }

                .botao {
                    margin-top: 22px;
                    background: #17365D;
                    color: white;
                    padding: 13px 22px;
                    border: none;
                    border-radius: 7px;
                    font-weight: bold;
                    cursor: pointer;
                    font-size: 14px;
                }

                .botao:hover {
                    background: #245184;
                }

                .titulo-lista {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    gap: 10px;
                    flex-wrap: wrap;
                }

                .contador {
                    background: #EAF0F7;
                    color: #17365D;
                    padding: 7px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: bold;
                }

                .tabela-container {
                    overflow-x: auto;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    min-width: 700px;
                }

                th {
    background: #EAF0F7;
    color: #17365D;
    text-align: left;
    padding: 14px 12px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

                td {
    padding: 16px 12px;
    border-bottom: 1px solid #C5D2E0;
    border-right: 1px solid #DCE4ED;
    font-size: 13px;
    vertical-align: middle;
}

                tbody tr:hover {
                    background: #F8FAFD;
                }

                .nome-produto {
                    color: #17365D;
                    font-weight: bold;
                    font-size: 14px;
                }

                .codigo {
                    display: inline-block;
                    background: #EEF3F9;
                    color: #31577F;
                    padding: 5px 9px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                }

                .preco {
                    font-weight: bold;
                    color: #263445;
                }

                .saldo {
                    font-size: 15px;
                    font-weight: bold;
                    color: #263445;
                }

                .status {
                    display: inline-block;
                    padding: 7px 10px;
                    border-radius: 20px;
                    font-size: 11px;
                    font-weight: bold;
                    white-space: nowrap;
                }

                .status-normal {
                    background: #E5F5EC;
                    color: #237747;
                }

                .status-baixo {
                    background: #FFF0E0;
                    color: #B65B12;
                }

                .vazio {
                    text-align: center;
                    padding: 35px;
                    color: #718096;
                }

                @media (max-width: 650px) {
                    body {
                        padding: 15px;
                    }

                    .form-grid {
                        grid-template-columns: 1fr;
                    }

                    .campo-completo {
                        grid-column: auto;
                    }

                    .card {
                        padding: 18px;
                    }

                    .topo h1 {
                        font-size: 23px;
                    }
                }
            </style>
        </head>

        <body>
            <div class="container">

                <div class="topo">
                    <div>
                        <h1>📦 Gestão de Produtos</h1>
                        <p class="subtitulo">
                            Cadastro e controle de produtos do estoque
                        </p>
                    </div>

                    <a class="voltar" href="/">
                        ← Painel principal
                    </a>
                </div>

                <div class="card">

                  <div class="titulo-secao">
    <h2>Adicionar novo produto</h2>
    <p>
        Preencha as informações para cadastrar um produto.
    </p>
</div>

                    <form method="POST">

                        <div class="form-grid">

                            <div class="campo">
                                <label>Código do produto (SKU)</label>
                                <input name="codigo" required
                                       placeholder="Ex.: PROD002">
                            </div>

                            <div class="campo">
                                <label>Nome do produto</label>
                                <input name="nome" required
                                       placeholder="Nome do produto">
                            </div>

                            <div class="campo">
                                <label>Descrição</label>
                                <input name="descricao"
                                       placeholder="Descrição do produto">
                            </div>

                            <div class="campo">
                                <label>Categoria</label>
                                <input name="categoria"
                                       placeholder="Ex.: Equipamentos">
                            </div>

                            <div class="campo">
                                <label>Preço de venda (R$)</label>
                                <input type="number" step="0.01" min="0"
                                       name="preco_venda" value="0">
                            </div>

                            <div class="campo">
                                <label>Quantidade inicial em estoque</label>
                                <input type="number" min="0"
                                       name="quantidade_estoque" value="0">
                            </div>

                            <div class="campo">
                                <label>Estoque mínimo</label>
                                <input type="number" min="0"
                                       name="estoque_minimo" value="0">
                            </div>

                        </div>

                        <button class="botao" type="submit">
                            + Cadastrar produto
                        </button>

                    </form>

                </div>

                <div class="card">

               <div class="titulo-lista">
    <div class="titulo-secao">
        <h2>Produtos cadastrados</h2>
        <p>
            Consulte os produtos e a situação atual do estoque.
        </p>
</div>


<form method="GET" action="/produtos" style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin:20px 0;">

    <input
        type="text"
        name="busca"
        placeholder="Buscar por nome ou código SKU"
        value="{{ busca }}"
        style="flex:2; min-width:220px; height:44px; padding:0 12px; border:1px solid #DCE3EC; border-radius:7px; font-size:14px;"
    >

    <select
        name="categoria"
        style="flex:1; min-width:180px; height:44px; padding:0 12px; border:1px solid #DCE3EC; border-radius:7px; font-size:14px;"
    >
        <option value="">Todas as categorias</option>

        {% for item in categorias %}
            <option value="{{ item['categoria'] }}"
                {% if categoria_filtro == item['categoria'] %}selected{% endif %}>
                {{ item['categoria'] }}
            </option>
        {% endfor %}
    </select>

    <button type="submit" class="botao"
        style="margin:0; height:44px; padding:0 22px; white-space:nowrap;">
        Buscar
    </button>

    <a href="/produtos" class="voltar"
        style="height:44px; padding:0 22px; display:flex; align-items:center; justify-content:center; white-space:nowrap;">
        Limpar
    </a>

</form>

</div>

<span class="contador">
    {{ lista_produtos|length }} produto(s)
</span>
</div>

                    </div>

                    <div class="tabela-container">

                      <table>
      <thead>
    <tr>
        <th style="background-color: #C5D5E8; color: #17365D;">Produto</th>
        <th style="background-color: #C5D5E8; color: #17365D;">Código SKU</th>
        <th style="background-color: #C5D5E8; color: #17365D;">Categoria</th>
        <th style="background-color: #C5D5E8; color: #17365D;">Preço</th>
        <th style="background-color: #C5D5E8; color: #17365D;">Estoque</th>
        <th style="background-color: #C5D5E8; color: #17365D;">Situação</th>
    </tr>
</thead>

                            <tbody>

                               {% for produto in lista_produtos %}
<tr style="background-color: #F4F7FB;">
                                    <td>
                                        <span class="nome-produto">
                                            {{ produto["nome"] }}
                                        </span>
                                    </td>

                                    <td>
                                        <span class="codigo">
                                            {{ produto["codigo"] or "Sem código" }}
                                        </span>
                                    </td>

                                    <td>
                                        {{ produto["categoria"] or "Não informada" }}
                                    </td>

                                    <td class="preco">
                                        R$ {{ "%.2f"|format(produto["preco_venda"] or 0) }}
                                    </td>

                                    <td>
                                        <span class="saldo">
                                            {{ produto["quantidade_estoque"] }}
                                        </span>
                                        <br>
                                        <small>
                                            Mínimo: {{ produto["estoque_minimo"] }}
                                        </small>
                                    </td>

                                    <td>
                                        {% if produto["quantidade_estoque"] <= produto["estoque_minimo"] %}
                                            <span class="status status-baixo">
                                                ⚠ Estoque baixo
                                            </span>
                                        {% else %}
                                            <span class="status status-normal">
                                                ✓ Estoque normal
                                            </span>
                                        {% endif %}
                                    </td>
                                </tr>

                                {% else %}
                                <tr>
                                    <td colspan="6" class="vazio">
                                        Nenhum produto cadastrado ainda.
                                    </td>
                                </tr>
                                {% endfor %}

                            </tbody>
                        </table>

                    </div>

                </div>

            </div>
        </body>
        </html>
    """,
        lista_produtos=lista_produtos,
        busca=busca,
        categorias=categorias,
        categoria_filtro=categoria_filtro
    )



# ==========================================
# MOVIMENTAÇÕES DE ESTOQUE
# ==========================================


@app.route("/movimentacoes-estoque", methods=["GET", "POST"])
def movimentacoes_estoque():

    conexao = conectar()

    if request.method == "POST":

        produto_id = request.form["produto_id"]
        tipo = request.form["tipo"]
        quantidade = request.form["quantidade"]
        motivo = request.form["motivo"].strip()

        if tipo not in ("Entrada", "Saída"):
            conexao.close()
            return "Tipo de movimentação inválido."

        try:
            quantidade = int(quantidade)

            if quantidade <= 0:
                conexao.close()
                return "A quantidade deve ser maior que zero."

            produto = conexao.execute("""
                SELECT * FROM produtos
                WHERE id = ? AND empresa_id = 1
            """, (produto_id,)).fetchone()

            if produto is None:
                conexao.close()
                return "Produto não encontrado."

            saldo_atual = produto["quantidade_estoque"]

            if tipo == "Saída" and quantidade > saldo_atual:
                conexao.close()
                return (
                    f"Estoque insuficiente! "
                    f"Disponível: {saldo_atual} unidade(s)."
                )

            if tipo == "Entrada":
                conexao.execute("""
                    UPDATE produtos
                    SET quantidade_estoque = quantidade_estoque + ?
                    WHERE id = ? AND empresa_id = 1
                """, (quantidade, produto_id))

            else:
                conexao.execute("""
                    UPDATE produtos
                    SET quantidade_estoque = quantidade_estoque - ?
                    WHERE id = ?
                    AND empresa_id = 1
                    AND quantidade_estoque >= ?
                """, (quantidade, produto_id, quantidade))

                if conexao.execute("SELECT changes()").fetchone()[0] == 0:
                    conexao.rollback()
                    conexao.close()
                    return "Estoque insuficiente para essa saída."

            conexao.execute("""
                INSERT INTO movimentacoes_estoque (
                    empresa_id, produto_id, tipo,
                    quantidade, motivo, data_movimentacao
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                1,
                produto_id,
                tipo,
                quantidade,
                motivo,
                date.today().isoformat()
            ))

            conexao.commit()
            conexao.close()

            return redirect(url_for("movimentacoes_estoque"))

        except ValueError:
            conexao.close()
            return "Informe uma quantidade inteira válida."

        except Exception as erro:
            conexao.rollback()
            conexao.close()
            return f"Erro na movimentação: {erro}"

    lista_produtos = conexao.execute("""
        SELECT * FROM produtos
        WHERE empresa_id = 1
        ORDER BY nome
    """).fetchall()

    historico = conexao.execute("""
        SELECT movimentacoes_estoque.*,
               produtos.nome AS produto_nome,
               produtos.codigo AS produto_codigo
        FROM movimentacoes_estoque
        JOIN produtos
            ON produtos.id = movimentacoes_estoque.produto_id
        WHERE movimentacoes_estoque.empresa_id = 1
        ORDER BY movimentacoes_estoque.id DESC
    """).fetchall()

    conexao.close()

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Movimentações - SGF Industrial</title>

            <style>
                * {
                    box-sizing: border-box;
                }

                body {
                    font-family: Arial, sans-serif;
                    background: #F1F4F9;
                    margin: 0;
                    padding: 30px;
                    color: #263445;
                }

                .container {
                    max-width: 1200px;
                    margin: auto;
                }

                .topo {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 25px;
    background: #DCE7F3;
    padding: 22px;
    border-left: 5px solid #17365D;
    border-radius: 9px;
}
                .topo h1 {
                    color: #17365D;
                    margin: 0 0 6px;
                    font-size: 28px;
                }

                .subtitulo {
                    color: #718096;
                    margin: 0;
                    font-size: 14px;
                }

                .voltar {
                    background: white;
                    color: #17365D;
                    text-decoration: none;
                    padding: 11px 17px;
                    border-radius: 7px;
                    border: 1px solid #DCE3EC;
                    font-weight: bold;
                }

                .voltar:hover {
                    background: #EAF0F7;
                }

                .card {
                    background: white;
                    padding: 25px;
                    border-radius: 12px;
                    box-shadow: 0 3px 12px rgba(20, 45, 75, 0.06);
                    margin-bottom: 25px;
                }

                .card h2 {
                    color: #17365D;
                    margin: 0 0 8px;
                    font-size: 20px;
                }

                .descricao-card {
                    color: #718096;
                    font-size: 13px;
                    margin: 0 0 22px;
                }
                .titulo-secao {
    background: #F4F7FB;
    border-left: 4px solid #17365D;
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 22px;
}

.titulo-secao h2 {
    color: #17365D;
    margin: 0 0 6px;
    font-size: 22px;
}

.titulo-secao p {
    color: #718096;
    margin: 0;
    font-size: 13px;
}

.titulo-lista {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 15px;
    flex-wrap: wrap;
    margin-bottom: 18px;
}

.titulo-lista .titulo-secao {
    flex: 1;
    margin-bottom: 0;
}

.titulo-lista .badge {
    background: #EAF0F7;
    color: #17365D;
    padding: 8px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: bold;
}

                .form-grid {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 18px;
                }

                .campo {
                    display: flex;
                    flex-direction: column;
                    gap: 7px;
                }

                .campo label {
                    font-size: 13px;
                    font-weight: bold;
                    color: #46566A;
                }

                .campo input,
                .campo select {
                    width: 100%;
                    padding: 12px;
                    border: 1px solid #DCE3EC;
                    border-radius: 7px;
                    font-size: 14px;
                    background: white;
                    outline: none;
                }

                .campo input:focus,
                .campo select:focus {
                    border-color: #2864A5;
                    box-shadow: 0 0 0 3px rgba(40, 100, 165, 0.10);
                }

                .campo-completo {
                    grid-column: 1 / -1;
                }

                .botao {
                    margin-top: 22px;
                    background: #17365D;
                    color: white;
                    padding: 13px 22px;
                    border: none;
                    border-radius: 7px;
                    font-weight: bold;
                    cursor: pointer;
                    font-size: 14px;
                }

                .botao:hover {
                    background: #245184;
                }

                .titulo-lista {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-bottom: 20px;
                }

                .contador {
                    background: #EAF0F7;
                    color: #17365D;
                    padding: 7px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: bold;
                }

                .tabela-container {
                    overflow-x: auto;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    min-width: 700px;
                }

               th {
    background: #EAF0F7 !important;
    color: #17365D;
    text-align: left;
    padding: 14px 12px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}
               td {
    padding: 16px 12px;
    border-bottom: 1px solid #D5DFEA;
    border-right: 1px solid #E1E8F0;
    font-size: 13px;
    vertical-align: middle;
}

tbody tr:hover {
    background-color: #DCE8F5 !important;
}
                tbody tr:hover {
                    background: #F8FAFD;
                }

                .nome-produto {
                    color: #17365D;
                    font-weight: bold;
                    font-size: 14px;
                }

                .codigo {
                    display: inline-block;
                    background: #EEF3F9;
                    color: #31577F;
                    padding: 5px 9px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                }

                .tipo {
                    display: inline-block;
                    padding: 7px 11px;
                    border-radius: 20px;
                    font-size: 11px;
                    font-weight: bold;
                }

                .entrada {
                    background: #E5F5EC;
                    color: #237747;
                }

                .saida {
                    background: #FCE8E8;
                    color: #B42318;
                }

                .quantidade {
                    font-weight: bold;
                    font-size: 14px;
                }

                .data {
                    color: #536477;
                    white-space: nowrap;
                }

                .vazio {
                    text-align: center;
                    padding: 35px;
                    color: #718096;
                }

                @media (max-width: 650px) {
                    body {
                        padding: 15px;
                    }

                    .form-grid {
                        grid-template-columns: 1fr;
                    }

                    .campo-completo {
                        grid-column: auto;
                    }

                    .card {
                        padding: 18px;
                    }

                    .topo h1 {
                        font-size: 23px;
                    }
                }
            </style>
        </head>

        <body>
            <div class="container">

                <div class="topo">
                    <div>
                        <h1>📊 Movimentações de Estoque</h1>
                        <p class="subtitulo">
                            Controle de entradas, saídas e histórico de produtos
                        </p>
                    </div>

                    <a class="voltar" href="/">
                        ← Painel principal
                    </a>
                </div>

                <div class="card">

                 <div class="titulo-secao">
    <h2>Registrar movimentação</h2>
    <p>
        Informe o produto, o tipo e a quantidade movimentada.
    </p>
</div>


                    <form method="POST">

                        <div class="form-grid">

                            <div class="campo campo-completo">
                                <label>Produto</label>

                                <select name="produto_id" required>
                                    <option value="">Selecione um produto</option>

                                    {% for produto in lista_produtos %}
                                        <option value="{{ produto['id'] }}">
                                            {{ produto['codigo'] }} - {{ produto['nome'] }}
                                            (Estoque: {{ produto['quantidade_estoque'] }})
                                        </option>
                                    {% endfor %}
                                </select>
                            </div>

                            <div class="campo">
                                <label>Tipo de movimentação</label>

                                <select name="tipo" required>
                                    <option value="Entrada">Entrada</option>
                                    <option value="Saída">Saída</option>
                                </select>
                            </div>

                            <div class="campo">
                                <label>Quantidade</label>

                                <input type="number" name="quantidade"
                                       min="1" step="1" required
                                       placeholder="Informe a quantidade">
                            </div>

                            <div class="campo campo-completo">
                                <label>Motivo da movimentação</label>

                                <input name="motivo"
                                       placeholder="Ex.: Compra, venda ou consumo interno">
                            </div>

                        </div>

                        <button class="botao" type="submit">
                            Registrar movimentação
                        </button>

                    </form>

                </div>

                <div class="card">

                   <div class="titulo-lista">
    <div class="titulo-secao">
        <h2>Histórico de movimentações</h2>
        <p>
            Acompanhe todas as entradas e saídas registradas.
        </p>
    </div>

                        <span class="contador">
                            {{ historico|length }} movimentação(ões)
                        </span>
                    </div>

                    <div class="tabela-container">

             <style>
    .tabela-movimentacoes thead th {
        background-color: #C5D5E8;
        color: #17365D;
    }

    .tabela-movimentacoes tbody td {
        background-color: #F4F7FB;
    }
</style>

<table class="tabela-produtos tabela-movimentacoes">
    <thead>
        <tr>
    <th>Produto</th>
                                    <th>Código SKU</th>
                                    <th>Tipo</th>
                                    <th>Quantidade</th>
                                    <th>Motivo</th>
                                    <th>Data</th>
                                </tr>
                            </thead>

                            <tbody>

                                {% for movimento in historico %}
                                <tr>
                                    <td>
                                        <span class="nome-produto">
                                            {{ movimento['produto_nome'] }}
                                        </span>
                                    </td>

                                    <td>
                                        <span class="codigo">
                                            {{ movimento['produto_codigo'] }}
                                        </span>
                                    </td>

                                    <td>
                                        {% if movimento['tipo'] == 'Entrada' %}
                                            <span class="tipo entrada">
                                                ↑ Entrada
                                            </span>
                                        {% else %}
                                            <span class="tipo saida">
                                                ↓ Saída
                                            </span>
                                        {% endif %}
                                    </td>

                                    <td class="quantidade">
                                        {{ movimento['quantidade'] }} un.
                                    </td>

                                    <td>
                                        {{ movimento['motivo'] or 'Não informado' }}
                                    </td>

                                    <td class="data">
                                        {{ movimento['data_movimentacao'][8:10] }}/{{ movimento['data_movimentacao'][5:7] }}/{{ movimento['data_movimentacao'][0:4] }}
                                    </td>
                                </tr>

                                {% else %}
                                <tr>
                                    <td colspan="6" class="vazio">
                                        Nenhuma movimentação registrada ainda.
                                    </td>
                                </tr>
                                {% endfor %}

                            </tbody>
                        </table>

                    </div>

                </div>

                <p>
                    <a class="voltar" href="/produtos">
                        📦 Consultar produtos
                    </a>
                </p>

            </div>
        </body>
        </html>
    """,
        lista_produtos=lista_produtos,

    )


# ==========================================
# PAINEL PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

    conexao = conectar()
    produtos_estoque_baixo = conexao.execute("""
        SELECT codigo, nome, quantidade_estoque, estoque_minimo
        FROM produtos
        WHERE empresa_id = 1
        AND quantidade_estoque <= estoque_minimo
        ORDER BY quantidade_estoque ASC
    """).fetchall()

    mes_atual = __import__('datetime').date.today().strftime('%Y-%m')

    total_recebido = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_receber
        WHERE empresa_id = 1
        AND situacao = 'Recebida'
        AND data_recebimento LIKE ?
    """, (mes_atual + '%',)).fetchone()[0]

    total_pago = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_pagar
        WHERE empresa_id = 1
        AND situacao = 'Paga'
        AND data_pagamento LIKE ?
    """, (mes_atual + '%',)).fetchone()[0]

    total_a_receber = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_receber
        WHERE empresa_id = 1
        AND situacao = 'Pendente'
    """).fetchone()[0]

    total_a_pagar = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_pagar
        WHERE empresa_id = 1
        AND situacao = 'Pendente'
    """).fetchone()[0]


    meses_financeiros = []

    hoje = date.today()

    for deslocamento in range(5, -1, -1):

        numero_mes = hoje.year * 12 + hoje.month - 1 - deslocamento

        ano = numero_mes // 12
        mes = numero_mes % 12 + 1

        mes_referencia = f"{ano:04d}-{mes:02d}"

        entradas = conexao.execute("""
            SELECT COALESCE(SUM(valor), 0)
            FROM contas_receber
            WHERE empresa_id = 1
            AND situacao = 'Recebida'
            AND data_recebimento LIKE ?
        """, (mes_referencia + '%',)).fetchone()[0]

        saidas = conexao.execute("""
            SELECT COALESCE(SUM(valor), 0)
            FROM contas_pagar
            WHERE empresa_id = 1
            AND situacao = 'Paga'
            AND data_pagamento LIKE ?
        """, (mes_referencia + '%',)).fetchone()[0]

        meses_financeiros.append({
            "mes": f"{mes:02d}/{str(ano)[-2:]}",
            "entradas": entradas,
            "saidas": saidas,
            "resultado": entradas - saidas
        })

    maior_movimento = max(
        [max(m["entradas"], m["saidas"]) for m in meses_financeiros] or [0]
    )
    maior_resultado = max(
        [abs(m["resultado"]) for m in meses_financeiros] or [0]
    )

    saldo_caixa = total_recebido - total_pago
    conexao.close()

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt-br">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <title>SGF Industrial</title>

            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: Arial, sans-serif;
                }

                body {
                    background: #F2F5F9;
                    color: #26364A;
                }

                .sidebar {
    width: 250px;
    height: 100vh;
    background: linear-gradient(180deg, #142B45 0%, #0D1D30 100%);
    color: white;
    position: fixed;
    padding: 25px 18px;
    box-shadow: 3px 0 12px rgba(0, 0, 0, 0.12);
    overflow-y: auto;
}

               .logo {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: #FFFFFF;
    white-space: nowrap;
    margin-bottom: 10px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

                .subtitle {
                    font-size: 11px;
                    color: #B9C9D9;
                    margin-bottom: 40px;
                }

                .menu a {
    display: block;
    color: #D6E2EF;
    text-decoration: none;
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.menu a:hover {
    background: #2474B8;
    color: #FFFFFF;
    padding-left: 20px;
}
               .main {
    margin-left: 250px;
    padding: 35px;
    min-height: 100vh;
    background: #CDD9E7;
}

                .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding: 20px 25px;
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E3EAF2;
    box-shadow: 0 3px 12px rgba(20, 43, 69, 0.05);
}
.header h1 {
    color: #142B45;
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 6px;
}

.header p {
    color: #64748B;
    font-size: 14px;
    margin: 0;
}

                .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 22px;
    margin-bottom: 30px;
}

.card {
    background: #FFFFFF;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #E3EAF2;
    box-shadow: 0 3px 12px rgba(20, 43, 69, 0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 7px 18px rgba(20, 43, 69, 0.12);
}

.card p {
    color: #64748B;
    font-size: 14px;
    margin-bottom: 12px;
}

.card h2 {
    color: #142B45;
    font-size: 26px;
    font-weight: bold;
}

                .card {
                    background: white;
                    padding: 25px;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px #0000000A;
                }

                .card p {
                    color: #718096;
                    margin-bottom: 15px;
                }

                .card h2 {
                    font-size: 25px;
                    color: #142B45;
                }

                .panel {
    background: #FFFFFF;
    padding: 28px;
    border-radius: 14px;
    min-height: 180px;
    border: 1px solid #E3EAF2;
    box-shadow: 0 3px 12px rgba(20, 43, 69, 0.06);
    margin-bottom: 25px;
}

.panel h2 {
    color: #142B45;
    font-size: 20px;
    margin-bottom: 15px;
}

.panel p {
    color: #64748B;
    font-size: 14px;
    line-height: 1.6;
}

                .botao {
    display: inline-block;
    margin-top: 20px;
    background: #2474B8;
    color: #FFFFFF;
    padding: 13px 22px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 14px;
    font-weight: bold;
    border: none;
    cursor: pointer;
    transition: background 0.2s, transform 0.2s;
}

.botao:hover {
    background: #185A91;
    transform: translateY(-2px);
}

                @media (max-width: 800px) {
                    .sidebar {
                        width: 100%;
                        height: auto;
                        position: relative;
                    }

                    .main {
                        margin-left: 0;
                        padding: 18px;
                    }

                    .cards {
                        grid-template-columns: 1fr;
                    }
                }
            </style>

        </head>

        <body>

            <aside class="sidebar">

                <div class="logo">SGF INDUSTRIAL</div>

                <div class="subtitle">
                    GESTÃO FINANCEIRA EMPRESARIAL
                </div>

                <nav class="menu">
    <a href="/">▦ Visão geral</a>
    <a href="/clientes">👥 Clientes</a>
    <a href="/equipamentos">🔧 Equipamentos</a>
    <a href="/produtos">📦 Produtos</a>
    <a href="/movimentacoes-estoque">📊 Movimentações de estoque</a>
    <a href="/fluxo-caixa">💰 Fluxo de caixa</a>
    <a href="/contas-pagar">📤 Contas a pagar</a>
<a href="/contas-receber">📥 Contas a receber</a>
<a href="/fechamento-mensal">📅 Fechamento mensal</a>
<a href="/fechamento-anual">📊 Fechamento anual</a>

                    <a href="#">📊 Relatórios</a>
                    <a href="#">🏢 Empresas</a>
                    <a href="#">⚙ Configurações</a>
                </nav>

            </aside>

            <main class="main">

                <header class="header">
                    <div>
                        <h1>Visão geral</h1>
                        <p>Bem-vindo ao SGF Industrial</p>
                    </div>

                    <strong>Administrador</strong>
                </header>
<section class="cards">

    <div class="card">
        <p>Resultado do mês</p>
        <h2>R$ {{ "%.2f"|format(saldo_caixa) }}</h2>
    </div>

    <div class="card">
        <p>Total recebido no mês</p>
        <h2>R$ {{ "%.2f"|format(total_recebido) }}</h2>
    </div>

    <div class="card">
        <p>Total pago no mês</p>
        <h2>R$ {{ "%.2f"|format(total_pago) }}</h2>
    </div>

    <div class="card">
        <p>Total a receber</p>
        <h2>R$ {{ "%.2f"|format(total_a_receber) }}</h2>
    </div>

    <div class="card">
        <p>Total a pagar</p>
        <h2>R$ {{ "%.2f"|format(total_a_pagar) }}</h2>
    </div>

</section>

<section class="panel">

    <h2>Entradas x Saídas — Últimos 6 meses</h2>
    {% if maior_movimento == 0 %}
    <p style="background: #F1F5F9; padding: 18px; border-radius: 8px; color: #64748B; text-align: center;">
        Sem movimentações financeiras neste período.
    </p>
{% endif %}

    {% for item in meses_financeiros %}

    <div style="margin-bottom: 22px;">

        <strong>{{ item.mes }}</strong>

        <p style="margin-top: 10px;">
            Entradas: R$ {{ "%.2f"|format(item.entradas) }}
        </p>

        <div style="background: #E5EAF0; height: 14px; border-radius: 10px; overflow: hidden;">
            <div style="background: #16A36A; height: 14px; width: {{ (item.entradas / maior_movimento * 100) if maior_movimento > 0 else 0 }}%; border-radius: 10px;">
            </div>
        </div>

        <p style="margin-top: 10px;">
            Saídas: R$ {{ "%.2f"|format(item.saidas) }}
        </p>

        <div style="background: #E5EAF0; height: 14px; border-radius: 10px; overflow: hidden;">
            <div style="background: #D9534F; height: 14px; width: {{ (item.saidas / maior_movimento * 100) if maior_movimento > 0 else 0 }}%; border-radius: 10px;">
            </div>
        </div>

    </div>

    {% endfor %}

</section>
<section class="panel">

    <h2>Evolução do Resultado Financeiro</h2>

    {% if maior_resultado == 0 %}

        <p style="background: #F1F5F9; padding: 18px; border-radius: 8px; color: #64748B; text-align: center;">
            Ainda não existem resultados financeiros neste período.
        </p>

    {% else %}

        {% for item in meses_financeiros %}

        <div style="margin-bottom: 20px;">

            <strong>{{ item.mes }}</strong>

            <p style="margin-top: 8px; font-weight: bold; color: {% if item.resultado >= 0 %}#16A36A{% else %}#D9534F{% endif %};">
                R$ {{ "%.2f"|format(item.resultado) }}
            </p>

            <div style="background: #E5EAF0; height: 16px; border-radius: 10px; overflow: hidden;">

                <div style="
                    background: {% if item.resultado >= 0 %}#16A36A{% else %}#D9534F{% endif %};
                    height: 16px;
                    width: {{ (item.resultado|abs / maior_resultado * 100) if maior_resultado > 0 else 0 }}%;
                    border-radius: 10px;">
                </div>

            </div>

        </div>

        {% endfor %}

    {% endif %}

</section>
<section class="panel">

    <h2>Resumo financeiro do mês</h2>

    <p>
        Neste mês, sua empresa recebeu
        <strong>R$ {{ "%.2f"|format(total_recebido) }}</strong>
        e realizou pagamentos de
        <strong>R$ {{ "%.2f"|format(total_pago) }}</strong>.
    </p>

    <p>
        O resultado financeiro do mês foi de
        <strong>R$ {{ "%.2f"|format(saldo_caixa) }}</strong>.
    </p>

    <a class="botao" href="/contas-receber">
        Consultar contas a receber
    </a>

</section>

<section class="card">

    <div style="display:flex; justify-content:space-between;
                align-items:center; gap:15px; flex-wrap:wrap;">

        <div>
            <h2 style="margin:0; color:#17365D; font-size:23px;">
                Controle de Estoque
            </h2>

            <p style="color:#718096; font-size:14px;
                      margin:7px 0 0;">
                Acompanhe os produtos que precisam de reposição.
            </p>
        </div>

        {% if produtos_estoque_baixo %}
            <span style="background:#FFF3D6; color:#946200;
                         padding:8px 14px; border-radius:20px;
                         font-size:13px; font-weight:bold;">
                {{ produtos_estoque_baixo|length }} alerta(s)
            </span>
        {% else %}
            <span style="background:#E6F4EA; color:#237A45;
                         padding:8px 14px; border-radius:20px;
                         font-size:13px; font-weight:bold;">
                0 alertas
            </span>
        {% endif %}

    </div>

    {% if produtos_estoque_baixo %}

        <div style="background:#FFF8E8;
                    border:1px solid #F0D9A0;
                    border-left:4px solid #E2A529;
                    padding:18px;
                    border-radius:8px;
                    margin-top:20px;">

            <strong style="color:#865B13; font-size:16px;">
                ⚠ Reposição necessária
            </strong>

            <p style="color:#795F33; margin:7px 0 0;">
                Existem produtos com estoque baixo.
                Verifique os itens abaixo.
            </p>

        </div>

        <div style="overflow-x:auto; margin-top:18px;
                    border:1px solid #D5DFEA; border-radius:8px;">

            <table style="width:100%; border-collapse:collapse;">

                <thead style="background:#DCE7F3; color:#17365D;">
                    <tr>
                        <th style="padding:14px; text-align:left;
                                   border-bottom:1px solid #C5D3E2;">
                            Produto
                        </th>
                        <th style="padding:14px; text-align:left;
                                   border-bottom:1px solid #C5D3E2;">
                            Código
                        </th>
                        <th style="padding:14px; text-align:center;
                                   border-bottom:1px solid #C5D3E2;">
                            Estoque atual
                        </th>
                        <th style="padding:14px; text-align:center;
                                   border-bottom:1px solid #C5D3E2;">
                            Estoque mínimo
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {% for produto in produtos_estoque_baixo %}
                    <tr style="background:#FFFFFF;">
                        <td style="padding:14px; border-bottom:1px solid #E2E8F0;">
                            {{ produto['nome'] }}
                        </td>
                        <td style="padding:14px; border-bottom:1px solid #E2E8F0;">
                            {{ produto['codigo'] }}
                        </td>
                        <td style="padding:14px; text-align:center;
                                   color:#B45309; font-weight:bold;
                                   border-bottom:1px solid #E2E8F0;">
                            {{ produto['quantidade_estoque'] }}
                        </td>
                        <td style="padding:14px; text-align:center;
                                   border-bottom:1px solid #E2E8F0;">
                            {{ produto['estoque_minimo'] }}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>

            </table>
        </div>

    {% else %}

        <div style="display:flex; align-items:center; gap:15px;
                    background:#F0F8F2;
                    border:1px solid #D0E8D7;
                    border-left:4px solid #2E8B57;
                    border-radius:8px;
                    padding:20px;
                    margin-top:20px;">

            <div style="background:#D8F0DF;
                        color:#237A45;
                        width:40px; height:40px;
                        border-radius:50%;
                        display:flex; align-items:center;
                        justify-content:center;
                        font-size:23px; font-weight:bold;
                        flex-shrink:0;">
                ✓
            </div>

            <div>
                <strong style="color:#237A45; font-size:16px;">
                    Estoque em dia
                </strong>

                <p style="margin:5px 0 0;
                          color:#52725B; font-size:14px;">
                    Nenhum produto precisa de reposição no momento.
                </p>
            </div>

        </div>

    {% endif %}

    <a class="botao" href="/produtos"
       style="display:inline-block; margin-top:20px;">
        Consultar produtos
    </a>

</section>

            </main>
        """,
        saldo_caixa=saldo_caixa,
        total_recebido=total_recebido,
        total_pago=total_pago,
        total_a_receber=total_a_receber,
        total_a_pagar=total_a_pagar,
        meses_financeiros=meses_financeiros,
        maior_movimento=maior_movimento,
        maior_resultado=maior_resultado,
        produtos_estoque_baixo=produtos_estoque_baixo
    )


@app.route("/locacoes", methods=["GET", "POST"])
def locacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        equipamento_id = request.form["equipamento_id"]
        modalidade = request.form["modalidade"]
        data_retirada = request.form["data_retirada"]
        data_prevista = request.form["data_prevista"]
        valor = request.form["valor"]
        observacoes = request.form["observacoes"]
                        # Inicia uma transação protegida no SQLite
        import sqlite3

        try:
            cursor.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as erro:
            conexao.close()

            if "locked" in str(erro).lower() or "busy" in str(erro).lower():
                return "O sistema está ocupado. Tente novamente em alguns instantes.", 503

            raise

        # Verifica se o equipamento está disponível
        equipamento = cursor.execute("""
            SELECT id, situacao
            FROM equipamentos
            WHERE id = ? AND empresa_id = 1
        """, (equipamento_id,)).fetchone()

        # Verifica se já existe uma locação ativa
        locacao_ativa = cursor.execute("""
            SELECT id
            FROM locacoes
            WHERE empresa_id = 1
              AND equipamento_id = ?
              AND situacao = 'Ativa'
            LIMIT 1
        """, (equipamento_id,)).fetchone()

        if (
            equipamento is None
            or equipamento["situacao"] != "Disponível"
            or locacao_ativa is not None
        ):
            conexao.close()
            return "Este equipamento não está disponível para locação.", 409

        cursor.execute("""
            INSERT INTO locacoes (
                empresa_id, cliente_id, equipamento_id,
                   modalidade, data_retirada,
                data_prevista_devolucao, valor,
                situacao, observacoes
            )
                 VALUES (?, ?, ?, ?, ?, ?, ?, 'Ativa', ?)
        """, (
            1, cliente_id, equipamento_id,
            modalidade, data_retirada,
            data_prevista, valor, observacoes
        ))
        # Identifica a locação que acabou de ser cadastrada
        locacao_id = cursor.lastrowid

        cursor.execute("""
            UPDATE equipamentos
            SET situacao = 'Alugado'
            WHERE id = ?
              AND empresa_id = 1
              AND situacao = 'Disponível'
        """, (equipamento_id,))

        # Confirma que o equipamento foi reservado
        if cursor.rowcount != 1:
            conexao.rollback()
            conexao.close()
            return "Este equipamento não está disponível para locação.", 409
        # Cria a cobrança vinculada à locação
        from datetime import date

        cursor.execute("""
            INSERT INTO contas_receber (
                empresa_id,
                cliente_id,
                locacao_id,
                descricao,
                valor,
                data_emissao,
                data_vencimento,
                situacao,
                observacoes
            )
            SELECT ?, ?, ?, ?, ?, ?, ?, 'Pendente', ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM contas_receber
                WHERE empresa_id = ?
                  AND locacao_id = ?
            )
        """, (
            1,
            cliente_id,
            locacao_id,
            f"Locação de equipamento - {modalidade}",
            valor,
            date.today().isoformat(),
            data_prevista,
            observacoes,
            1,
            locacao_id
        ))


        conexao.commit()
        conexao.close()
        return redirect(url_for("locacoes"))

    clientes = cursor.execute(
        "SELECT * FROM clientes WHERE empresa_id = 1 ORDER BY nome"
    ).fetchall()

    equipamentos = cursor.execute("""
        SELECT * FROM equipamentos
        WHERE empresa_id = 1 AND situacao = 'Disponível'
        ORDER BY nome
    """).fetchall()

    registros = cursor.execute("""
        SELECT locacoes.*, clientes.nome AS cliente_nome,
               equipamentos.nome AS equipamento_nome
        FROM locacoes
        JOIN clientes ON clientes.id = locacoes.cliente_id
        JOIN equipamentos ON equipamentos.id = locacoes.equipamento_id
        WHERE locacoes.empresa_id = 1
        ORDER BY locacoes.id DESC
    """).fetchall()


    conexao.close()

    # Data atual para identificar locações atrasadas
    from datetime import date
    hoje = date.today().isoformat()

    return render_template_string("""

    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Locações - SGF Industrial</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background: #F4F5F7;
                margin: 0;
                padding: 30px;
                color: #263445;
            }

            .container {
                max-width: 1200px;
                margin: auto;
            }

            .topo {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 15px;
                margin-bottom: 25px;
                background: #DCE7F3;
                border-left: 5px solid #17365D;
                border-radius: 10px;
                padding: 22px;
            }

            .topo h1 {
                color: #17365D;
                margin: 0 0 6px;
                font-size: 28px;
            }

            .subtitulo {
                color: #718096;
                margin: 0;
                font-size: 14px;
            }

            .voltar {
                display: inline-block;
                background: #FFFFFF;
                color: #17365D;
                padding: 11px 17px;
                border: 1px solid #DCE3EC;
                border-radius: 7px;
                font-weight: bold;
                text-decoration: none;
            }

            .voltar:hover {
                background: #EAF0F7;
            }

            .card {
                background: #FFFFFF;
                border: 1px solid #DCE3EC;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 16px rgba(23, 54, 93, 0.06);
                margin-bottom: 24px;
            }

            .card h2 {
                margin: 0 0 18px;
                color: #17365D;
                font-size: 22px;
            }

            .card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
                flex-wrap: wrap;
                margin-bottom: 18px;
            }

            .badge {
                background: #EAF0F7;
                color: #17365D;
                padding: 8px 12px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: bold;
            }

            .form-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 18px 24px;
            }

            .campo label {
                display: block;
                color: #34465B;
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 8px;
            }

            .campo input,
            .campo select,
            .campo textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #CBD5E0;
                border-radius: 7px;
                background: #FFFFFF;
                font-size: 14px;
                color: #263445;
            }

            .campo textarea {
                min-height: 110px;
                resize: vertical;
            }

            .campo-completo {
                grid-column: 1 / -1;
            }

            .acoes {
                grid-column: 1 / -1;
                display: flex;
                justify-content: flex-start;
            }

            .botao-primario {
                background: #2474B8;
                color: #FFFFFF;
                border: none;
                padding: 12px 20px;
                border-radius: 7px;
                font-weight: bold;
                cursor: pointer;
            }

            .botao-primario:hover {
                background: #175A94;
            }

            .tabela-container {
                overflow-x: auto;
                border: 1px solid #D5DFEA;
                border-radius: 8px;
            }

            .tabela-locacoes {
                width: 100%;
                border-collapse: collapse;
                background: #FFFFFF;
                min-width: 950px;
            }

            .tabela-locacoes th {
                background: #DCE7F3;
                color: #17365D;
                padding: 15px 12px;
                text-align: left;
                border-bottom: 1px solid #C5D3E2;
                font-size: 13px;
            }

            .tabela-locacoes td {
                padding: 15px 12px;
                border-bottom: 1px solid #E2E8F0;
                color: #263445;
                font-size: 14px;
                vertical-align: middle;
            }

            .tabela-locacoes tbody tr:nth-child(even) {
                background: #F8FAFC;
            }

            .tabela-locacoes tbody tr:hover {
                background: #EEF4FA;
            }

            .status-ativa {
                display: inline-block;
                background: #FFF3D6;
                color: #946200;
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: bold;
            }

            .status-finalizada {
                display: inline-block;
                background: #E6F4EA;
                color: #237A45;
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: bold;
            }

            .btn-devolver {
                background: #2474B8;
                color: white;
                padding: 9px 14px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
            }

            .btn-devolver:hover {
                background: #175A94;
            }

            .devolvido {
                color: #237A45;
                font-weight: bold;
            }

            .vazio {
                text-align: center;
                padding: 25px;
                color: #718096;
            }

            @media (max-width: 700px) {
                body {
                    padding: 15px;
                }

                .form-grid {
                    grid-template-columns: 1fr;
                }

                .campo-completo {
                    grid-column: auto;
                }

                .acoes {
                    grid-column: auto;
                }

                .card {
                    padding: 18px;
                }

                .topo h1 {
                    font-size: 23px;
                }
            }
        </style>
    </head>

    <body>
        <div class="container">

            <div class="topo">
                <div>
                    <h1>Locações de Equipamentos</h1>
                    <p class="subtitulo">
                        Registre locações, acompanhe devoluções e controle a disponibilidade dos equipamentos.
                    </p>
                </div>

                <a href="/" class="voltar">← Voltar ao painel</a>
            </div>

            <div class="card">
                <h2>Nova Locação</h2>

                <form method="POST" class="form-grid">

                    <div class="campo">
                        <label>Cliente</label>
                        <select name="cliente_id" required>
                            <option value="">Selecione o cliente</option>
                            {% for cliente in clientes %}
                                <option value="{{ cliente.id }}">{{ cliente.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="campo">
                        <label>Equipamento</label>
                        <select name="equipamento_id" required>
                            <option value="">Selecione o equipamento</option>
                            {% for equipamento in equipamentos %}
                                <option value="{{ equipamento.id }}">{{ equipamento.nome }} - {{ equipamento.modelo }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="campo">
                        <label>Modalidade</label>
                        <select name="modalidade" required>
                            <option value="Diária">Diária</option>
                            <option value="Semanal">Semanal</option>
                            <option value="Mensal">Mensal</option>
                            <option value="Personalizada">Personalizada</option>
                        </select>
                    </div>

                    <div class="campo">
                        <label>Data da retirada</label>
                        <input type="date" name="data_retirada" required>
                    </div>

                    <div class="campo">
                        <label>Previsão de devolução</label>
                        <input type="date" name="data_prevista" required>
                    </div>

                    <div class="campo">
                        <label>Valor da locação</label>
                        <input type="number" step="0.01" name="valor" required>
                    </div>

                    <div class="campo campo-completo">
                        <label>Observações</label>
                        <textarea name="observacoes"></textarea>
                    </div>

                    <div class="acoes">
                        <button type="submit" class="botao-primario">Registrar Locação</button>
                    </div>

                </form>
            </div>

            <div class="card">
                <div class="card-header">
                    <h2>Locações Registradas</h2>
                    <span class="badge">{{ registros|length }} registro(s)</span>
                </div>

                <div class="tabela-container">

<table class="tabela-locacoes">
    <thead>
        <tr>
            <th>Cliente</th>
            <th>Equipamento</th>
            <th>Modalidade</th>
            <th>Retirada</th>
            <th>Devolução prevista</th>
            <th>Valor</th>
            <th>Situação</th>
            <th>Ações</th>
        </tr>
    </thead>

    <tbody>
        {% for registro in registros %}
        <tr>
            <td>{{ registro.cliente_nome }}</td>
            <td>{{ registro.equipamento_nome }}</td>
            <td>{{ registro.modalidade }}</td>

            <td>
                {{ registro.data_retirada[8:10] }}/{{ registro.data_retirada[5:7] }}/{{ registro.data_retirada[0:4] }}
            </td>

            <td>
                {{ registro.data_prevista_devolucao[8:10] }}/{{ registro.data_prevista_devolucao[5:7] }}/{{ registro.data_prevista_devolucao[0:4] }}
            </td>

            <td>
                R$ {{ "%.2f"|format(registro.valor) }}
            </td>

            <td>
                {% if registro.situacao == "Ativa" %}
                    {% if registro.data_prevista_devolucao < hoje %}
                        <span style="background:#FDE8E8;
                                     color:#B42318;
                                     padding:6px 12px;
                                     border-radius:20px;
                                     font-size:12px;
                                     font-weight:bold;">
                            ⚠ Atrasada
                        </span>
                    {% else %}
                        <span class="status-ativa">Ativa</span>
                    {% endif %}
                {% else %}
                    <span class="status-finalizada">Finalizada</span>
                {% endif %}
            </td>

            <td>
                {% if registro.situacao == "Ativa" %}
                    <form method="POST"
                          action="{{ url_for('devolver_locacao', locacao_id=registro.id) }}"
                          onsubmit="return confirm('Confirmar devolução deste equipamento?');">

                        <button type="submit" class="btn-devolver">
                            Registrar devolução
                        </button>
                    </form>
                {% else %}
                    <span class="devolvido">✓ Devolvido</span>
                {% endif %}
            </td>
        </tr>

        {% else %}
        <tr>
            <td colspan="8" class="vazio">
                Nenhuma locação cadastrada até o momento.
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

                </div>
            </div>

        </div>
    </body>
    </html>

    """,
        clientes=clientes,
        equipamentos=equipamentos,
        registros=registros,
        hoje=hoje
    )



# ==========================================
# DEVOLUÇÃO DE EQUIPAMENTOS LOCADOS
# ==========================================

@app.route("/locacoes/devolver/<int:locacao_id>", methods=["POST"])
def devolver_locacao(locacao_id):

    from datetime import date

    conexao = conectar()

    try:
        locacao = conexao.execute("""
            SELECT equipamento_id, situacao
            FROM locacoes
            WHERE id = ? AND empresa_id = 1
        """, (locacao_id,)).fetchone()

        if locacao is None or locacao["situacao"] != "Ativa":
            return redirect(url_for("locacoes"))

        # Finaliza a locação e registra a devolução
        conexao.execute("""
            UPDATE locacoes
            SET situacao = 'Finalizada',
                data_devolucao = ?
            WHERE id = ?
              AND empresa_id = 1
              AND situacao = 'Ativa'
        """, (date.today().isoformat(), locacao_id))

        # Libera o equipamento para outra locação
        conexao.execute("""
            UPDATE equipamentos
            SET situacao = 'Disponível'
            WHERE id = ?
              AND empresa_id = 1
              AND situacao = 'Alugado'
        """, (locacao["equipamento_id"],))

        conexao.commit()

    finally:
        conexao.close()

    return redirect(url_for("locacoes"))

# ==========================================
# CONTAS A RECEBER
# ==========================================

@app.route("/contas-receber", methods=["GET", "POST"])
def contas_receber():

    conexao = conectar()

    if request.method == "POST":

        cliente_id = request.form["cliente_id"]
        descricao = request.form["descricao"]
        valor = float(request.form["valor"])
        data_vencimento = request.form["data_vencimento"]
        observacoes = request.form["observacoes"]

        conexao.execute("""
            INSERT INTO contas_receber (
                empresa_id,
                cliente_id,
                descricao,
                valor,
                data_vencimento,
                situacao,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, 'Pendente', ?)
        """, (
            1,
            cliente_id,
            descricao,
            valor,
            data_vencimento,
            observacoes
        ))

        conexao.commit()
        conexao.close()

        return redirect(url_for("contas_receber"))

    clientes = conexao.execute("""
        SELECT * FROM clientes
        WHERE empresa_id = 1
        ORDER BY nome
    """).fetchall()

    registros = conexao.execute("""
        SELECT contas_receber.*,
               clientes.nome AS cliente_nome
        FROM contas_receber
        JOIN clientes
            ON clientes.id = contas_receber.cliente_id
        WHERE contas_receber.empresa_id = 1
        ORDER BY contas_receber.data_vencimento
    """).fetchall()

    conexao.close()


    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contas a Receber - SGF Industrial</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 35px;
                font-family: Arial, sans-serif;
                background: #e7edf5;
                color: #172c4b;
            }

            .container {
                max-width: 1150px;
                margin: auto;
            }

            h1 {
                margin-bottom: 8px;
                color: #1e3a5f;
            }

            .subtitulo {
                color: #64748b;
                margin-bottom: 28px;
            }
            /* Cabeçalho padronizado - Contas a Receber */
.topo-financeiro {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 25px;
    background: #DCE7F3;
    padding: 22px;
    border-left: 5px solid #17365D;
    border-radius: 9px;
}

.topo-financeiro h1 {
    color: #17365D;
    margin: 0 0 6px;
    font-size: 28px;
}

.topo-financeiro .subtitulo {
    color: #718096;
    margin: 0;
    font-size: 14px;
}

.voltar-financeiro {
    display: inline-block;
    background: #FFFFFF;
    color: #17365D;
    padding: 11px 17px;
    border: 1px solid #DCE3EC;
    border-radius: 7px;
    font-weight: bold;
    text-decoration: none;
}

.voltar-financeiro:hover {
    background: #EAF0F7;
}

            .card {
                background: white;
                padding: 25px;
                border-radius: 14px;
                margin-bottom: 25px;
                box-shadow: 0 3px 12px rgba(0,0,0,0.04);
            }
            /* Cabeçalhos internos de Contas a Receber */
.titulo-secao {
    background: #F4F7FB;
    border-left: 4px solid #17365D;
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 22px;
}

.titulo-secao h2 {
    color: #17365D;
    margin: 0 0 6px;
    font-size: 22px;
}

.titulo-secao p {
    color: #718096;
    margin: 0;
    font-size: 13px;
}

            .form-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 18px;
            }

            .campo {
                display: flex;
                flex-direction: column;
                gap: 7px;
            }

            .campo-completo {
                grid-column: 1 / -1;
            }

            label {
                font-weight: bold;
                font-size: 14px;
            }

            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                font-size: 14px;
            }

            textarea {
                min-height: 75px;
                resize: vertical;
            }

            button {
                background: #1e3a5f;
                color: white;
                border: none;
                padding: 12px 22px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
            }

            button:hover {
                background: #294f7c;
            }

            .tabela-container {
                overflow-x: auto;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                min-width: 750px;
            }
            .tabela-produtos {
    width: 100%;
    border-collapse: collapse;
    min-width: 750px;
    border: 1px solid #B8C8D9;
}

.tabela-produtos th {
    background-color: #DCE6F1;
    color: #17365D;
    border: 1px solid #B8C8D9;
    padding: 14px 12px;
}

.tabela-produtos td {
    background-color: #F4F7FB;
    border: 1px solid #D5DFEA;
    padding: 16px 12px;
    font-size: 13px;
    vertical-align: middle;
}

            th {
                background: #e7edf5;
                text-align: left;
                padding: 14px;
                font-size: 13px;
            }

            td {
                padding: 14px;
                border-bottom: 1px solid #e2e8f0;
                font-size: 14px;
            }

            .pendente {
                color: #b45309;
                font-weight: bold;
            }

            .recebida {
                color: #15803d;
                font-weight: bold;
            }

            .botao-receber {
                padding: 8px 13px;
                font-size: 12px;
                background: #15803d;
            }

            .voltar {
                display: inline-block;
                margin-top: 10px;
                color: #1e3a5f;
                text-decoration: none;
                font-weight: bold;
            }

            @media (max-width: 650px) {
                body {
                    padding: 18px;
                }

                .form-grid {
                    grid-template-columns: 1fr;
                }

                .campo-completo {
                    grid-column: auto;
                }
            }
        </style>
    </head>

    <body>
        <div class="container">

           <div class="topo-financeiro">
    <div>
        <h1>Contas a Receber</h1>
        <p class="subtitulo">
            Gerencie suas cobranças, clientes e recebimentos.
        </p>
    </div>

    <a href="/" class="voltar-financeiro">← Voltar ao painel</a>
</div>

            <div class="card">
                <div class="titulo-secao">
    <h2>Nova cobrança</h2>
    <p>Registre novas cobranças e acompanhe os recebimentos da empresa.</p>
</div>

                <form method="POST">
                    <div class="form-grid">

                        <div class="campo">
                            <label>Cliente:</label>
                            <select name="cliente_id" required>
                                <option value="">Selecione o cliente</option>
                                {% for cliente in clientes %}
                                    <option value="{{ cliente['id'] }}">
                                        {{ cliente['nome'] }}
                                    </option>
                                {% endfor %}
                            </select>
                        </div>

                        <div class="campo">
                            <label>Descrição:</label>
                            <input name="descricao" required>
                        </div>

                        <div class="campo">
                            <label>Valor (R$):</label>
                            <input type="number" step="0.01" min="0.01"
                                   name="valor" required>
                        </div>

                        <div class="campo">
                            <label>Data de vencimento:</label>
                            <input type="date" name="data_vencimento" required>
                        </div>

                        <div class="campo campo-completo">
                            <label>Observações:</label>
                            <textarea name="observacoes"></textarea>
                        </div>

                        <div class="campo campo-completo">
                            <button type="submit">Salvar cobrança</button>
                        </div>

                    </div>
                </form>
            </div>

            <div class="card">
                <div class="titulo-secao">
    <h2>Cobranças cadastradas</h2>
    <p>
        Consulte suas cobranças e acompanhe a situação dos recebimentos.
    </p>
</div>

                <div class="tabela-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Cliente</th>
                                <th>Descrição</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Situação</th>
                                <th>Ação</th>
                            </tr>
                        </thead>

                        <tbody>
                            {% for registro in registros %}
                            <tr>
                                <td>{{ registro['cliente_nome'] }}</td>
                                <td>{{ registro['descricao'] }}</td>
                                <td>R$ {{ "%.2f"|format(registro['valor']) }}</td>
                                <td>{{ registro['data_vencimento'] }}</td>

                                <td>
                                    {% if registro['situacao'] == 'Pendente' %}
                                        <span class="pendente">Pendente</span>
                                    {% else %}
                                        <span class="recebida">Recebida</span>
                                    {% endif %}
                                </td>

                                <td>
                                    {% if registro['situacao'] == 'Pendente' %}
                                        <form method="POST"
                                              action="/contas-receber/receber/{{ registro['id'] }}">
                                            <button class="botao-receber"
                                                    type="submit">
                                                Registrar recebimento
                                            </button>
                                        </form>
                                    {% else %}
                                        <span class="recebida">Concluído</span>
                                    {% endif %}
                                </td>
                            </tr>

                            {% else %}
                            <tr>
                                <td colspan="6">
                                    Nenhuma cobrança cadastrada.
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <a class="voltar" href="/">← Voltar ao Dashboard</a>

        </div>
    </body>
    </html>
    """, clientes=clientes, registros=registros)


# ==========================================
# CONTAS A PAGAR
# ==========================================

@app.route("/contas-pagar", methods=["GET", "POST"])
def contas_pagar():

    conexao = conectar()

    if request.method == "POST":

        descricao = request.form["descricao"]
        categoria = request.form["categoria"]
        fornecedor = request.form["fornecedor"]
        valor = float(request.form["valor"])
        data_vencimento = request.form["data_vencimento"]
        observacoes = request.form["observacoes"]

        conexao.execute("""
            INSERT INTO contas_pagar (
                empresa_id,
                descricao,
                categoria,
                fornecedor,
                valor,
                data_vencimento,
                situacao,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?, 'Pendente', ?)
        """, (
            1,
            descricao,
            categoria,
            fornecedor,
            valor,
            data_vencimento,
            observacoes
        ))

        conexao.commit()
        conexao.close()

        return redirect(url_for("contas_pagar"))

    registros = conexao.execute("""
        SELECT * FROM contas_pagar
        WHERE empresa_id = 1
        ORDER BY data_vencimento
    """).fetchall()

    conexao.close()


    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contas a Pagar - SGF Industrial</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 35px;
                font-family: Arial, sans-serif;
                background: #e7edf5;
                color: #172c4b;
            }

            .container {
                max-width: 1150px;
                margin: auto;
            }

            h1 {
                margin-bottom: 8px;
                color: #1e3a5f;
            }

            .subtitulo {
                color: #64748b;
                margin-bottom: 28px;
            }
            /* Cabeçalho padronizado - Contas a Pagar */
.topo-financeiro {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 25px;
    background: #DCE7F3;
    padding: 22px;
    border-left: 5px solid #17365D;
    border-radius: 9px;
}

.topo-financeiro h1 {
    color: #17365D;
    margin: 0 0 6px;
    font-size: 28px;
}

.topo-financeiro .subtitulo {
    color: #718096;
    margin: 0;
    font-size: 14px;
}

.voltar-financeiro {
    display: inline-block;
    background: #FFFFFF;
    color: #17365D;
    padding: 11px 17px;
    border: 1px solid #DCE3EC;
    border-radius: 7px;
    font-weight: bold;
    text-decoration: none;
}

.voltar-financeiro:hover {
    background: #EAF0F7;
}

            .card {
                background: white;
                padding: 25px;
                border-radius: 14px;
                margin-bottom: 25px;
                box-shadow: 0 3px 12px rgba(0,0,0,0.04);
            }
            /* Cabeçalhos internos de Contas a Pagar */
.titulo-secao {
    background: #F4F7FB;
    border-left: 4px solid #17365D;
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 22px;
}

.titulo-secao h2 {
    color: #17365D;
    margin: 0 0 6px;
    font-size: 22px;
}

.titulo-secao p {
    color: #718096;
    margin: 0;
    font-size: 13px;
}


            .form-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 18px;
            }

            .campo {
                display: flex;
                flex-direction: column;
                gap: 7px;
            }

            .campo-completo {
                grid-column: 1 / -1;
            }

            label {
                font-weight: bold;
                font-size: 14px;
            }

            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                font-size: 14px;
            }

            textarea {
                min-height: 75px;
                resize: vertical;
            }

            button {
                background: #1e3a5f;
                color: white;
                border: none;
                padding: 12px 22px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
            }

            button:hover {
                background: #294f7c;
            }

            .tabela-container {
                overflow-x: auto;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                min-width: 750px;
            }

            th {
                background: #e7edf5;
                text-align: left;
                padding: 14px;
                font-size: 13px;
            }

            td {
                padding: 14px;
                border-bottom: 1px solid #e2e8f0;
                font-size: 14px;
            }

            .pendente {
                color: #b45309;
                font-weight: bold;
            }

            .paga {
                color: #15803d;
                font-weight: bold;
            }

            .botao-baixa {
                padding: 8px 13px;
                font-size: 12px;
                background: #15803d;
            }

            .voltar {
                display: inline-block;
                margin-top: 10px;
                color: #1e3a5f;
                text-decoration: none;
                font-weight: bold;
            }

            @media (max-width: 650px) {
                body {
                    padding: 18px;
                }

                .form-grid {
                    grid-template-columns: 1fr;
                }

                .campo-completo {
                    grid-column: auto;
                }
            }
          .tabela-alertas {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

.tabela-alertas th,
.tabela-alertas td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}

.tabela-alertas th {
    background-color: #f1f5f9;
    color: #1e293b;
    font-weight: bold;
}

.tabela-alertas td {
    color: #334155;
}
        </style>
    </head>

    <body>
        <div class="container">

           <div class="topo-financeiro">
    <div>
        <h1>Contas a Pagar</h1>
        <p class="subtitulo">
            Gerencie suas despesas, fornecedores e pagamentos.
        </p>
    </div>

    <a href="/" class="voltar-financeiro">← Voltar ao painel</a>
</div>

            <div class="card">
                <div class="titulo-secao">
    <h2>Nova despesa</h2>
    <p>Registre suas despesas e acompanhe os pagamentos da empresa.</p>
</div>

                <form method="POST">
                    <div class="form-grid">

                        <div class="campo">
                            <label>Descrição:</label>
                            <input name="descricao" required>
                        </div>

                        <div class="campo">
                            <label>Categoria:</label>
                            <select name="categoria" required>
                                <option value="">Selecione</option>
                                <option>Materiais</option>
                                <option>Fornecedores</option>
                                <option>Aluguel</option>
                                <option>Energia elétrica</option>
                                <option>Água</option>
                                <option>Internet e telefone</option>
                                <option>Impostos</option>
                                <option>Despesas operacionais</option>
                                <option>Outros</option>
                            </select>
                        </div>

                        <div class="campo">
                            <label>Fornecedor:</label>
                            <input name="fornecedor">
                        </div>

                        <div class="campo">
                            <label>Valor (R$):</label>
                            <input type="number" step="0.01" min="0.01"
                                   name="valor" required>
                        </div>

                        <div class="campo">
                            <label>Data de vencimento:</label>
                            <input type="date" name="data_vencimento" required>
                        </div>

                        <div class="campo campo-completo">
                            <label>Observações:</label>
                            <textarea name="observacoes"></textarea>
                        </div>

                        <div class="campo campo-completo">
                            <button type="submit">Salvar despesa</button>
                        </div>

                    </div>
                </form>
            </div>

            <div class="card">
               <div class="titulo-secao">
    <h2>Despesas cadastradas</h2>
    <p>
        Consulte suas despesas e acompanhe a situação dos pagamentos.
    </p>
</div>

                <div class="tabela-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Descrição</th>
                                <th>Categoria</th>
                                <th>Fornecedor</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Situação</th>
                                <th>Ação</th>
                            </tr>
                        </thead>

                        <tbody>
                            {% for registro in registros %}
                            <tr>
                                <td>{{ registro['descricao'] }}</td>
                                <td>{{ registro['categoria'] or '-' }}</td>
                                <td>{{ registro['fornecedor'] or '-' }}</td>
                                <td>R$ {{ "%.2f"|format(registro['valor']) }}</td>
                                <td>{{ registro['data_vencimento'] }}</td>

                                <td>
                                    {% if registro['situacao'] == 'Pendente' %}
                                        <span class="pendente">Pendente</span>
                                    {% else %}
                                        <span class="paga">Paga</span>
                                    {% endif %}
                                </td>

                                <td>
                                    {% if registro['situacao'] == 'Pendente' %}
                                        <form method="POST"
                                              action="/contas-pagar/pagar/{{ registro['id'] }}">
                                            <button class="botao-baixa"
                                                    type="submit">
                                                Dar baixa
                                            </button>
                                        </form>
                                    {% else %}
                                        <span class="paga">Concluído</span>
                                    {% endif %}
                                </td>
                            </tr>

                            {% else %}
                            <tr>
                                <td colspan="7">
                                    Nenhuma despesa cadastrada.
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <a class="voltar" href="/">← Voltar ao Dashboard</a>

        </div>
    </body>
    </html>
    """, registros=registros)

# ==========================================
# REGISTRAR PAGAMENTO
# ==========================================

@app.route("/contas-pagar/pagar/<int:id>", methods=["POST"])
def pagar_conta(id):

    conexao = conectar()

    conexao.execute("""
        UPDATE contas_pagar
        SET situacao = 'Paga',
            data_pagamento = date('now', 'localtime')
        WHERE id = ? AND empresa_id = 1
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("contas_pagar"))
# ==========================================
# REGISTRAR RECEBIMENTO
# ==========================================

@app.route("/contas-receber/receber/<int:id>", methods=["POST"])
def receber_conta(id):

    conexao = conectar()

    conexao.execute("""
        UPDATE contas_receber
        SET situacao = 'Recebida',
            data_recebimento = date('now', 'localtime')
        WHERE id = ? AND empresa_id = 1
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("contas_receber"))


@app.route("/fechamento-mensal")
def fechamento_mensal():

    conexao = conectar()

    mes_atual = request.args.get('mes') or __import__('datetime').date.today().strftime('%Y-%m')

    total_recebido = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_receber
        WHERE empresa_id = 1
        AND situacao = 'Recebida'
        AND data_recebimento LIKE ?
    """, (mes_atual + '%',)).fetchone()[0]

    total_pago = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_pagar
        WHERE empresa_id = 1
        AND situacao = 'Paga'
        AND data_pagamento LIKE ?
    """, (mes_atual + '%',)).fetchone()[0]

    total_a_receber = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_receber
        WHERE empresa_id = 1
        AND situacao = 'Pendente'
    """).fetchone()[0]

    total_a_pagar = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_pagar
        WHERE empresa_id = 1
        AND situacao = 'Pendente'
    """).fetchone()[0]

    resultado = total_recebido - total_pago

    conexao.close()

    return render_template_string("""
    <div style="
        background:#e7edf5;
        min-height:100vh;
        padding:35px;
        font-family:Arial,sans-serif;
        color:#172c4b;
    ">

        <div style="max-width:1100px;margin:auto;">

            <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    flex-wrap:wrap;
    gap:15px;
    background:#DCE7F3;
    padding:22px;
    border-left:5px solid #17365D;
    border-radius:9px;
    margin-bottom:25px;
">
    <div>
        <h1 style="
            color:#17365D;
            font-size:28px;
            margin:0 0 6px;
        ">
            Fechamento Mensal
        </h1>

        <p style="
            color:#718096;
            font-size:14px;
            margin:0;
        ">
            Acompanhe os resultados financeiros da empresa.
        </p>
    </div>

    <a href="/" style="
        display:inline-block;
        background:#FFFFFF;
        color:#17365D;
        padding:11px 17px;
        border:1px solid #DCE3EC;
        border-radius:7px;
        font-weight:bold;
        text-decoration:none;
    ">
        ← Voltar ao painel
    </a>
</div>

            <div style="
                background:white;
                padding:24px;
                border-radius:14px;
                box-shadow:0 3px 12px rgba(0,0,0,0.06);
                margin-bottom:28px;
            ">

                <form method="GET">
                    <label style="font-weight:bold;">
                        Selecione o mês:
                    </label>

                    <input
                        type="month"
                        name="mes"
                        value="{{ mes_atual }}"
                        style="
                            padding:10px;
                            border:1px solid #cbd5e1;
                            border-radius:8px;
                            margin:10px;
                        "
                    >

                    <button type="submit" style="
                        background:#1e3a5f;
                        color:white;
                        border:0;
                        padding:11px 22px;
                        border-radius:8px;
                        cursor:pointer;
                    ">
                        Consultar
                    </button>
                </form>

            </div>

           <div style="
    background:#F4F7FB;
    border-left:4px solid #17365D;
    border-radius:8px;
    padding:16px 18px;
    margin-bottom:22px;
">
    <h2 style="
        color:#17365D;
        margin:0 0 6px;
        font-size:22px;
    ">
        Resumo financeiro
    </h2>

    <p style="
        color:#718096;
        margin:0;
        font-size:13px;
    ">
        Confira os resultados financeiros do mês selecionado.
    </p>
</div>

            <div style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
                gap:18px;
                margin-bottom:30px;
            ">

                <div style="
                    background:white;
                    padding:24px;
                    border-radius:14px;
                    box-shadow:0 3px 12px rgba(0,0,0,0.06);
                    border-left:5px solid #16a34a;
                ">
                    <p style="color:#64748b;">Total recebido</p>
                    <h2 style="color:#15803d;">
                        R$ {{ "%.2f"|format(total_recebido) }}
                    </h2>
                </div>

                <div style="
                    background:white;
                    padding:24px;
                    border-radius:14px;
                    box-shadow:0 3px 12px rgba(0,0,0,0.06);
                    border-left:5px solid #dc2626;
                ">
                    <p style="color:#64748b;">Total pago</p>
                    <h2 style="color:#dc2626;">
                        R$ {{ "%.2f"|format(total_pago) }}
                    </h2>
                </div>

                <div style="
                    background:white;
                    padding:24px;
                    border-radius:14px;
                    box-shadow:0 3px 12px rgba(0,0,0,0.06);
                    border-left:5px solid #2563eb;
                ">
                    <p style="color:#64748b;">Resultado do mês</p>
                    <h2 style="color:#1e3a5f;">
                        R$ {{ "%.2f"|format(resultado) }}
                    </h2>
                </div>

            </div>

          <div style="
    background:#F4F7FB;
    border-left:4px solid #17365D;
    border-radius:8px;
    padding:16px 18px;
    margin-bottom:22px;
">
    <h2 style="
        color:#17365D;
        margin:0 0 6px;
        font-size:22px;
    ">
        Contas pendentes
    </h2>

    <p style="
        color:#718096;
        margin:0;
        font-size:13px;
    ">
        Acompanhe os valores que ainda precisam ser recebidos ou pagos.
    </p>
</div>

            <div style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
                gap:18px;
                margin-bottom:30px;
            ">

                <div style="
                    background:white;
                    padding:24px;
                    border-radius:14px;
                    box-shadow:0 3px 12px rgba(0,0,0,0.06);
                    border-left:5px solid #2563eb;
                ">
                    <p style="color:#64748b;">Total a receber</p>
                    <h2 style="color:#2563eb;">
                        R$ {{ "%.2f"|format(total_a_receber) }}
                    </h2>
                </div>

                <div style="
                    background:white;
                    padding:24px;
                    border-radius:14px;
                    box-shadow:0 3px 12px rgba(0,0,0,0.06);
                    border-left:5px solid #d97706;
                ">
                    <p style="color:#64748b;">Total a pagar</p>
                    <h2 style="color:#d97706;">
                        R$ {{ "%.2f"|format(total_a_pagar) }}
                    </h2>
                </div>

            </div>

            <a href="/" style="
                display:inline-block;
                background:#1e3a5f;
                color:white;
                padding:12px 22px;
                border-radius:8px;
                text-decoration:none;
            ">
                Voltar ao Dashboard
            </a>

        </div>
    </div>
    """,
    total_recebido=total_recebido,
    total_pago=total_pago,
    resultado=resultado,
    total_a_receber=total_a_receber,
    total_a_pagar=total_a_pagar,
    mes_atual=mes_atual
    )

@app.route("/fechamento-anual")
def fechamento_anual():

    conexao = conectar()

    ano_atual = request.args.get('ano') or str(__import__('datetime').date.today().year)

    dados_mensais = conexao.execute("""
        SELECT
            substr(data_recebimento, 6, 2) AS mes,
            SUM(valor) AS total
        FROM contas_receber
        WHERE empresa_id = 1
        AND situacao = 'Recebida'
        AND data_recebimento LIKE ?
        GROUP BY substr(data_recebimento, 6, 2)
    """, (ano_atual + '%',)).fetchall()

    dados_pagamentos = conexao.execute("""
        SELECT
            substr(data_pagamento, 6, 2) AS mes,
            SUM(valor) AS total
        FROM contas_pagar
        WHERE empresa_id = 1
        AND situacao = 'Paga'
        AND data_pagamento LIKE ?
        GROUP BY substr(data_pagamento, 6, 2)
    """, (ano_atual + '%',)).fetchall()

    recebimentos = {int(item['mes']): item['total'] for item in dados_mensais}
    pagamentos = {int(item['mes']): item['total'] for item in dados_pagamentos}

    nomes_meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril',
        'Maio', 'Junho', 'Julho', 'Agosto',
        'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]

    meses = []

    for numero in range(1, 13):
        recebido = recebimentos.get(numero, 0) or 0
        pago = pagamentos.get(numero, 0) or 0

        meses.append({
            'nome': nomes_meses[numero - 1],
            'recebido': recebido,
            'pago': pago,
            'resultado': recebido - pago
        })

    total_recebido = sum(item['recebido'] for item in meses)
    total_pago = sum(item['pago'] for item in meses)
    resultado_anual = total_recebido - total_pago

    total_a_receber = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_receber
        WHERE empresa_id = 1
        AND situacao = 'Pendente'
    """).fetchone()[0]

    total_a_pagar = conexao.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM contas_pagar
        WHERE empresa_id = 1
        AND situacao = 'Pendente'
    """).fetchone()[0]

    conexao.close()

    return render_template_string("""
    <div style="
        background:#e7edf5;
        min-height:100vh;
        padding:35px;
        font-family:Arial,sans-serif;
        color:#172c4b;
    ">

        <div style="max-width:1100px;margin:auto;">

         <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    flex-wrap:wrap;
    gap:15px;
    background:#DCE7F3;
    padding:22px;
    border-left:5px solid #17365D;
    border-radius:9px;
    margin-bottom:25px;
">
    <div>
        <h1 style="
            color:#17365D;
            font-size:28px;
            margin:0 0 6px;
        ">
            Fechamento Anual
        </h1>

        <p style="
            color:#718096;
            font-size:14px;
            margin:0;
        ">
            Acompanhe os resultados financeiros do ano.
        </p>
    </div>

    <a href="/" style="
        display:inline-block;
        background:#FFFFFF;
        color:#17365D;
        padding:11px 17px;
        border:1px solid #DCE3EC;
        border-radius:7px;
        font-weight:bold;
        text-decoration:none;
    ">
        ← Voltar ao painel
    </a>
</div>
            <div style="
                background:white;
                padding:24px;
                border-radius:14px;
                margin-bottom:28px;
            ">

                <form method="GET">
                    <label><strong>Selecione o ano:</strong></label>

                    <input
                        type="number"
                        name="ano"
                        value="{{ ano_atual }}"
                        min="2000"
                        max="2100"
                        style="padding:10px;margin:10px;border-radius:8px;border:1px solid #cbd5e1;"
                    >

                    <button type="submit" style="
                        background:#1e3a5f;
                        color:white;
                        border:0;
                        padding:11px 22px;
                        border-radius:8px;
                        cursor:pointer;
                    ">
                        Consultar
                    </button>
                </form>

            </div>

            <div style="
    background:#F4F7FB;
    border-left:4px solid #17365D;
    border-radius:8px;
    padding:16px 18px;
    margin-bottom:22px;
">
    <h2 style="
        color:#17365D;
        margin:0 0 6px;
        font-size:22px;
    ">
        Resumo do ano
    </h2>

    <p style="
        color:#718096;
        margin:0;
        font-size:13px;
    ">
        Confira os resultados financeiros do ano selecionado.
    </p>
</div>

            <div style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
                gap:18px;
                margin-bottom:30px;
            ">

                <div style="background:white;padding:24px;border-radius:14px;border-left:5px solid #16a34a;">
                    <p>Total recebido</p>
                    <h2 style="color:#15803d;">
                        R$ {{ "%.2f"|format(total_recebido) }}
                    </h2>
                </div>

                <div style="background:white;padding:24px;border-radius:14px;border-left:5px solid #dc2626;">
                    <p>Total pago</p>
                    <h2 style="color:#dc2626;">
                        R$ {{ "%.2f"|format(total_pago) }}
                    </h2>
                </div>

                <div style="background:white;padding:24px;border-radius:14px;border-left:5px solid #2563eb;">
                    <p>Resultado anual</p>
                    <h2 style="color:#1e3a5f;">
                        R$ {{ "%.2f"|format(resultado_anual) }}
                    </h2>
                </div>

            </div>

            <div style="
    background:#F4F7FB;
    border-left:4px solid #17365D;
    border-radius:8px;
    padding:16px 18px;
    margin-bottom:22px;
">
    <h2 style="
        color:#17365D;
        margin:0 0 6px;
        font-size:22px;
    ">
        Contas pendentes
    </h2>

    <p style="
        color:#718096;
        margin:0;
        font-size:13px;
    ">
        Acompanhe os valores que ainda precisam ser recebidos ou pagos.
    </p>
</div>

            <div style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
                gap:18px;
                margin-bottom:30px;
            ">

                <div style="background:white;padding:24px;border-radius:14px;border-left:5px solid #2563eb;">
                    <p>Total a receber</p>
                    <h2>R$ {{ "%.2f"|format(total_a_receber) }}</h2>
                </div>

                <div style="background:white;padding:24px;border-radius:14px;border-left:5px solid #d97706;">
                    <p>Total a pagar</p>
                    <h2>R$ {{ "%.2f"|format(total_a_pagar) }}</h2>
                </div>

            </div>

            <div style="
    background:#F4F7FB;
    border-left:4px solid #17365D;
    border-radius:8px;
    padding:16px 18px;
    margin-bottom:22px;
">
    <h2 style="
        color:#17365D;
        margin:0 0 6px;
        font-size:22px;
    ">
        Resultado por mês
    </h2>

    <p style="
        color:#718096;
        margin:0;
        font-size:13px;
    ">
        Acompanhe os recebimentos, pagamentos e resultados de cada mês.
    </p>
</div>

            <div style="background:white;padding:20px;border-radius:14px;overflow-x:auto;">

                <table style="width:100%;border-collapse:collapse;">
                    <thead>
                        <tr style="background:#e7edf5;">
                            <th style="padding:12px;text-align:left;">Mês</th>
                            <th style="padding:12px;text-align:right;">Recebido</th>
                            <th style="padding:12px;text-align:right;">Pago</th>
                            <th style="padding:12px;text-align:right;">Resultado</th>
                        </tr>
                    </thead>

                    <tbody>
                        {% for item in meses %}
                        <tr>
                            <td style="padding:12px;border-bottom:1px solid #e2e8f0;">
                                {{ item.nome }}
                            </td>
                            <td style="padding:12px;text-align:right;border-bottom:1px solid #e2e8f0;">
                                R$ {{ "%.2f"|format(item.recebido) }}
                            </td>
                            <td style="padding:12px;text-align:right;border-bottom:1px solid #e2e8f0;">
                                R$ {{ "%.2f"|format(item.pago) }}
                            </td>
                            <td style="padding:12px;text-align:right;border-bottom:1px solid #e2e8f0;">
                                R$ {{ "%.2f"|format(item.resultado) }}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>

            </div>

            <a href="/" style="
                display:inline-block;
                background:#1e3a5f;
                color:white;
                padding:12px 22px;
                border-radius:8px;
                text-decoration:none;
                margin-top:25px;
            ">
                Voltar ao Dashboard
            </a>

        </div>
    </div>
    """,
    ano_atual=ano_atual,
    total_recebido=total_recebido,
    total_pago=total_pago,
    resultado_anual=resultado_anual,
    total_a_receber=total_a_receber,
    total_a_pagar=total_a_pagar,
    meses=meses
    )

@app.route("/fluxo-caixa")

def fluxo_caixa():
    hoje = date.today()
    mes_selecionado = request.args.get(
        'mes', hoje.strftime('%Y-%m')
    )

    # Validar o mês selecionado
    try:
        ano, mes = mes_selecionado.split('-')
        ano = int(ano)
        mes = int(mes)

        if mes < 1 or mes > 12 or ano < 1900 or ano > 9999:
            raise ValueError

        mes_selecionado = f"{ano:04d}-{mes:02d}"

    except (ValueError, TypeError):
        ano = hoje.year
        mes = hoje.month
        mes_selecionado = hoje.strftime('%Y-%m')

    data_inicio = f"{ano:04d}-{mes:02d}-01"

    if mes == 12:
        data_fim = f"{ano + 1:04d}-01-01"
    else:
        data_fim = f"{ano:04d}-{mes + 1:02d}-01"

    conexao = conectar()

    recebimentos = conexao.execute("""
        SELECT descricao, valor,
               data_recebimento AS data,
               'Entrada' AS tipo
        FROM contas_receber
        WHERE empresa_id = 1
        AND situacao = 'Recebida'
        AND data_recebimento >= ?
        AND data_recebimento < ?
    """, (data_inicio, data_fim)).fetchall()

    pagamentos = conexao.execute("""
        SELECT descricao, valor,
               data_pagamento AS data,
               'Saída' AS tipo
        FROM contas_pagar
        WHERE empresa_id = 1
        AND situacao = 'Paga'
        AND data_pagamento >= ?
        AND data_pagamento < ?
    """, (data_inicio, data_fim)).fetchall()

    movimentacoes = list(recebimentos) + list(pagamentos)

    movimentacoes.sort(
        key=lambda item: item['data'] or '',
        reverse=True
    )

    total_entradas = sum(
        item['valor'] for item in recebimentos
    )

    total_saidas = sum(
        item['valor'] for item in pagamentos
    )

    saldo = total_entradas - total_saidas

    conexao.close()

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Fluxo de Caixa - SGF Industrial</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 35px;
                font-family: Arial, sans-serif;
                background: #e7edf5;
                color: #172c4b;
            }

            .container {
                max-width: 1150px;
                margin: auto;
            }

            h1 {
                color: #1e3a5f;
                margin-bottom: 8px;
            }

            .subtitulo {
                color: #64748b;
                margin-bottom: 28px;
            }
            /* Cabeçalho principal do Fluxo de Caixa */
.topo-fluxo {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 25px;
    background: #DCE7F3;
    padding: 22px;
    border-left: 5px solid #17365D;
    border-radius: 9px;
}

.topo-fluxo h1 {
    color: #17365D;
    margin: 0 0 6px;
    font-size: 28px;
}

.topo-fluxo .subtitulo {
    color: #718096;
    margin: 0;
    font-size: 14px;
}

.voltar-fluxo {
    display: inline-block;
    background: #FFFFFF;
    color: #17365D;
    padding: 11px 17px;
    border: 1px solid #DCE3EC;
    border-radius: 7px;
    font-weight: bold;
    text-decoration: none;
}

.voltar-fluxo:hover {
    background: #EAF0F7;
}

            .filtro {
                background: white;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 25px;
                display: flex;
                align-items: center;
                gap: 15px;
                flex-wrap: wrap;
            }

            .filtro label {
                font-weight: bold;
            }

            .filtro input {
                padding: 10px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
            }

            .filtro button {
                padding: 10px 18px;
                background: #1e3a5f;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }

            .filtro button:hover {
                background: #294f7c;
            }

            .resumo {
                display: grid;
                grid-template-columns: repeat(
                    auto-fit, minmax(220px, 1fr)
                );
                gap: 18px;
                margin-bottom: 28px;
            }

            .card {
                background: white;
                padding: 24px;
                border-radius: 14px;
                box-shadow: 0 3px 12px rgba(0,0,0,0.04);
            }

            .card p {
                color: #64748b;
                margin-top: 0;
            }

            .entrada {
                border-left: 5px solid #16a34a;
            }

            .saida {
                border-left: 5px solid #dc2626;
            }

            .saldo {
                border-left: 5px solid #2563eb;
            }

            .entrada h2 {
                color: #15803d;
            }

            .saida h2 {
                color: #dc2626;
            }

            .saldo h2 {
                color: #1e3a5f;
            }

            .tabela-container {
                overflow-x: auto;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                min-width: 650px;
            }

            th {
                background: #e7edf5;
                text-align: left;
                padding: 14px;
                font-size: 13px;
            }

            td {
                padding: 14px;
                border-bottom: 1px solid #e2e8f0;
                font-size: 14px;
            }

            .tipo-entrada {
                color: #15803d;
                font-weight: bold;
            }

            .tipo-saida {
                color: #dc2626;
                font-weight: bold;
            }

            .voltar {
                display: inline-block;
                margin-top: 25px;
                color: #1e3a5f;
                text-decoration: none;
                font-weight: bold;
            }

            @media (max-width: 650px) {
                body {
                    padding: 18px;
                }
            }
        </style>
    </head>

    <body>
        <div class="container">

           <div class="topo-fluxo">
    <div>
        <h1>Fluxo de Caixa</h1>
        <p class="subtitulo">
            Acompanhe as entradas, saídas e resultados financeiros da empresa.
        </p>
    </div>

    <a href="/" class="voltar-fluxo">← Voltar ao painel</a>
</div>

            <form method="GET" class="filtro">

                <label for="mes">Selecione o mês:</label>

                <input
                    type="month"
                    id="mes"
                    name="mes"
                    value="{{ mes_selecionado }}"
                    required
                >

                <button type="submit">
                    Consultar
                </button>

            </form>

            <div class="resumo">

                <div class="card entrada">
                    <p>Total de entradas</p>
                    <h2>R$ {{ "%.2f"|format(total_entradas) }}</h2>
                </div>

                <div class="card saida">
                    <p>Total de saídas</p>
                    <h2>R$ {{ "%.2f"|format(total_saidas) }}</h2>
                </div>

                <div class="card saldo">
                    <p>Saldo do período</p>
                    <h2>R$ {{ "%.2f"|format(saldo) }}</h2>
                </div>

            </div>

            <div class="card">

              <div style="
    background:#DCE7F3;
    border-left:4px solid #17365D;
    border-radius:8px;
    padding:16px 18px;
    margin-bottom:22px;
">
    <h2 style="
        color:#17365D;
        margin:0 0 6px;
        font-size:22px;
    ">
        Movimentações financeiras
    </h2>

    <p style="
        color:#718096;
        margin:0;
        font-size:13px;
    ">
        Consulte as entradas e saídas financeiras do período selecionado.
    </p>
</div>

                <div class="tabela-container">

                    <table>
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Descrição</th>
                                <th>Tipo</th>
                                <th>Valor</th>
                            </tr>
                        </thead>

                        <tbody>

                            {% for item in movimentacoes %}

                            <tr>
                                <td>{{ item['data'] }}</td>
                                <td>{{ item['descricao'] }}</td>

                                <td>
                                    {% if item['tipo'] == 'Entrada' %}
                                        <span class="tipo-entrada">Entrada</span>
                                    {% else %}
                                        <span class="tipo-saida">Saída</span>
                                    {% endif %}
                                </td>

                                <td>
                                    R$ {{ "%.2f"|format(item['valor']) }}
                                </td>
                            </tr>

                            {% else %}

                            <tr>
                                <td colspan="4">
                                    Nenhuma movimentação financeira cadastrada neste mês.
                                </td>
                            </tr>

                            {% endfor %}

                        </tbody>
                    </table>

                </div>
            </div>

            <a class="voltar" href="/">
                ← Voltar ao Dashboard
            </a>

        </div>
    </body>
    </html>
    """,
    total_entradas=total_entradas,
    total_saidas=total_saidas,
    saldo=saldo,
    movimentacoes=movimentacoes,
    mes_selecionado=mes_selecionado
    )



if __name__ == "__main__":
    app.run(debug=True)


