import subprocess
from .utils.command_utils import countdown
from src.logs.config_logger import LoggerConfigurator

logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

class DockerManager:
    RETRY_COUNT = 3

    def __init__(self):
        self.logger = logger

    def check_docker(self):
        while True:
            try:
                self.run_docker_command(['docker', '--version'], "Docker está instalado.", "Docker no está instalado o no está en el PATH.")
                break
            except Exception as e:
                self.logger.error(f"Error verificando Docker: {e}")
                countdown(10, "Reintentando verificación de Docker")

    def is_docker_running(self):
        """Verifica si Docker Desktop está en ejecución."""
        for _ in range(self.RETRY_COUNT):
            try:
                result = subprocess.run(['docker', 'info'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if "Server" in result.stdout.decode():
                    self.logger.info("Docker Desktop está en ejecución.")
                    return True
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error verificando el estado de Docker Desktop: {e.stderr.decode().strip()}")
                countdown(10, "Reintentando verificación del estado de Docker Desktop")
        return False

    def initialize_docker(self):
        """Inicializa Docker y verifica si está en ejecución."""
        self.check_docker()
        if not self.is_docker_running():
            self.logger.error("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")
            raise SystemExit("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")

    def run_docker_command(self, docker_command, success_message, error_message):
        try:
            result = subprocess.run(docker_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.info(success_message)
            return result.stdout.decode()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"{error_message}: {e.stderr.decode().strip()}")
            raise
