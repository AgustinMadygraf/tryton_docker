# Tryton\src\app.py
import subprocess
from .logs.config_logger import configurar_logging
from .docker_operations import run_docker_command, check_if_container_exists, check_if_container_stopped, create_and_start_container, start_container, setup_tryton_database
from .utils.command_utils import countdown

# Configurar el logger
logger = configurar_logging()

RETRY_COUNT = 3
CONTAINERS = ["tryton-postgres", "tryton"]

def check_docker():
    while True:
        try:
            run_docker_command(['docker', '--version'], "Docker está instalado.", "Docker no está instalado o no está en el PATH.")
            break
        except Exception as e:
            logger.error(f"Error verificando Docker: {e}")
            countdown(10, "Reintentando verificación de Docker")

def is_docker_running():
    """Verifica si Docker Desktop está en ejecución."""
    for _ in range(RETRY_COUNT):
        try:
            result = subprocess.run(['docker', 'info'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if "Server" in result.stdout.decode():
                logger.info("Docker Desktop está en ejecución.")
                return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error verificando el estado de Docker Desktop: {e.stderr.decode().strip()}")
            countdown(10, "Reintentando verificación del estado de Docker Desktop")
    return False

def initialize_docker():
    """Inicializa Docker y verifica si está en ejecución."""
    check_docker()
    if not is_docker_running():
        logger.error("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")
        raise SystemExit("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")

def manage_containers(containers):
    """Verifica y gestiona los contenedores Docker."""
    for container in containers:
        if check_if_container_exists(container):
            logger.info(f"El contenedor {container} está en ejecución.")
        elif check_if_container_stopped(container):
            logger.info(f"El contenedor {container} existe pero no está en ejecución. Iniciando el contenedor.")
            start_container(container)
        else:
            logger.error(f"El contenedor {container} no está en ejecución. Creando e iniciando el contenedor.")
            create_and_start_container(container)
            if container == "tryton-postgres":
                setup_tryton_database()

def main():
    initialize_docker()
    manage_containers(CONTAINERS)
    countdown(10, "Finalizando")
    logger.info("Tryton está listo para usarse. Abre tu navegador en http://localhost:8000 e inicia sesión con tus credenciales.")
