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

class NgrokManager:
    """Gestiona la configuración y conexión de ngrok."""

    def __init__(self, logger):
        self.logger = logger

    def start_tunnel(self, port=8000):
        try:
            # Configurar ngrok
            conf.get_default().region = "us"  # Cambia la región si es necesario

            # Inicia un túnel HTTP
            tunnel = ngrok.connect(port)
            print(f" * ngrok tunnel \"{tunnel.public_url}\" -> \"http://localhost:{port}\"")
            
            # Registrar la función de cierre para asegurarse de que los túneles se cierren correctamente
            atexit.register(ngrok.disconnect, tunnel.public_url)
            return tunnel.public_url

        except PyngrokNgrokError as e:
            self.logger.error(f"Error al iniciar ngrok: {e}")
            if "ERR_NGROK_3200" in str(e):
                self.logger.error("Tunnel not found. Please check your ngrok configuration.")
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")



def main():
    docker_manager = DockerManager()
    container_manager = ContainerManager()
    docker_manager.initialize_docker()
    manage_containers(container_manager, CONTAINERS)
    # Iniciar ngrok
    ngrok_manager = NgrokManager(logger)
    public_url = ngrok_manager.start_tunnel(8000)
    logger.info(f"Tryton está listo para usarse en {public_url}. Abre tu navegador e inicia sesión.")

    countdown(3, "Finalizando")
