from api import db, ma


class Pessoas(db.Model):
    id_pessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(70), nullable=False)
    cpf = db.Column(db.String(30), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date)

    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Contas(db.Model):
    id_conta = db.Column(db.Integer, primary_key=True)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoas.id_pessoa'), nullable=False)
    saldo = db.Column(db.Float(precision=2), nullable=False)  # monetario - limitar negativo ? deposito negativo
    limite_saque_diario = db.Column(db.Float(precision=2))  # monetario - limitar negativo ?
    flag_ativo = db.Column(db.Boolean, default=True)
    tipo_conta = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.DateTime)
    # ALTER TABLE public.pessoas ADD data_criacao timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP;

    def __init__(self, id_conta, id_pessoa, saldo, limite_saque_diario, flag_ativo, tipo_conta, data_criacao):
        self.id_conta = id_conta
        self.id_pessoa = id_pessoa
        self.saldo = saldo
        self.limite_saque_diario = limite_saque_diario
        self.flag_ativo = flag_ativo
        self.tipo_conta = tipo_conta
        self.data_criacao = data_criacao


class ContasSchema(ma.Schema):
    class Meta:
        fields = ('id_conta', 'id_pessoa', 'saldo', 'limite_saque_diario', 'flag_ativo', 'tipo_conta', 'data_criacao')


conta_schema = ContasSchema()


class Transacoes(db.Model):
    id_transacao = db.Column(db.Integer, primary_key=True)
    id_conta = db.Column(db.Integer, db.ForeignKey('contas.id_conta'), nullable=False)
    valor = db.Column(db.Float(precision=2), nullable=False)
    data_transacao = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_transacao, id_conta, valor, data_transacao):
        self.id_transacao = id_transacao
        self.id_conta = id_conta
        self.valor = valor
        self.data_transacao = data_transacao


class TransacoesSchema(ma.Schema):
    class Meta:
        fields = ('id_transacao', 'id_conta', 'valor', 'data_transacao')


transacao_schema = TransacoesSchema()
