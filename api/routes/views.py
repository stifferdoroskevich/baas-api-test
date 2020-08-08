from api import app, db
from flask import request, Blueprint, render_template, jsonify, flash, redirect, url_for

from api.models.db_creation import Pessoas


@app.route('/')
def start():
    return "Dock is Here"


@app.route('/pessoas')
def get_pessoas():
    pessoas = Pessoas.query.all()
    res = {}
    for pessoa in pessoas:
        res[pessoa.id_pessoa] = {
            'idPessoa': pessoa.id_pessoa,
            'nome': pessoa.nome,
            'cpf': pessoa.cpf,
            'dataNascimento': pessoa.data_nascimento
        }
    return jsonify(res)
