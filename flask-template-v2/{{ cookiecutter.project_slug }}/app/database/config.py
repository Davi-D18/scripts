import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_NAME = 'data.db'
DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, SQLITE_DB_NAME)}"

# Instalar o driver do banco de dados correspondente (por exemplo, psycopg2 para PostgreSQL).
# Configurar a aplicação Flask para que ela leia a variável de conexão (por exemplo, usando app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONFIG['DATABASE_URI']).

DATABASE_CONFIG = {
    "DATABASE_URI": DATABASE_URI,
    # "DATABASE_URI": "postgresql://seu_usuario:sua_senha@localhost/nome_do_banco"
}

