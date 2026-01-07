from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    nome_completo = db.Column(db.String(200), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)  # admin, tecnico, comunicacao
    whatsapp = db.Column(db.String(20))  # Número do WhatsApp
    ativo = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class OrdemServico(db.Model):
    __tablename__ = 'ordem_servico'
    
    id = db.Column(db.Integer, primary_key=True)
    data_abertura = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    prazo_limite = db.Column(db.Date)
    status = db.Column(db.String(50), nullable=False, default='Aguardando Técnico')
    unidade_origem = db.Column(db.String(200), nullable=False)
    local_prestacao = db.Column(db.String(200), nullable=False)
    tecnico_responsavel = db.Column(db.String(100))
    tipo_equipamento = db.Column(db.String(100), nullable=False)
    entregue_por = db.Column(db.String(100))
    recebido_por = db.Column(db.String(100))
    retirado_por = db.Column(db.String(100))
    descricao_servicos = db.Column(db.Text, nullable=False)
    data_solucao = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    aceita_por_tecnico = db.Column(db.Boolean, default=False)
    link_aceite = db.Column(db.String(100))  # Token único para aceite
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<OS #{self.id} - {self.status}>'


class Briefing(db.Model):
    __tablename__ = 'briefing'
    
    id = db.Column(db.Integer, primary_key=True)
    secretaria_responsavel = db.Column(db.String(200), nullable=False)
    responsavel_evento = db.Column(db.String(200), nullable=False)
    acao_evento = db.Column(db.Text)
    contato_whats = db.Column(db.String(50), nullable=False)
    autoridades_presentes = db.Column(db.Text)
    data_hora_local = db.Column(db.Text)
    qtd_beneficiados = db.Column(db.String(50))
    objetivo_principal = db.Column(db.Text)
    descricao_acao = db.Column(db.Text)
    parceiros_logos = db.Column(db.Text)
    solicitacao_profissionais = db.Column(db.Text)
    meios_digitais = db.Column(db.Text)
    meios_impressos = db.Column(db.Text)
    medidas_material = db.Column(db.Text)
    imagens_anexo = db.Column(db.Text)  # Lista de nomes de arquivos separados por vírgula
    status = db.Column(db.String(50), default='Recebido')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    criado_por = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Briefing #{self.id} - {self.secretaria_responsavel}>'