"""
Script para popular o banco de dados com dados de exemplo
Execute este script APENAS se quiser ter dados de teste no sistema

Uso: python init_dados_exemplo.py
"""

from app import app, db, User, OrdemServico, Briefing
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def criar_usuarios_exemplo():
    """Cria usuários de exemplo"""
    print("📝 Criando usuários de exemplo...")
    
    usuarios = [
        {
            'username': 'admin',
            'password': 'admin123',
            'nome_completo': 'Administrador do Sistema',
            'telefone': '79999999999',
            'role': 'admin'
        },
        {
            'username': 'guilhermetec',
            'password': 'senha123',
            'nome_completo': 'Guilherme Santos',
            'telefone': '79988887777',
            'role': 'tecnico'
        },
        {
            'username': 'carlostech',
            'password': 'senha123',
            'nome_completo': 'Carlos Eduardo',
            'telefone': '79977776666',
            'role': 'tecnico'
        },
        {
            'username': 'mariacom',
            'password': 'senha123',
            'nome_completo': 'Maria Silva',
            'telefone': '79966665555',
            'role': 'comunicacao'
        }
    ]
    
    for dados in usuarios:
        usuario_existe = User.query.filter_by(username=dados['username']).first()
        if not usuario_existe:
            usuario = User(
                username=dados['username'],
                password=generate_password_hash(dados['password']),
                nome_completo=dados['nome_completo'],
                telefone=dados['telefone'],
                role=dados['role'],
                ativo=True
            )
            db.session.add(usuario)
            print(f"  ✅ Criado: {dados['nome_completo']} ({dados['username']}/{dados['password']})")
        else:
            print(f"  ⚠️  Já existe: {dados['username']}")
    
    db.session.commit()

def criar_os_exemplo():
    """Cria Ordens de Serviço de exemplo"""
    print("\n🔧 Criando Ordens de Serviço de exemplo...")
    
    os_exemplos = [
        {
            'unidade_origem': 'Secretaria de Saúde',
            'local_prestacao': 'Sala de TI - 2º andar',
            'tipo_equipamento': 'Computador',
            'descricao_servicos': 'Computador não liga após queda de energia. LED da fonte acende mas não dá vídeo.',
            'status': 'Entrada',
            'prazo_limite': datetime.now().date() + timedelta(days=3)
        },
        {
            'unidade_origem': 'Secretaria de Educação',
            'local_prestacao': 'Laboratório de Informática',
            'tipo_equipamento': 'Impressora',
            'descricao_servicos': 'Impressora apresentando erro de papel atolado. Já foi verificado o caminho do papel mas continua apresentando erro.',
            'status': 'Andamento',
            'tecnico_responsavel': 'guilhermetec',
            'prazo_limite': datetime.now().date() + timedelta(days=2)
        },
        {
            'unidade_origem': 'Prefeitura - Gabinete',
            'local_prestacao': 'Sala do Prefeito',
            'tipo_equipamento': 'Roteador/Switch',
            'descricao_servicos': 'Internet intermitente. Conexão cai a cada 10 minutos aproximadamente.',
            'status': 'Aguardando Peça',
            'tecnico_responsavel': 'carlostech',
            'prazo_limite': datetime.now().date() + timedelta(days=5)
        },
        {
            'unidade_origem': 'Secretaria de Obras',
            'local_prestacao': 'Recepção',
            'tipo_equipamento': 'Notebook',
            'descricao_servicos': 'Notebook Dell Latitude lento. Windows 10 demorando muito para iniciar e abrir programas.',
            'status': 'Aprovado/Pronto',
            'tecnico_responsavel': 'guilhermetec',
            'prazo_limite': datetime.now().date() + timedelta(days=1),
            'data_solucao': datetime.now().date(),
            'observacoes': 'Realizada limpeza de disco, desfragmentação e atualização de drivers. Sistema operando normalmente.'
        }
    ]
    
    for dados in os_exemplos:
        os = OrdemServico(
            unidade_origem=dados['unidade_origem'],
            local_prestacao=dados['local_prestacao'],
            tipo_equipamento=dados['tipo_equipamento'],
            descricao_servicos=dados['descricao_servicos'],
            status=dados['status'],
            prazo_limite=dados.get('prazo_limite'),
            tecnico_responsavel=dados.get('tecnico_responsavel'),
            data_solucao=dados.get('data_solucao'),
            observacoes=dados.get('observacoes'),
            criado_por='admin'
        )
        db.session.add(os)
        print(f"  ✅ OS: {dados['tipo_equipamento']} - {dados['unidade_origem']}")
    
    db.session.commit()

