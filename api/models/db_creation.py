from api import db


class Pessoas(db.Model):
    id_pessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    cpf = db.Column(db.String(255))
    data_nascimento = db.Column(db.Date)

    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
