from api import app, db
from flask import request, jsonify
from api.models.db_creation import Pessoas, Contas, Transacoes


@app.route('/')
def start():
    return "Welcome to Dock"


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


@app.route('/contas/new', methods=['POST'])
def new_conta():
    if request.method == 'POST':
        id_conta = request.json['idConta']
        id_pessoa = request.json['idPessoa']
        saldo = request.json['saldo']
        limite_saque_diario = request.json['limiteSaqueDiario']
        flag_ativo = request.json['flagAtivo']
        tipo_conta = request.json['tipoConta']
        data_criacao = request.json['dataCriacao']

        conta = Contas(id_conta, id_pessoa, saldo, limite_saque_diario, flag_ativo, tipo_conta, data_criacao)
        db.session.add(conta)
        db.session.commit()

        if conta:
            return "200"


@app.route('/contas/<id>', methods=['GET'])
def get_saldo(id):
    conta = Contas.query.get(id)
    if conta:
        valor_saldo = {id: {
            'saldo': conta.saldo
        }}
    return jsonify(valor_saldo)


@app.route('/transacao/deposito', methods=['POST'])
def deposito():
    if request.method == 'POST':
        id_transacao = request.json['idTransacao']
        id_conta = request.json['idConta']
        valor = request.json['valor']
        data_transacao = request.json['dataTransacao']

        transacao = Transacoes(id_transacao, id_conta, valor, data_transacao)
        db.session.add(transacao)
        db.session.commit()

        if transacao:
            return "200"


@app.route('/transacao/<id>', methods=['GET'])
def get_extrato_conta(id):
    extratos = Transacoes.query.filter(Transacoes.id_conta == id)
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
