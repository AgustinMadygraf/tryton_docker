# Tryton\src\app.py
from .docker_manager import DockerManager
from .container_manager import ContainerManager
from .utils.command_utils import countdown
from src.logs.config_logger import LoggerConfigurator
import atexit
from pyngrok import ngrok, conf
from pyngrok.exception import PyngrokNgrokError

logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

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

def start_ngrok():
    try:
        # Configurar ngrok
        conf.get_default().region = "us"  # Cambia la región si es necesario

        # Inicia un túnel HTTP en el puerto 8000
        http_tunnel_8000 = ngrok.connect(8000)
        print(f" * ngrok tunnel \"{http_tunnel_8000.public_url}\" -> \"http://localhost:8000\"")


        # Registrar la función de cierre para asegurarse de que los túneles se cierren correctamente
        atexit.register(ngrok.disconnect, http_tunnel_8000.public_url)

    except PyngrokNgrokError as e:
        print(f"Error al iniciar ngrok: {e}")
        if "ERR_NGROK_3200" in str(e):
            print("Tunnel not found. Please check your ngrok configuration and try again.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def main():
    docker_manager = DockerManager()
    container_manager = ContainerManager()
    docker_manager.initialize_docker()
    manage_containers(container_manager, CONTAINERS)
    start_ngrok()
    logger.info("Tryton está listo para usarse. Abre tu navegador en http://localhost:8000 e inicia sesión con tus credenciales.")
    countdown(10, "Finalizando")
