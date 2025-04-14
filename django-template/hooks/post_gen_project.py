#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path


def main():
    """
    1. Creates virtual environment
    2. Installs requirements
    3. Renames main app directory
    4. Prints next steps
    """

    project_dir = Path.cwd()
    venv_dir = project_dir / 'venv'
    requirements_file = project_dir / 'requirements.txt'

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

    # Install requirements
    print('\nInstalling requirements...')
    subprocess.run([str(pip_path), 'install', '-r', str(requirements_file)], check=True)
    
    print('\n Setup completo! ')
    print('Próximos passos:')
    print(f'1. cd {project_dir.name}')
    print('2. Olhe o arquivo README.md')
    print('\nHappy coding! \n')

if __name__ == '__main__':
    main()
