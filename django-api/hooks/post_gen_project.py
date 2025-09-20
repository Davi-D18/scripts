#!/usr/bin/env python
import os
import subprocess
import sys
import shutil
from pathlib import Path


def format_code_with_make(python_path):
    """Executa o comando 'make format' para formatar o código"""
    print("\n🔧 Formatando código...")
    try:
        # Executa make format usando o Python do ambiente virtual
        subprocess.run(
            [str(python_path), "-m", "black", "."],
            check=True
        )
        subprocess.run(
            [str(python_path), "-m", "isort", "."],
            check=True
        )
        print("✅ Código formatado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Erro ao formatar código: {e}")
        print("Execute manualmente depois: make format")

def remove_documentation_config():
    """
    Remove configurações de documentação se use_documentation for "no"
    """
    use_documentation = "{{ cookiecutter.use_documentation }}"
    if use_documentation == "no":
        # Remover swagger.py
        swagger_path = Path.cwd() / 'core' / 'configs' / 'libs' / 'swagger.py'
        if swagger_path.exists():
            swagger_path.unlink()

def remove_authentication_app():
    """
    Remove o app authentication se a opção use_authentication for "no"
    """
    use_authentication = "{{ cookiecutter.use_authentication }}"
    if use_authentication == "no":
        auth_app_path = Path.cwd() / 'apps' / 'authentication'
        if auth_app_path.exists():
            shutil.rmtree(auth_app_path)

        # Remover jwt.py
        jwt_config_path = Path.cwd() / 'core' / 'configs' / 'libs' / 'jwt.py'
        if jwt_config_path.exists():
            jwt_config_path.unlink()

    return


def main():
    project_dir = Path.cwd()
    venv_dir = project_dir / 'venv'
    requirements_file = project_dir / 'requirements_dev.txt'

    # Create virtual environment
    print('\nCriando ambiente virtual...')
    subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)

    # Get the correct python and pip paths
    if os.name == 'nt':  # Windows
        python_path = venv_dir / 'Scripts' / 'python.exe'
        pip_path = venv_dir / 'Scripts' / 'pip.exe'
    else:  # Unix/Linux
        python_path = venv_dir / 'bin' / 'python'
        pip_path = venv_dir / 'bin' / 'pip'

    print('\nInstalando dependências no ambiente virtual...')
    subprocess.run([str(python_path), '-m', 'pip', 'install', '--upgrade', 'pip', '--no-warn-script-location'], check=True)
    
    subprocess.run([str(python_path), '-m', 'pip', 'install', '-r', str(requirements_file), '--no-warn-script-location'], check=True)
    
    # Remove o app authentication se não for necessário
    remove_authentication_app()
    remove_documentation_config()
    format_code_with_make(python_path)

    mensagem = f"""
    Setup completo!
    Ambiente virtual criado e ativado
    
    Próximos passos:
    1. cd {project_dir.name}
    2. Olhe o arquivo README.md
    
    Happy Coding!     :)
    """

    print(mensagem)

if __name__ == '__main__':
    main()