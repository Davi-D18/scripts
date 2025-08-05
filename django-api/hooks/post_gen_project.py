#!/usr/bin/env python
import os
import subprocess
import sys
import shutil
from pathlib import Path


def remove_authentication_app():
    """
    Remove o app authentication se a opção use_authentication for "no"
    """
    use_authentication = "{{ cookiecutter.use_authentication }}"
    if use_authentication == "no":
        auth_app_path = Path.cwd() / 'apps' / 'authentication'
        if auth_app_path.exists():
            shutil.rmtree(auth_app_path)

    return


def main():
    project_dir = Path.cwd()
    venv_dir = project_dir / 'venv'
    requirements_file = project_dir / 'requirements-dev.txt'

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