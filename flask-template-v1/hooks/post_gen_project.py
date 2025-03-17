import os
import shutil
import subprocess
import sys

def remove_empty_dirs(path):
    # Percorre a árvore de diretórios de baixo para cima e remove os vazios
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        if not dirnames and not filenames:
            print(f"Removendo diretório vazio: {dirpath}")
            os.rmdir(dirpath)

def remove_dir_if_exists(path, description):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Removendo {description} por opção do usuário.")
        except Exception as e:
            print(f"❌ Erro ao remover {description}: {e}")

def main():
    project_dir = os.getcwd()
    remove_empty_dirs(project_dir)
    
    # Verifica as opções definidas no cookiecutter via variáveis de ambiente
    use_middleware = os.environ.get("cookiecutter_use_middleware", "n").lower() == "y"
    use_logging = os.environ.get("cookiecutter_use_logging", "n").lower() == "y"
    
    # Se o usuário não quiser middlewares, remove a pasta correspondente
    if not use_middleware:
        middleware_dir = os.path.join(project_dir, "app", "middlewares")
        remove_dir_if_exists(middleware_dir, "diretório de middlewares")
    
    # Se o usuário não quiser logging, remove a pasta correspondente
    if not use_logging:
        logging_dir = os.path.join(project_dir, "app", "logging")
        remove_dir_if_exists(logging_dir, "diretório de logging")
    
    # Criação do ambiente virtual
    setup_venv = os.environ.get("cookiecutter_setup_venv", "y").lower() == "y"
    if setup_venv:
        print("Criando ambiente virtual...")
        venv_path = os.path.join(project_dir, "venv")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print(f"✅ Ambiente virtual criado em {venv_path}")
        except Exception as e:
            print(f"❌ Erro ao criar ambiente virtual: {e}")
    
    # Instalação das dependências
    install_deps = os.environ.get("cookiecutter_install_dependencies", "y").lower() == "y"
    if install_deps:
        print("Instalando dependências...")
        pip_path = os.path.join(project_dir, "venv", "bin", "pip") if os.path.exists(os.path.join(project_dir, "venv", "bin", "pip")) else "pip"
        requirements_path = os.path.join(project_dir, "requirements.txt")
        try:
            subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
            print("✅ Dependências instaladas!")
        except Exception as e:
            print(f"❌ Erro ao instalar dependências: {e}")
    
    # Configuração do banco de dados (se solicitado)
    run_migrations = os.environ.get("cookiecutter_run_db_migrations", "n").lower() == "y"
    use_db = os.environ.get("cookiecutter_use_db", "n").lower() == "y"
    if use_db and run_migrations:
        print("Configurando banco de dados...")
        flask_path = os.path.join(project_dir, "venv", "bin", "flask") if os.path.exists(os.path.join(project_dir, "venv", "bin", "flask")) else "flask"
        migrations_dir = os.path.join(project_dir, "migrations")
        if os.path.exists(migrations_dir):
            try:
                shutil.rmtree(migrations_dir)
                print("♻️  Diretório migrations antigo removido")
            except Exception as e:
                print(f"❌ Erro ao remover migrations: {e}")
        commands = [
            [flask_path, "--app", "run.py", "db", "init"],
            [flask_path, "--app", "run.py", "db", "migrate", "-m", "Initial migration"],
            [flask_path, "--app", "run.py", "db", "upgrade"]
        ]
        for cmd in commands:
            try:
                subprocess.run(cmd, check=True, cwd=project_dir)
            except Exception as e:
                print(f"❌ Erro ao executar comando: {' '.join(cmd)}. Erro: {e}")
        print("✅ Banco de dados configurado!")
    
    print("\n🎉 Projeto gerado com sucesso!")
    print("Para começar a trabalhar, entre no diretório do projeto e ative o ambiente virtual, se necessário.")

if __name__ == '__main__':
    main()
