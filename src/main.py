import os
import subprocess
from logs.config_logger import configurar_logging

# Configurar el logger
logger = configurar_logging()

def check_docker():
    """Verifica si Docker está instalado y en ejecución."""
    try:
        subprocess.run(['docker', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Docker está instalado.")
    except subprocess.CalledProcessError:
        logger.error("Docker no está instalado o no está en el PATH.")
        raise SystemExit("Docker no está instalado o no está en el PATH.")

def is_docker_running():
    """Verifica si Docker Desktop está en ejecución."""
    try:
        result = subprocess.run(['docker', 'info'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "Server" in result.stdout.decode():
            logger.info("Docker Desktop está en ejecución.")
            return True
        else:
            logger.error("Docker Desktop no está en ejecución.")
            return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error verificando el estado de Docker Desktop: {e.stderr.decode().strip()}")
        return False

def start_container(container_name):
    """Inicia un contenedor Docker dado su nombre."""
    try:
        subprocess.run(['docker', 'start', container_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Contenedor {container_name} iniciado exitosamente.")
        print(f"Successfully started {container_name}")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip()
        logger.error(f"Fallo al iniciar el contenedor {container_name}: {error_message}")
        print(f"Failed to start {container_name}")

def main():
    check_docker()
    
    if not is_docker_running():
        logger.error("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")
        raise SystemExit("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")

    containers = ["tryton-postgres", "tryton"]
    for container in containers:
        start_container(container)
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
