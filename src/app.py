"""
Path: src\app.py
Este módulo se encarga de gestionar los contenedores Docker y mantener la aplicación en ejecución.
"""

from threading import Thread
from src.logs.config_logger import LoggerConfigurator
from .docker_manager import DockerManager
from .container_manager import ContainerManager

logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

CONTAINERS = ["tryton-postgres", "tryton"]

def manage_containers(container_manager, containers):
    """Verifica y gestiona los contenedores Docker."""
    for container in containers:
        if container_manager.check_if_container_exists(container):
            logger.info("El contenedor %s está en ejecución.", container)
        elif container_manager.check_if_container_stopped(container):
            logger.info("""El contenedor %s existe pero
                        no está en ejecución. Iniciando el contenedor.""",container)
            container_manager.start_container(container)
            logger.error("""El contenedor %s no está en ejecución.
                         Creando e iniciando el contenedor.""", container)
            logger.error("""El contenedor %s no está en ejecución.
                         Creando e iniciando el contenedor.""", container)
            container_manager.create_and_start_container(container)
            if container == "tryton-postgres":
                container_manager.setup_tryton_database()



def main():
    """Función principal de la aplicación."""
    docker_manager = DockerManager()
    container_manager = ContainerManager()
    try:
        docker_manager.initialize_docker()
        # Ejecutar el manejo de contenedores en segundo plano
        thread = Thread(target=manage_containers, args=(container_manager, CONTAINERS))
        thread.start()

        url= "localhost:8000"
        logger.info("Tryton está listo para usarse en %s. Abre tu navegador e inicia sesión.", url)
        logger.info("Tryton está listo para usarse en %s. Abre tu navegador e inicia sesión.", url)
        input("Presiona Enter para finalizar...")

    except SystemExit as e:
        print(e)
