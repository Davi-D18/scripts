#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path

use_poetry = "{{ cookiecutter.use_poetry }}"

def main():
    project_dir = Path.cwd()
    venv_dir = project_dir / '.venv'
    python_path = venv_dir / 'bin' / 'python'

    if use_poetry == "no":
        requirements_file = project_dir / 'requirements_dev.txt'
        # Create virtual environment
        print('\nCriando ambiente virtual...')
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)

        # Get the correct python and pip paths
        if os.name == 'nt':  # Windows
            python_path = venv_dir / 'Scripts' / 'python.exe'

        print('\nInstalando dependências no ambiente virtual...')
        subprocess.run([str(python_path), '-m', 'pip', 'install', '--upgrade', 'pip', '--no-warn-script-location'], check=True)
    
        subprocess.run([str(python_path), '-m', 'pip', 'install', '-r', str(requirements_file), '--no-warn-script-location'], check=True)

        mensagem = f"""
        Setup completo!
        Ambiente virtual criado e ativado
        
        Próximos passos:
        1. cd {project_dir.name}
        2. Olhe o arquivo README.md
        
        Happy Coding!     :)
        """
        print(mensagem)

    else:
        mensagem = f"""
        Setup completo!
        crie o ambiente virtual e instale as dependências
        
        Próximos passos:
        1. cd {project_dir.name}
        2. Olhe o arquivo README.md
        
        Happy Coding!     :)
        """
        print(mensagem)


if __name__ == '__main__':
    main()