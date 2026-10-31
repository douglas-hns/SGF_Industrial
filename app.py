
from flask import Flask, render_template_string, request, redirect, url_for
from banco import conectar, criar_tabelas

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
                body {
                    font-family: Arial, sans-serif;
                    background: #F2F5F9;
                    color: #26364A;
                    padding: 30px;
                }

                .container {
                    max-width: 900px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }

                input {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    margin: 8px 0 15px;
                    border: 1px solid #CBD5E0;
                    border-radius: 6px;
                    box-sizing: border-box;
                }

                button {
                    background: #2474B8;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 6px;
                    cursor: pointer;
                }

                .cliente {
                    padding: 15px;
                    border-bottom: 1px solid #E2E8F0;
                }

                a {
                    color: #2474B8;
                    text-decoration: none;
                }
            </style>
        </head>

        <body>
            <div class="container">

                <h1>Cadastro de clientes</h1>

                <form method="POST">

                    <label>Nome do cliente</label>
                    <input name="nome" required>

                    <label>CPF/CNPJ</label>
                    <input name="documento">

                    <label>Telefone</label>
                    <input name="telefone">

                    <label>E-mail</label>
                    <input name="email" type="email">

                    <label>Endereço</label>
                    <input name="endereco">

                    <button type="submit">Salvar cliente</button>

                </form>

                <hr>

                <h2>Clientes cadastrados</h2>

                {% for cliente in lista_clientes %}
                    <div class="cliente">
                        <strong>{{ cliente["nome"] }}</strong><br>
                        Telefone: {{ cliente["telefone"] or "Não informado" }}<br>
                        CPF/CNPJ: {{ cliente["documento"] or "Não informado" }}<br>
                       <a href="{{ url_for('editar_cliente', id=cliente['id']) }}">
    Editar
</a>

<form method="POST"
      action="{{ url_for('excluir_cliente', id=cliente['id']) }}"
      onsubmit="return confirm('Tem certeza que deseja excluir este cliente?');"
      style="display: inline;">

    <button type="submit"
            style="background: #DC3545; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer;">
        Excluir
    </button>

</form>
                    </div>
                {% else %}
                    <p>Nenhum cliente cadastrado.</p>
                {% endfor %}

                <p><a href="/">Voltar ao painel</a></p>

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
            <title>Editar cliente - SGF Industrial</title>
        </head>

        <body style="font-family: Arial; background: #F2F5F9; padding: 30px;">

            <h1>Editar cliente</h1>

            <form method="POST">

                <p>Nome:</p>
                <input name="nome" value="{{ cliente['nome'] }}" required>

                <p>CPF/CNPJ:</p>
                <input name="documento" value="{{ cliente['documento'] or '' }}">

                <p>Telefone:</p>
                <input name="telefone" value="{{ cliente['telefone'] or '' }}">

                <p>E-mail:</p>
                <input name="email" type="email" value="{{ cliente['email'] or '' }}">

                <p>Endereço:</p>
                <input name="endereco" value="{{ cliente['endereco'] or '' }}">

                <br>
                <button type="submit">Salvar alterações</button>

            </form>

            <p><a href="/clientes">Voltar aos clientes</a></p>

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
                body {
                    font-family: Arial, sans-serif;
                    background: #F2F5F9;
                    color: #26364A;
                    padding: 30px;
                }

                .container {
                    max-width: 950px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }

                input, select {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    margin: 8px 0 15px;
                    border: 1px solid #CBD5E0;
                    border-radius: 6px;
                    box-sizing: border-box;
                }

                button {
                    background: #2474B8;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 6px;
                    cursor: pointer;
                }

                .equipamento {
                    padding: 15px;
                    border-bottom: 1px solid #E2E8F0;
                }

                a {
                    color: #2474B8;
                    text-decoration: none;
                }
            </style>
        </head>

        <body>
            <div class="container">

                <h1>Cadastro de equipamentos</h1>

                <form method="POST">

                    <label>Nome do equipamento</label>
                    <input name="nome" required>

                    <label>Marca</label>
                    <input name="marca">

                    <label>Modelo</label>
                    <input name="modelo">

                    <label>Número de série</label>
                    <input name="numero_serie">

                    <label>Tipo de gás detectado</label>
                    <input name="tipo_gas">

                    <label>Situação</label>
                    <select name="situacao">
                        <option>Disponível</option>
                        <option>Alugado</option>
                        <option>Em manutenção</option>
                    </select>

                    <label>Valor da diária (R$)</label>
                    <input type="number" step="0.01" min="0" name="valor_diaria">

                    <label>Valor semanal (R$)</label>
                    <input type="number" step="0.01" min="0" name="valor_semanal">

                    <label>Valor mensal (R$)</label>
                    <input type="number" step="0.01" min="0" name="valor_mensal">

                    <button type="submit">Salvar equipamento</button>

                </form>

                <hr>

                <h2>Equipamentos cadastrados</h2>

                {% for equipamento in lista_equipamentos %}
                    <div class="equipamento">
                        
