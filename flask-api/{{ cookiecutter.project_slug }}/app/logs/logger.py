import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    """Configura o sistema de logs com base nas variáveis do app.config."""
    
    # Configuração do nível de log
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    # Se LOG_FILE estiver definido, salva em arquivo
    if app.config['LOG_FILE']:
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=app.config['LOG_MAX_BYTES'],
            backupCount=app.config['LOG_BACKUP_COUNT']
        )
        
        detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s\nContext: %(details)s'
        )
        file_handler.setFormatter(detailed_formatter)
        app.logger.addHandler(file_handler)
    
    # Adiciona log no console em desenvolvimento
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(console_handler)