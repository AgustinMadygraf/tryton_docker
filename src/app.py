#Tryton\src\app.py
import subprocess
from .logs.config_logger import configurar_logging
import time

# Configurar el logger
logger = configurar_logging()

def run_docker_command(docker_command, success_message, error_message):
    try:
        result = subprocess.run(docker_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(success_message)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        logger.error(f"{error_message}: {e.stderr.decode().strip()}")
        raise

def countdown(seconds, message):
    for i in range(seconds, 0, -1):
        print(f"{message} en {i} segundos...", end="\r")
        time.sleep(1)
    print(" " * 50, end="\r")  # Clear the line after countdown
    logger.info(f"{message} finalizado.")

def check_docker():
    while True:
        try:
            run_docker_command(['docker', '--version'], "Docker está instalado.", "Docker no está instalado o no está en el PATH.")
            break
        except Exception as e:
            countdown(10, "Reintentando verificación de Docker")

def is_docker_running():
    """Verifica si Docker Desktop está en ejecución."""
    while True:
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
            countdown(10, "Reintentando verificación del estado de Docker Desktop")

def check_if_container_exists(container_name):
    """Verifica si un contenedor Docker existe."""
    try:
        subprocess.run(['docker', 'inspect', container_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def create_and_start_container(container_name):
    """Crea e inicia los contenedores Docker necesarios para Tryton."""
    while True:
        if container_name == "tryton-postgres":
            try:
                subprocess.run(['docker', 'run', '--name', 'tryton-postgres', '-e', 'POSTGRES_PASSWORD=mysecretpassword', '-e', 'POSTGRES_DB=tryton', '-d', 'postgres'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                logger.info(f"Contenedor {container_name} creado e iniciado exitosamente.")
                logger.info(f"Successfully created and started {container_name}")
                break
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.decode().strip()
                logger.error(f"Fallo al crear e iniciar el contenedor {container_name}: {error_message}")
                logger.error(f"Failed to create and start {container_name}")
                countdown(10, "Reintentando creación y inicio del contenedor")
        elif container_name == "tryton":
            try:
                subprocess.run(['docker', 'run', '--name', 'tryton', '-p', '8000:8000', '--link', 'tryton-postgres:postgres', '-e', 'DB_PASSWORD=mysecretpassword', '-d', 'tryton/tryton'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                logger.info(f"Contenedor {container_name} creado e iniciado exitosamente.")
                logger.info(f"Successfully created and started {container_name}")
                break
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.decode().strip()
                logger.error(f"Fallo al crear e iniciar el contenedor {container_name}: {error_message}")
                logger.error(f"Failed to create and start {container_name}")
                countdown(10, "Reintentando creación y inicio del contenedor")

def setup_tryton_database():
    """Configura la base de datos para Tryton."""
    while True:
        try:
            subprocess.run(['docker', 'run', '--link', 'tryton-postgres:postgres', '-e', 'DB_PASSWORD=mysecretpassword', '-it', 'tryton/tryton', 'trytond-admin', '-d', 'tryton', '--all'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("Base de datos de Tryton configurada exitosamente.")
            logger.info("Successfully set up Tryton database")
            break
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode().strip()
            logger.error(f"Fallo al configurar la base de datos de Tryton: {error_message}")
            logger.error(f"Failed to set up Tryton database")
            countdown(10, "Reintentando configuración de la base de datos de Tryton")

def main():
    check_docker()
    
    if not is_docker_running():
        logger.error("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")
        raise SystemExit("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")

    containers = ["tryton-postgres", "tryton"]
    for container in containers:
        if check_if_container_exists(container):
            while True:
                try:
                    subprocess.run(['docker', 'start', container], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    logger.info(f"Contenedor {container} iniciado exitosamente.")
                    logger.info(f"Successfully started {container}")
                    break
                except subprocess.CalledProcessError as e:
                    error_message = e.stderr.decode().strip()
                    logger.error(f"Fallo al iniciar el contenedor {container}: {error_message}")
                    logger.error(f"Failed to start {container}")
                    countdown(10, "Reintentando inicio del contenedor")
        else:
            logger.error(f"El contenedor {container} no existe. Creando e iniciando el contenedor.")
            logger.warning(f"Container {container} does not exist. Creating and starting the container.")
            create_and_start_container(container)
            if container == "tryton-postgres":
                setup_tryton_database()
    
    countdown(10, "Finalizando")
