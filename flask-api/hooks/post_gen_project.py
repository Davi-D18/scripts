import os
import subprocess
import sys


def remove_directory(target_path):
    """Remove o diretório e seu conteúdo, se existir."""
    if os.path.exists(target_path) and os.path.isdir(target_path):
        # Remove arquivos e subdiretórios (de baixo para cima)
        for root, dirs, files in os.walk(target_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
        # Remove a pasta principal
        os.rmdir(target_path)

def remove_if_empty(path):
    """
    Remove o arquivo se estiver vazio ou remove o diretório se estiver vazio.
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            if os.path.getsize(path) == 0:
                os.remove(path)
        elif os.path.isdir(path):
            # Remove o diretório se estiver vazio
            if not os.listdir(path):
                os.rmdir(path)
                
def main():
    project_dir = os.getcwd()
    venv_dir = os.path.join(project_dir, 'venv')
    
    use_middlewares = "{{ cookiecutter.usar_middlewares }}"
    usar_docs_api = "{{ cookiecutter.usar_docs_api }}"
    
   # Se o usuário não usar middlewares, remova o diretório app/middlewares
    if use_middlewares.lower() == 'n':
        middlewares_dir = os.path.join(project_dir, 'app', 'middlewares')
        remove_directory(middlewares_dir)
    
    # Se o usuário não usar documentação da API, remova o arquivo swagger/teste.yml
    if usar_docs_api.lower() == 'n':
        swagger_dir = os.path.join(project_dir, 'swagger')
        remove_directory(swagger_dir)
        
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

    print("""
        Tudo pronto!
    """)

if __name__ == '__main__':
    main()