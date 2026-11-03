
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

    conexao = conectar()

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

            </main>
        """,
        saldo_caixa=saldo_caixa,
        total_recebido=total_recebido,
        total_pago=total_pago,
        total_a_receber=total_a_receber,
        total_a_pagar=total_a_pagar,
        meses_financeiros=meses_financeiros,
        maior_movimento=maior_movimento,
        maior_resultado=maior_resultado
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

            .card {
                background: white;
                padding: 25px;
                border-radius: 14px;
                margin-bottom: 25px;
                box-shadow: 0 3px 12px rgba(0,0,0,0.04);
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

            <h1>Contas a Receber</h1>

            <p class="subtitulo">
                Gerencie suas cobranças, clientes e recebimentos.
            </p>

            <div class="card">
                <h2>Nova cobrança</h2>

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
                <h2>Cobranças cadastradas</h2>

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

            .card {
                background: white;
                padding: 25px;
                border-radius: 14px;
                margin-bottom: 25px;
                box-shadow: 0 3px 12px rgba(0,0,0,0.04);
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
        </style>
    </head>

    <body>
        <div class="container">

            <h1>Contas a Pagar</h1>

            <p class="subtitulo">
                Gerencie suas despesas, fornecedores e pagamentos.
            </p>

            <div class="card">
                <h2>Nova despesa</h2>

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
                <h2>Despesas cadastradas</h2>

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

            <div style="margin-bottom:28px;">
                <h1 style="margin-bottom:8px;">
                    Fechamento Mensal
                </h1>
                <p style="color:#64748b;">
                    Acompanhe os resultados financeiros da empresa.
                </p>
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

            <h2 style="margin-bottom:18px;">
                Resumo financeiro
            </h2>

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

            <h2 style="margin-bottom:18px;">
                Contas pendentes
            </h2>

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

            <h1>Fechamento Anual</h1>

            <p style="color:#64748b;margin:10px 0 28px;">
                Acompanhe os resultados financeiros do ano.
            </p>

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

            <h2 style="margin-bottom:18px;">Resumo do ano</h2>

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

            <h2 style="margin-bottom:18px;">Contas pendentes</h2>

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

            <h2 style="margin-bottom:18px;">Resultado por mês</h2>

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

            <h1>Fluxo de Caixa</h1>

            <p class="subtitulo">
                Acompanhe as entradas, saídas e resultados financeiros da empresa.
            </p>

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

                <h2>Movimentações financeiras</h2>

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


