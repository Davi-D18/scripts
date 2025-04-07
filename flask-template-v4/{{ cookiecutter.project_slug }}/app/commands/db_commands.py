import click
from flask import current_app
from flask.cli import AppGroup
from urllib.parse import urlparse
import subprocess
import os
import shutil

from app.extensions import db as db_extension

def register(app):
    # Pega o grupo 'db' já criado pelo Flask-Migrate ou cria um novo
    db_cli = app.cli.commands.get('db')
    if db_cli is None:
        db_cli = AppGroup('db', help='Comandos relacionados ao banco de dados.')
        app.cli.add_command(db_cli)

    @db_cli.command('drop-all')
    def drop_db():
        """Remove todas as tabelas do banco de dados."""
        with current_app.app_context():
            db_extension.drop_all()
        click.echo('Todas as tabelas foram removidas.')

    @db_cli.command('create-all')
    def create_db():
        """Cria todas as tabelas do banco de dados."""
        with current_app.app_context():
            db_extension.create_all()
        click.echo('Todas as tabelas foram criadas.')

    @db_cli.command('reset')
    def reset_db():
        """Reseta o banco de dados (drop-all + create-all)."""
        drop_db()
        create_db()
        click.echo('Banco de dados resetado.')

    @db_cli.command('backup')
    @click.option('--filename', default='backup.sql', help='Nome do arquivo de backup.')
    @click.option('--path', default='.', help='Diretório para salvar o backup.')
    def backup_db(filename, path):
        """Cria um backup do banco de dados (PostgreSQL, SQLite ou MySQL)."""
        db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
        parsed = urlparse(db_url)
        scheme = parsed.scheme

        dst = os.path.join(path, filename)
        if scheme.startswith('postgresql'):
            cmd = ['pg_dump', db_url, '-f', dst]
            subprocess.run(cmd, check=True)
            click.echo(f'Backup PostgreSQL salvo em {dst}')
        elif scheme.startswith('sqlite'):
            db_path = parsed.path
            shutil.copy(db_path, dst)
            click.echo(f'Backup SQLite copiado para {dst}')
        elif scheme.startswith('mysql'):
            user = parsed.username or ''
            password = parsed.password or ''
            host = parsed.hostname or 'localhost'
            port = parsed.port or 3306
            dbname = parsed.path.lstrip('/')
            cmd = ['mysqldump', '-u', user, f'-p{password}', '-h', host, '-P', str(port), dbname]
            with open(dst, 'w') as f:
                subprocess.run(cmd, stdout=f, check=True)
            click.echo(f'Backup MySQL salvo em {dst}')
        else:
            click.echo('Backup não suportado para este tipo de banco de dados.')

    @db_cli.command('restore')
    @click.option('--filename', required=True, help='Nome do arquivo de backup.')
    @click.option('--path', default='.', help='Diretório do arquivo de backup.')
    def restore_db(filename, path):
        """Restaura o banco de dados a partir de um backup (PostgreSQL, SQLite ou MySQL)."""
        db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
        parsed = urlparse(db_url)
        scheme = parsed.scheme
        backup_file = os.path.join(path, filename)

        if scheme.startswith('postgresql'):
            cmd = ['psql', db_url, '-f', backup_file]
            subprocess.run(cmd, check=True)
            click.echo(f'Restaurado PostgreSQL de {backup_file}')
        elif scheme.startswith('sqlite'):
            db_path = parsed.path
            # Remove o arquivo atual e copia o backup
            if os.path.exists(db_path):
                os.remove(db_path)
            shutil.copy(backup_file, db_path)
            click.echo(f'Restaurado SQLite de {backup_file}')
        elif scheme.startswith('mysql'):
            user = parsed.username or ''
            password = parsed.password or ''
            host = parsed.hostname or 'localhost'
            port = parsed.port or 3306
            dbname = parsed.path.lstrip('/')
            cmd = ['mysql', '-u', user, f'-p{password}', '-h', host, '-P', str(port), dbname]
            with open(backup_file, 'r') as f:
                subprocess.run(cmd, stdin=f, check=True)
            click.echo(f'Restaurado MySQL de {backup_file}')
        else:
            click.echo('Restauração não suportada para este tipo de banco de dados.')

    @db_cli.command('shell')
    def db_shell():
        """Abre um shell interativo do banco (psql, sqlite3 ou mysql)."""
        db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
        parsed = urlparse(db_url)
        scheme = parsed.scheme
        if scheme.startswith('postgresql'):
            os.execvp('psql', ['psql', db_url])
        elif scheme.startswith('sqlite'):
            db_path = parsed.path
            os.execvp('sqlite3', ['sqlite3', db_path])
        elif scheme.startswith('mysql'):
            user = parsed.username or ''
            password = parsed.password or ''
            host = parsed.hostname or 'localhost'
            port = parsed.port or 3306
            dbname = parsed.path.lstrip('/')
            cmd = ['mysql', f'-u{user}', f'-p{password}', '-h', host, '-P', str(port), dbname]
            os.execvp('mysql', cmd)
        else:
            click.echo('Shell não suportado para este tipo de banco de dados.')
