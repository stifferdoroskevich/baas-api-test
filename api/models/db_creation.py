from api import db
from sqlalchemy.dialects import postgresql


class Pessoas(db.Model):
    id_pessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    cpf = db.Column(db.String(255), unique=True)
    data_nascimento = db.Column(db.Date)  # falta definir formato a DDDMMYYYY

    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
# creamos el __repr__ ?


class Contas(db.Model):
    id_conta = db.Column(db.Integer, primary_key=True)
    id_pessoa = db.Column(db.Integer, foreign_key=Pessoas.id_pessoa, nullable=False)
    saldo = db.Column(postgresql.MONEY)  # monetario - limitar negativo ? deposito negativo
    limite_saque_diario = db.Column(db.Numeric)  # monetario - limitar negativo ?
    flag_ativo = db.Column(db.Boolean)  # condicional
    tipo_conta = db.Column(db.Integer)
    data_criacao = db.Column(db.Date)  # formato

    def __init__(self, id_conta, saldo, limite_saque_diario, flag_ativo, tipo_conta, data_criacao):
        self.id_conta = id_conta
        self.saldo = saldo
        self.limite_saque_diario = limite_saque_diario
        self.flag_ativo = flag_ativo
        self.tipo_conta = tipo_conta
        self.data_criacao = data_criacao
# creamos el __repr__ ?