def criar_briefings_exemplo():
    """Cria Briefings de exemplo"""
    print("\n📢 Criando Briefings de exemplo...")
    
    briefings_exemplos = [
        {
            'secretaria_responsavel': 'Secretaria de Saúde',
            'responsavel_evento': 'Dr. João Silva',
            'acao_evento': 'Campanha de Vacinação contra Dengue',
            'contato_whats': '79988887777',
            'data_hora_local': '20/01/2026, 8h às 17h - Praça Central',
            'qtd_beneficiados': '500 pessoas',
            'objetivo_principal': 'Imunizar a população contra a dengue durante o período de maior incidência da doença.',
            'descricao_acao': 'Campanha itinerante de vacinação com equipes médicas. Serão disponibilizadas 3 tendas com profissionais de saúde para aplicação das vacinas.',
            'solicitacao_profissionais': 'Fotógrafo, Videomaker',
            'meios_digitais': 'Instagram, Facebook, Site da Prefeitura',
            'status': 'Recebido'
        },
        {
            'secretaria_responsavel': 'Secretaria de Educação',
            'responsavel_evento': 'Profª Maria Santos',
            'acao_evento': 'Inauguração da Biblioteca Municipal',
            'contato_whats': '79977776666',
            'data_hora_local': '25/01/2026, 10h - Biblioteca Municipal',
            'qtd_beneficiados': '200 alunos',
            'objetivo_principal': 'Inaugurar oficialmente o novo espaço de leitura da cidade.',
            'descricao_acao': 'Cerimônia de inauguração com presença de autoridades, apresentação cultural dos alunos e abertura para visitação.',
            'autoridades_presentes': 'Prefeito, Secretário de Educação, Vereadores',
            'solicitacao_profissionais': 'Fotógrafo, Videomaker, Designer (convites)',
            'meios_digitais': 'Instagram, Facebook, WhatsApp',
            'meios_impressos': 'Banner 2x1m para entrada, Convites impressos (100 unidades)',
            'status': 'Em Produção'
        }
    ]
    
    for dados in briefings_exemplos:
        briefing = Briefing(
            secretaria_responsavel=dados['secretaria_responsavel'],
            responsavel_evento=dados['responsavel_evento'],
            acao_evento=dados['acao_evento'],
            contato_whats=dados['contato_whats'],
            data_hora_local=dados.get('data_hora_local'),
            qtd_beneficiados=dados.get('qtd_beneficiados'),
            objetivo_principal=dados.get('objetivo_principal'),
            descricao_acao=dados.get('descricao_acao'),
            autoridades_presentes=dados.get('autoridades_presentes'),
            solicitacao_profissionais=dados.get('solicitacao_profissionais'),
            meios_digitais=dados.get('meios_digitais'),
            meios_impressos=dados.get('meios_impressos'),
            status=dados['status'],
            criado_por='mariacom'
        )
        db.session.add(briefing)
        print(f"  ✅ Briefing: {dados['acao_evento']}")
    
    db.session.commit()

def main():
    """Função principal"""
    print("="*60)
    print("🚀 INICIANDO POPULAÇÃO DO BANCO DE DADOS COM DADOS DE EXEMPLO")
    print("="*60)
    print()
    
    with app.app_context():
        # Criar as tabelas se não existirem
        db.create_all()
        
        # Popular com dados de exemplo
        criar_usuarios_exemplo()
        criar_os_exemplo()
        criar_briefings_exemplo()
        
        print()
        print("="*60)
        print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
        print("="*60)
        print()
        print("📋 USUÁRIOS CRIADOS:")
        print("  • admin / admin123 (Administrador)")
        print("  • guilhermetec / senha123 (Técnico)")
        print("  • carlostech / senha123 (Técnico)")
        print("  • mariacom / senha123 (Comunicação)")
        print()
        print("🔧 ORDENS DE SERVIÇO: 4 exemplos")
        print("📢 BRIEFINGS: 2 exemplos")
        print()
        print("🌐 Inicie o sistema com: python app.py")
        print("🔗 Acesse: http://localhost:5000")
        print()

if __name__ == '__main__':
    main()