from api import app, db
from flask import request, jsonify, flash, redirect, url_for
from api.models.db_creation import Pessoas, Contas


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
        print(request.json)
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

        return 'Recibido!!'
        # jsonify(conta)
