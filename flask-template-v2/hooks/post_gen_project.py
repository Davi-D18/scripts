import os
import subprocess
import sys

def main():
    project_dir = os.getcwd()
    venv_dir = os.path.join(project_dir, 'venv')
    
    print("Criando ambiente virtual em 'venv'...")
    subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
    print("Ambiente virtual criado com sucesso!")
    
    # Define os caminhos para o pip e o script de ativação
    if os.name == 'nt':
        pip_executable = os.path.join(venv_dir, 'Scripts', 'pip.exe')
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate.bat')
    else:
        pip_executable = os.path.join(venv_dir, 'bin', 'pip')
        activate_script = os.path.join(venv_dir, 'bin', 'activate')
    
    # Instala as dependências listadas em requirements.txt
    requirements_file = os.path.join(project_dir, 'requirements.txt')
    if os.path.exists(requirements_file):
        print("Instalando dependências...")
        subprocess.check_call([pip_executable, 'install', '-r', requirements_file])
        print("Dependências instaladas com sucesso!")
    else:
        print("Arquivo requirements.txt não encontrado, pulando instalação de dependências.")
    
    # Abre uma nova shell com o ambiente virtual ativado
    print("Abrindo uma nova shell com o ambiente virtual ativado...")
    if os.name == 'nt':
        # No Windows, abre um novo prompt de comando com o ambiente ativado
        subprocess.call(['cmd', '/k', activate_script])
    else:
        # No Linux/macOS, abre um novo terminal (bash) com o ambiente ativado
        subprocess.call(['bash', '-c', f'source {activate_script} && exec bash'])
    
if __name__ == '__main__':
    main()

