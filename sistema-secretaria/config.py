import os

class Config:
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-municipal-2024'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Banco de dados
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'secretaria.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Sessão e Cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Upload de arquivos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'briefings')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    
    # Criar pasta de upload se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)