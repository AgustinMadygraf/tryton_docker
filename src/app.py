# Tryton\src\app.py
import subprocess
from .logs.config_logger import configurar_logging
from .docker_manager import DockerManager
from .docker_operations import run_docker_command, check_if_container_exists, check_if_container_stopped, create_and_start_container, start_container, setup_tryton_database
from .utils.command_utils import countdown

# Configurar el logger
logger = configurar_logging()

RETRY_COUNT = 3
CONTAINERS = ["tryton-postgres", "tryton"]

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
    docker_manager = DockerManager()
    docker_manager.initialize_docker()
    manage_containers(CONTAINERS)
    countdown(10, "Finalizando")
    logger.info("Tryton está listo para usarse. Abre tu navegador en http://localhost:8000 e inicia sesión con tus credenciales.")
