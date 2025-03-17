import os
import subprocess
import sys


def remove_middlewares_directory(project_dir):
    """Remove a pasta middlewares e seu conteúdo se existir."""
    middlewares_dir = os.path.join(project_dir, 'app', 'middlewares')
    if os.path.exists(middlewares_dir):
        # Remove arquivos e subdiretórios primeiro
        for root, dirs, files in os.walk(middlewares_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
                print(f"Pasta removida: {dir_path}")
        # Remove a pasta principal
        os.rmdir(middlewares_dir)
        print(f"Pasta 'middlewares' removida: {middlewares_dir}")

def main():
    project_dir = os.getcwd()
    venv_dir = os.path.join(project_dir, 'venv')
    
    use_middlewares = "{{ cookiecutter.usar_middlewares }}"
    
    if use_middlewares.lower() == 'n':
        remove_middlewares_directory(project_dir)
    
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
    if os.path.exists(requirements_file) and os.stat(requirements_file).st_size > 0:
        print("Instalando dependências...")
        subprocess.check_call([pip_executable, 'install', '-r', requirements_file])
        print("Dependências instaladas com sucesso!")
    else:
        print("Nenhum requirements.txt válido encontrado, pulando instalação de dependências.")

    # Abre uma nova shell com o ambiente virtual ativado
    print("Abrindo uma nova shell com o ambiente virtual ativado...")
    if os.name == 'nt':
        subprocess.call(['cmd', '/k', activate_script])
    else:
        subprocess.call(['bash', '--init-file', activate_script])

if __name__ == '__main__':
    main()
