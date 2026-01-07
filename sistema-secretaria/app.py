from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from urllib.parse import quote
import os
import secrets

from config import Config
from models import db, User, OrdemServico, Briefing

app = Flask(__name__)
app.config.from_object(Config)

# Configuração adicional para sessões
app.config['SESSION_COOKIE_NAME'] = 'secretaria_session'
app.config['SESSION_COOKIE_SECURE'] = False  # True apenas se usar HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Função auxiliar para verificar extensão de arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ========== ROTAS DE AUTENTICAÇÃO ==========
@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        if current_user.perfil == 'admin' or current_user.perfil == 'tecnico':
            return redirect(url_for('dashboard_ti'))
        elif current_user.perfil == 'comunicacao':
            return redirect(url_for('dashboard_comunicacao'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Bem-vindo(a), {user.nome_completo}!', 'success')
            
            # Redirecionar para o dashboard apropriado
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.perfil == 'admin' or user.perfil == 'tecnico':
                return redirect(url_for('dashboard_ti'))
            elif user.perfil == 'comunicacao':
                return redirect(url_for('dashboard_comunicacao'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

# ========== DASHBOARDS ==========
@app.route('/dashboard/ti', methods=['GET'])
@login_required
def dashboard_ti():
    if current_user.perfil == 'comunicacao':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard_comunicacao'))
    
    # Contadores
    os_prontas = OrdemServico.query.filter_by(status='Aprovado/Pronto').count()
    os_aguardando = OrdemServico.query.filter_by(status='Aguardando Peça').count()
    os_sem_conserto = OrdemServico.query.filter_by(status='Sem Conserto').count()
    os_entrada = OrdemServico.query.filter_by(status='Aguardando Técnico').count()
    os_andamento = OrdemServico.query.filter_by(status='Andamento').count()
    
    # OS recentes (últimas 10)
    if current_user.perfil == 'tecnico':
        os_recentes = OrdemServico.query.filter_by(tecnico_responsavel=current_user.username).order_by(OrdemServico.data_criacao.desc()).limit(10).all()
    else:
        os_recentes = OrdemServico.query.order_by(OrdemServico.data_criacao.desc()).limit(10).all()
    
    return render_template('dashboard_ti.html', 
                         os_prontas=os_prontas,
                         os_aguardando=os_aguardando,
                         os_sem_conserto=os_sem_conserto,
                         os_entrada=os_entrada,
                         os_andamento=os_andamento,
                         os_recentes=os_recentes)

@app.route('/dashboard/comunicacao', methods=['GET'])
@login_required
def dashboard_comunicacao():
    if current_user.perfil != 'comunicacao' and current_user.perfil != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard_ti'))
    
    briefings = Briefing.query.order_by(Briefing.data_criacao.desc()).all()
    return render_template('dashboard_comunicacao.html', briefings=briefings)

# ========== GERENCIAMENTO DE USUÁRIOS ==========
@app.route('/usuarios', methods=['GET'])
@login_required
def usuarios_lista():
    if current_user.perfil != 'admin':
        flash('Apenas administradores podem gerenciar usuários.', 'danger')
        return redirect(url_for('index'))
    
    usuarios = User.query.all()
    return render_template('usuarios_lista.html', usuarios=usuarios)

@app.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
def usuario_novo():
    if current_user.perfil != 'admin':
        flash('Apenas administradores podem criar usuários.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            
            # Verificar se usuário já existe
            if User.query.filter_by(username=username).first():
                flash('Este nome de usuário já existe!', 'danger')
                return render_template('usuario_form.html', usuario=None)
            
            usuario = User(
                username=username,
                nome_completo=request.form.get('nome_completo'),
                perfil=request.form.get('perfil'),
                whatsapp=request.form.get('whatsapp'),
                ativo=True
            )
            usuario.set_password(request.form.get('password'))
            
            db.session.add(usuario)
            db.session.commit()
            
            flash(f'Usuário {username} criado com sucesso!', 'success')
            return redirect(url_for('usuarios_lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar usuário: {str(e)}', 'danger')
    
    return render_template('usuario_form.html', usuario=None)

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def usuario_editar(id):
    if current_user.perfil != 'admin':
        flash('Apenas administradores podem editar usuários.', 'danger')
        return redirect(url_for('index'))
    
    usuario = User.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            usuario.nome_completo = request.form.get('nome_completo')
            usuario.perfil = request.form.get('perfil')
            usuario.whatsapp = request.form.get('whatsapp')
            usuario.ativo = request.form.get('ativo') == 'on'
            
            # Só atualiza senha se fornecida
            nova_senha = request.form.get('password')
            if nova_senha:
                usuario.set_password(nova_senha)
            
            db.session.commit()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('usuarios_lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')
    
    return render_template('usuario_form.html', usuario=usuario)

@app.route('/usuarios/redefinir-senha/<int:id>', methods=['POST'])
@login_required
def usuario_redefinir_senha(id):
    if current_user.perfil != 'admin':
        flash('Apenas administradores podem redefinir senhas.', 'danger')
        return redirect(url_for('index'))
    
    usuario = User.query.get_or_404(id)
    nova_senha = request.form.get('nova_senha')
    
    if nova_senha:
        usuario.set_password(nova_senha)
        db.session.commit()
        flash(f'Senha do usuário {usuario.username} redefinida com sucesso!', 'success')
    else:
        flash('Senha não pode ser vazia!', 'danger')
    
    return redirect(url_for('usuarios_lista'))

# ========== ORDEM DE SERVIÇO ==========
@app.route('/os/nova', methods=['GET', 'POST'])
@login_required
def os_nova():
    if current_user.perfil == 'comunicacao':
        flash('Você não tem permissão para criar OS.', 'danger')
        return redirect(url_for('dashboard_comunicacao'))
    
    if request.method == 'POST':
        try:
            data_abertura = request.form.get('data_abertura')
            if not data_abertura:
                data_abertura = datetime.utcnow().date()
            else:
                data_abertura = datetime.strptime(data_abertura, '%Y-%m-%d').date()
            
            prazo_limite = request.form.get('prazo_limite')
            prazo_limite = datetime.strptime(prazo_limite, '%Y-%m-%d').date() if prazo_limite else None
            
            # Gerar token único para aceite
            token_aceite = secrets.token_urlsafe(16)
            
            os = OrdemServico(
                data_abertura=data_abertura,
                prazo_limite=prazo_limite,
                status='Aguardando Técnico',
                unidade_origem=request.form.get('unidade_origem'),
                local_prestacao=request.form.get('local_prestacao'),
                tecnico_responsavel=None,  # Técnico escolhe
                tipo_equipamento=request.form.get('tipo_equipamento'),
                entregue_por=request.form.get('entregue_por'),
                recebido_por=request.form.get('recebido_por'),
                retirado_por=request.form.get('retirado_por'),
                descricao_servicos=request.form.get('descricao_servicos'),
                observacoes=request.form.get('observacoes'),
                link_aceite=token_aceite
            )
            
            db.session.add(os)
            db.session.commit()
            
            flash(f'Ordem de Serviço #{os.id} criada com sucesso! Aguardando técnico.', 'success')
            return redirect(url_for('os_lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar OS: {str(e)}', 'danger')
    
    return render_template('os_form.html', os=None, tecnicos=None, hoje=datetime.utcnow().date())

@app.route('/os/lista', methods=['GET'])
@login_required
def os_lista():
    if current_user.perfil == 'comunicacao':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard_comunicacao'))
    
    if current_user.perfil == 'tecnico':
        # Técnico vê suas OS e as disponíveis
        minhas_os = OrdemServico.query.filter_by(tecnico_responsavel=current_user.username).order_by(OrdemServico.data_criacao.desc()).all()
        os_disponiveis = OrdemServico.query.filter_by(tecnico_responsavel=None, status='Aguardando Técnico').order_by(OrdemServico.data_criacao.desc()).all()
        return render_template('os_list.html', ordens=minhas_os, os_disponiveis=os_disponiveis)
    else:
        ordens = OrdemServico.query.order_by(OrdemServico.data_criacao.desc()).all()
        return render_template('os_list.html', ordens=ordens, os_disponiveis=None)

@app.route('/os/aceitar-link/<token>', methods=['GET'])
@login_required
def os_aceitar_link(token):
    if current_user.perfil != 'tecnico':
        flash('Apenas técnicos podem aceitar OS.', 'danger')
        return redirect(url_for('os_lista'))
    
    os = OrdemServico.query.filter_by(link_aceite=token).first()
    
    if not os:
        flash('Link inválido ou OS já foi aceita.', 'danger')
        return redirect(url_for('os_lista'))
    
    if os.tecnico_responsavel:
        flash('Esta OS já foi aceita por outro técnico.', 'warning')
        return redirect(url_for('os_lista'))
    
    os.tecnico_responsavel = current_user.username
    os.aceita_por_tecnico = True
    os.status = 'Andamento'
    os.link_aceite = None  # Invalida o link
    db.session.commit()
    
    flash(f'OS #{os.id} aceita com sucesso! Status atualizado para Andamento.', 'success')
    return redirect(url_for('os_editar', id=os.id))

@app.route('/os/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def os_editar(id):
    os = OrdemServico.query.get_or_404(id)
    
    if current_user.perfil == 'comunicacao':
        flash('Você não tem permissão para editar OS.', 'danger')
        return redirect(url_for('dashboard_comunicacao'))
    
    if current_user.perfil == 'tecnico' and os.tecnico_responsavel != current_user.username:
        flash('Você não tem permissão para editar esta OS.', 'danger')
        return redirect(url_for('os_lista'))
    
    if request.method == 'POST':
        try:
            os.status = request.form.get('status')
            os.unidade_origem = request.form.get('unidade_origem')
            os.local_prestacao = request.form.get('local_prestacao')
            os.tipo_equipamento = request.form.get('tipo_equipamento')
            os.entregue_por = request.form.get('entregue_por')
            os.recebido_por = request.form.get('recebido_por')
            os.retirado_por = request.form.get('retirado_por')
            os.descricao_servicos = request.form.get('descricao_servicos')
            os.observacoes = request.form.get('observacoes')
            
            if current_user.perfil == 'admin':
                data_abertura = request.form.get('data_abertura')
                if data_abertura:
                    os.data_abertura = datetime.strptime(data_abertura, '%Y-%m-%d').date()
                
                prazo_limite = request.form.get('prazo_limite')
                if prazo_limite:
                    os.prazo_limite = datetime.strptime(prazo_limite, '%Y-%m-%d').date()
            
            if os.status in ['Aprovado/Pronto', 'Sem Conserto']:
                data_solucao = request.form.get('data_solucao')
                if data_solucao:
                    os.data_solucao = datetime.strptime(data_solucao, '%Y-%m-%d').date()
                else:
                    os.data_solucao = datetime.utcnow().date()
            
            db.session.commit()
            flash('OS atualizada com sucesso!', 'success')
            return redirect(url_for('os_lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar OS: {str(e)}', 'danger')
    
    return render_template('os_form.html', os=os, tecnicos=None, hoje=datetime.utcnow().date())

@app.route('/os/aceitar/<int:id>')
@login_required
def os_aceitar(id):
    if current_user.perfil != 'tecnico':
        flash('Apenas técnicos podem aceitar OS.', 'danger')
        return redirect(url_for('os_lista'))
    
    os = OrdemServico.query.get_or_404(id)
    
    if os.tecnico_responsavel != current_user.username:
        flash('Esta OS não está atribuída a você.', 'danger')
        return redirect(url_for('os_lista'))
    
    os.aceita_por_tecnico = True
    os.status = 'Andamento'
    db.session.commit()
    
    flash(f'OS #{os.id} aceita! Status atualizado para Andamento.', 'success')
    return redirect(url_for('os_lista'))

@app.route('/os/notificar-tecnicos/<int:id>', methods=['GET'])
@login_required
def os_notificar_tecnicos(id):
    if current_user.perfil != 'admin':
        flash('Apenas administradores podem notificar técnicos.', 'danger')
        return redirect(url_for('os_lista'))
    
    os = OrdemServico.query.get_or_404(id)
    
    if os.tecnico_responsavel:
        flash('Esta OS já foi aceita por um técnico.', 'warning')
        return redirect(url_for('os_lista'))
    
    # Buscar TODOS os técnicos ativos
    todos_tecnicos = User.query.filter_by(perfil='tecnico', ativo=True).all()
    
    # Filtrar apenas os que têm WhatsApp cadastrado (não vazio)
    tecnicos = [t for t in todos_tecnicos if t.whatsapp and t.whatsapp.strip()]
    
    if not tecnicos:
        flash('Nenhum técnico ativo com WhatsApp cadastrado encontrado. Cadastre WhatsApp para os técnicos.', 'warning')
        return redirect(url_for('usuarios_lista'))
    
    # Gerar links de WhatsApp
    links_whatsapp = []
    base_url = request.host_url.rstrip('/')
    link_aceite = f"{base_url}/os/aceitar-link/{os.link_aceite}"
    
    # Mensagem individual para técnicos (mais curta)
    mensagem_individual = f"""NOVA OS DISPONIVEL

OS #{os.id}
{os.data_abertura.strftime('%d/%m/%Y')}

Unidade: {os.unidade_origem}
Equip: {os.tipo_equipamento}

Clique no link para aceitar:

{link_aceite}"""
    
    # Mensagem para grupo (otimizada)
    prazo_texto = f"Prazo: {os.prazo_limite.strftime('%d/%m/%Y')}" if os.prazo_limite else ""
    
    mensagem_grupo = f"""NOVA OS DISPONIVEL

OS #{os.id} - {os.data_abertura.strftime('%d/%m/%Y')}
{prazo_texto}

Unidade: {os.unidade_origem}
Equipamento: {os.tipo_equipamento}
Local: {os.local_prestacao}

Descricao:
{os.descricao_servicos[:200]}

Clique para aceitar a OS:

{link_aceite}

Primeiro que clicar fica responsavel!
Disponiveis: {', '.join([t.nome_completo.split()[0] for t in tecnicos])}"""
    
    for tecnico in tecnicos:
        # Remover caracteres não numéricos
        whats_limpo = ''.join(filter(str.isdigit, tecnico.whatsapp))
        
        # Adicionar código do país se necessário
        if len(whats_limpo) == 11:  # DDD + número brasileiro
            whats_limpo = '55' + whats_limpo
        elif len(whats_limpo) == 10:  # Sem DDD
            whats_limpo = '5579' + whats_limpo
        
        # Codificar mensagem individual corretamente
        mensagem_individual_encoded = quote(mensagem_individual)
        
        link_whats = f"https://wa.me/{whats_limpo}?text={mensagem_individual_encoded}"
        links_whatsapp.append({
            'tecnico': tecnico.nome_completo,
            'whatsapp': tecnico.whatsapp,
            'whatsapp_limpo': whats_limpo,
            'link': link_whats
        })
    
    # Codificar mensagem do grupo corretamente
    mensagem_grupo_encoded = quote(mensagem_grupo)
    link_grupo = f"https://wa.me/?text={mensagem_grupo_encoded}"
    
    return render_template('os_notificar.html', 
                         os=os, 
                         links_whatsapp=links_whatsapp, 
                         link_aceite=link_aceite,
                         mensagem_grupo=mensagem_grupo,
                         link_grupo=link_grupo)

@app.route('/os/imprimir/<int:id>', methods=['GET'])
@login_required
def os_imprimir(id):
    os = OrdemServico.query.get_or_404(id)
    
    if current_user.perfil == 'comunicacao':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard_comunicacao'))
    
    if current_user.perfil == 'tecnico' and os.tecnico_responsavel != current_user.username:
        flash('Você não tem permissão para imprimir esta OS.', 'danger')
        return redirect(url_for('os_lista'))
    
    return render_template('os_print.html', os=os, datetime=datetime)

# ========== BRIEFING ==========
@app.route('/briefing/novo', methods=['GET', 'POST'])
@login_required
def briefing_novo():
    if current_user.perfil != 'comunicacao' and current_user.perfil != 'admin':
        flash('Você não tem permissão para criar Briefings.', 'danger')
        return redirect(url_for('dashboard_ti'))
    
    if request.method == 'POST':
        try:
            briefing = Briefing(
                secretaria_responsavel=request.form.get('secretaria_responsavel'),
                responsavel_evento=request.form.get('responsavel_evento'),
                acao_evento=request.form.get('acao_evento'),
                contato_whats=request.form.get('contato_whats'),
                autoridades_presentes=request.form.get('autoridades_presentes'),
                data_hora_local=request.form.get('data_hora_local'),
                qtd_beneficiados=request.form.get('qtd_beneficiados'),
                objetivo_principal=request.form.get('objetivo_principal'),
                descricao_acao=request.form.get('descricao_acao'),
                parceiros_logos=request.form.get('parceiros_logos'),
                solicitacao_profissionais=request.form.get('solicitacao_profissionais'),
                meios_digitais=request.form.get('meios_digitais'),
                meios_impressos=request.form.get('meios_impressos'),
                medidas_material=request.form.get('medidas_material'),
                criado_por=current_user.username
            )
            
            # Upload de imagens
            uploaded_files = []
            if 'imagens' in request.files:
                files = request.files.getlist('imagens')
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        uploaded_files.append(filename)
            
            briefing.imagens_anexo = ','.join(uploaded_files)
            
            db.session.add(briefing)
            db.session.commit()
            
            flash(f'Briefing #{briefing.id} criado com sucesso!', 'success')
            return redirect(url_for('briefing_lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar Briefing: {str(e)}', 'danger')
    
    return render_template('briefing_form.html')

@app.route('/briefing/lista', methods=['GET'])
@login_required
def briefing_lista():
    if current_user.perfil != 'comunicacao' and current_user.perfil != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard_ti'))
    
    briefings = Briefing.query.order_by(Briefing.data_criacao.desc()).all()
    return render_template('briefing_list.html', briefings=briefings)

@app.route('/briefing/ver/<int:id>', methods=['GET'])
@login_required
def briefing_ver(id):
    if current_user.perfil != 'comunicacao' and current_user.perfil != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard_ti'))
    
    briefing = Briefing.query.get_or_404(id)
    return render_template('briefing_view.html', briefing=briefing)

@app.route('/briefing/status/<int:id>/<status>', methods=['GET'])
@login_required
def briefing_status(id, status):
    if current_user.perfil != 'admin':
        flash('Apenas administradores podem alterar status de Briefings.', 'danger')
        return redirect(url_for('briefing_lista'))
    
    briefing = Briefing.query.get_or_404(id)
    briefing.status = status
    db.session.commit()
    
    flash(f'Status do Briefing #{id} atualizado para {status}!', 'success')
    return redirect(url_for('briefing_lista'))

# ========== INICIALIZAÇÃO ==========
def init_db():
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                nome_completo='Administrador do Sistema',
                perfil='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Criar usuário técnico exemplo
        if not User.query.filter_by(username='guilhermetec').first():
            tecnico = User(
                username='guilhermetec',
                nome_completo='Guilherme - Técnico',
                perfil='tecnico'
            )
            tecnico.set_password('guilherme123')
            db.session.add(tecnico)
        
        # Criar usuário comunicação exemplo
        if not User.query.filter_by(username='comunicacao').first():
            com = User(
                username='comunicacao',
                nome_completo='Equipe de Comunicação',
                perfil='comunicacao'
            )
            com.set_password('comunicacao123')
            db.session.add(com)
        
        db.session.commit()
        print("Banco de dados inicializado com sucesso!")
        print("Usuários padrão criados:")
        print("  - admin / admin123")
        print("  - guilhermetec / guilherme123")
        print("  - comunicacao / comunicacao123")

if __name__ == '__main__':
    init_db()
    # Configurar para aceitar conexões de qualquer IP na rede local
    app.run(host='0.0.0.0', port=5000, debug=True)