<strong>{{ equipamento["nome"] }}</strong><br>
Marca: {{ equipamento["marca"] or "Não informada" }}<br>
Modelo: {{ equipamento["modelo"] or "Não informado" }}<br>
Número de série: {{ equipamento["numero_serie"] or "Não informado" }}<br>
Situação: {{ equipamento["situacao"] }}<br>

<a href="{{ url_for('editar_equipamento', id=equipamento['id']) }}">
    Editar equipamento
</a>

<form method="POST"
      action="{{ url_for('excluir_equipamento', id=equipamento['id']) }}"
      onsubmit="return confirm('Tem certeza que deseja excluir este equipamento?');"
      style="display: inline;">

    <button type="submit"
            style="background: #DC3545; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer;">
        Excluir equipamento
    </button>

</form>


                    </div>
                {% else %}
                    <p>Nenhum equipamento cadastrado.</p>
                {% endfor %}

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
# PAINEL PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

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
                    background: #142B45;
                    color: white;
                    position: fixed;
                    padding: 25px 18px;
                }

                .logo {
                    font-size: 22px;
                    font-weight: bold;
                    margin-bottom: 8px;
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
                    padding: 14px;
                    border-radius: 7px;
                    margin-bottom: 8px;
                }

                .menu a:hover {
                    background: #2474B8;
                    color: white;
                }

                .main {
                    margin-left: 250px;
                    padding: 30px;
                }

                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 30px;
                }

                .cards {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin-bottom: 25px;
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
                    background: white;
                    padding: 25px;
                    border-radius: 12px;
                    min-height: 180px;
                }

                .botao {
                    display: inline-block;
                    margin-top: 20px;
                    background: #2474B8;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 7px;
                    text-decoration: none;
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
                    <a href="#">💰 Fluxo de caixa</a>
                    <a href="#">📤 Contas a pagar</a>
                    <a href="#">📥 Contas a receber</a>
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
                        <p>Saldo em caixa</p>
                        <h2>R$ 0,00</h2>
                    </div>

                    <div class="card">
                        <p>Total a receber</p>
                        <h2>R$ 0,00</h2>
                    </div>

                    <div class="card">
                        <p>Total a pagar</p>
                        <h2>R$ 0,00</h2>
                    </div>

                </section>

                <section class="panel">

                    <h2>Resumo financeiro</h2>

                    <p>
                        Seu painel financeiro está pronto para receber
                        os primeiros lançamentos.
                    </p>

                    <a class="botao" href="/clientes">
                        Acessar cadastro de clientes
                    </a>

                </section>

            </main>

        </body>
        </html>
    """)


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

        cursor.execute("""
            UPDATE equipamentos
            SET situacao = 'Alugado'
            WHERE id = ? AND empresa_id = 1
        """, (equipamento_id,))

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

    return render_template_string("""
        <h1>Locações de Equipamentos</h1>

        <h2>Nova Locação</h2>

        <form method="POST">
            <label>Cliente:</label><br>
            <select name="cliente_id" required>
                <option value="">Selecione o cliente</option>
                {% for cliente in clientes %}
                    <option value="{{ cliente.id }}">{{ cliente.nome }}</option>
                {% endfor %}
            </select><br><br>

            <label>Equipamento:</label><br>
            <select name="equipamento_id" required>
                <option value="">Selecione o equipamento</option>
                {% for equipamento in equipamentos %}
                    <option value="{{ equipamento.id }}">{{ equipamento.nome }} - {{ equipamento.modelo }}</option>
                {% endfor %}
            </select><br><br>

            <label>Modalidade:</label><br>
            <select name="modalidade" required>
                <option value="Diária">Diária</option>
                <option value="Semanal">Semanal</option>
                <option value="Mensal">Mensal</option>
                <option value="Personalizada">Personalizada</option>
            </select><br><br>

            <label>Data da retirada:</label><br>
            <input type="date" name="data_retirada" required><br><br>

            <label>Previsão de devolução:</label><br>
            <input type="date" name="data_prevista" required><br><br>

            <label>Valor da locação:</label><br>
            <input type="number" step="0.01" name="valor" required><br><br>

            <label>Observações:</label><br>
            <textarea name="observacoes"></textarea><br><br>

            <button type="submit">Registrar Locação</button>
        </form>

        <hr>

        <h2>Locações Registradas</h2>

        <table border="1" cellpadding="8">
            <tr>
                <th>Cliente</th>
                <th>Equipamento</th>
                <th>Modalidade</th>
                <th>Retirada</th>
                <th>Devolução prevista</th>
                <th>Valor</th>
                <th>Situação</th>
            </tr>

            {% for registro in registros %}
            <tr>
                <td>{{ registro.cliente_nome }}</td>
                <td>{{ registro.equipamento_nome }}</td>
                <td>{{ registro.modalidade }}</td>
                <td>{{ registro.data_retirada }}</td>
                <td>{{ registro.data_prevista_devolucao }}</td>
                <td>R$ {{ "%.2f"|format(registro.valor) }}</td>
                <td>{{ registro.situacao }}</td>
            </tr>
            {% endfor %}
        </table>
      """, clientes=clientes, equipamentos=equipamentos, registros=registros)


if __name__ == "__main__":
    app.run(debug=True)
