# Tryton\src\app.py
from .logs.config_logger import configurar_logging
from .docker_manager import DockerManager
from .container_manager import ContainerManager
from .utils.command_utils import countdown

# Configurar el logger
logger = configurar_logging()

CONTAINERS = ["tryton-postgres", "tryton"]

def manage_containers(container_manager, containers):
    """Verifica y gestiona los contenedores Docker."""
    for container in containers:
        if container_manager.check_if_container_exists(container):
            logger.info(f"El contenedor {container} está en ejecución.")
        elif container_manager.check_if_container_stopped(container):
            logger.info(f"El contenedor {container} existe pero no está en ejecución. Iniciando el contenedor.")
            container_manager.start_container(container)
        else:
            logger.error(f"El contenedor {container} no está en ejecución. Creando e iniciando el contenedor.")
            container_manager.create_and_start_container(container)
            if container == "tryton-postgres":
                container_manager.setup_tryton_database()

def main():
    docker_manager = DockerManager()
    container_manager = ContainerManager()
    docker_manager.initialize_docker()
    manage_containers(container_manager, CONTAINERS)
    countdown(10, "Finalizando")
    logger.info("Tryton está listo para usarse. Abre tu navegador en http://localhost:8000 e inicia sesión con tus credenciales.")
