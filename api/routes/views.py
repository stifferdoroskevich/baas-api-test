from api import app, db
from flask import request, jsonify
from api.models.db_creation import Contas, Transacoes, Pessoas


@app.route('/')
def home():
    return "Welcome to DOCK!"


@app.route('/pessoas', methods=['GET'])
def get_pessoas():
    pessoas = Pessoas.query.all()
    dados_pessoas = {}
    for pessoa in pessoas:
        dados_pessoas[pessoa.id_pessoa] = {
            'idPessoa': pessoa.id_pessoa,
            'nome': pessoa.nome,
            'cpf': pessoa.cpf,
            'dataNascimento': pessoa.data_nascimento
        }
    return jsonify(dados_pessoas)


@app.route('/pessoas/<id>', methods=['GET'])
def get_pessoa(id):
    pessoa = Pessoas.query.get(id)
    if pessoa:
        dados_pessoa = {id: {
            'idPessoa': pessoa.id_pessoa,
            'nome': pessoa.nome,
            'cpf': pessoa.cpf,
            'dataNascimento': pessoa.data_nascimento
        }}
    return jsonify(dados_pessoa)


@app.route('/contas', methods=['POST'])
def new_conta():
    try:
        id_pessoa = int(request.json['idPessoa'])
        saldo = int(request.json['saldo'])
        limite_saque_diario = int(request.json['limiteSaqueDiario'])
        flag_ativo = bool(request.json['flagAtivo'])
        tipo_conta = int(request.json['tipoConta'])
    except Exception as e:
        return jsonify({"message": "Parametros invalidos. Favor a siga a documentacao: https://bit.ly/documentacao_dock"}), 403

    # Validar limiteSaqueDiario e saldo e tipoConta
    if limite_saque_diario < 0 or tipo_conta not in [0, 1]:
        return jsonify({"message": "Limite de saque diario nao deve ser negativo. Tipo de conta deve ser 0 - Conta Corrente, 1 - Conta Poupança."}), 403
    # Validar se a pessoa existe
    pessoa = Pessoas.query.get(id_pessoa)
    if pessoa:
        conta = Contas(id_pessoa, saldo, limite_saque_diario, flag_ativo, tipo_conta)
        db.session.add(conta)
        db.session.commit()
    else:
        return jsonify({"message": "pessoa invalida"}), 403
    if conta:
        return jsonify({"message": {"idConta": conta.id_conta}}), 200


@app.route('/contas/<id>', methods=['GET'])
def get_saldo(id):
    conta = Contas.query.get(id)
    if conta:
        valor_saldo = {id: {
            'saldo': conta.saldo
        }}
    return jsonify(valor_saldo)


@app.route('/contas/<id>/inativar', methods=['PUT'])
def inativar_conta(id):
    conta = Contas.query.get(id)
    conta.flag_ativo = False
    db.session.commit()

    return "Conta Inativada!"


@app.route('/transacao/deposito', methods=['POST'])
def deposito():
    id_conta = request.json['idConta']
    valor = request.json['valor']

    transacao = Transacoes(id_conta, valor)
    conta = Contas.query.get(id_conta)
    conta.saldo = conta.saldo + valor
    db.session.add(transacao, conta)
    db.session.commit()

    if transacao:
        return "200"


@app.route('/transacao/saque', methods=['POST'])
def saque():
    id_conta = request.json['idConta']
    valor = request.json['valor']
    conta = Contas.query.get(id_conta)

    if valor > conta.saldo:
        return "Saldo Insuficiente"
    if valor > conta.limite_saque_diario:
        return "valor superior ao limite diario"

    conta.saldo = conta.saldo - valor
    transacao = Transacoes(id_conta, -valor)
    db.session.add(transacao, conta)
    db.session.commit()

    if transacao:
        return "200"


@app.route('/transacao/<id>', methods=['GET'])
def get_extrato_conta(id):
    filter_list = [Transacoes.id_conta == id]
    if request.json:
        try:
            data_inicial = request.json['dataInicial']
            data_final = request.json['dataFinal']
            filter_list.extend([Transacoes.data_transacao >= data_inicial, Transacoes.data_transacao <= data_final])
        except Exception as e:
            return jsonify(
                {"message": "Parametros invalidos. Favor a siga a documentacao: https://bit.ly/documentacao_dock"}), 403

    extratos = Transacoes.query.filter(*filter_list)

    resumo_extrato = {}
    for extrato in extratos:
        resumo_extrato[extrato.id_transacao] = {extrato.id_conta: {
            "idConta": extrato.id_conta,
            "idTransacao": extrato.id_transacao,
            "valor": extrato.valor,
            "dataTransacao": extrato.data_transacao
        }
    }
    return jsonify(resumo_extrato)
