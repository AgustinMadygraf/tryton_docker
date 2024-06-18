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

def container_exists(container_name):
    """Verifica si un contenedor Docker existe."""
    try:
        subprocess.run(['docker', 'inspect', container_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def create_and_start_container(container_name):
    """Crea e inicia los contenedores Docker necesarios para Tryton."""
    if container_name == "tryton-postgres":
        try:
            subprocess.run(['docker', 'run', '--name', 'tryton-postgres', '-e', 'POSTGRES_PASSWORD=mysecretpassword', '-e', 'POSTGRES_DB=tryton', '-d', 'postgres'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"Contenedor {container_name} creado e iniciado exitosamente.")
            print(f"Successfully created and started {container_name}")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode().strip()
            logger.error(f"Fallo al crear e iniciar el contenedor {container_name}: {error_message}")
            print(f"Failed to create and start {container_name}")
    elif container_name == "tryton":
        try:
            subprocess.run(['docker', 'run', '--name', 'tryton', '-p', '8000:8000', '--link', 'tryton-postgres:postgres', '-e', 'DB_PASSWORD=mysecretpassword', '-d', 'tryton/tryton'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"Contenedor {container_name} creado e iniciado exitosamente.")
            print(f"Successfully created and started {container_name}")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode().strip()
            logger.error(f"Fallo al crear e iniciar el contenedor {container_name}: {error_message}")
            print(f"Failed to create and start {container_name}")

def setup_tryton_database():
    """Configura la base de datos para Tryton."""
    try:
        subprocess.run(['docker', 'run', '--link', 'tryton-postgres:postgres', '-e', 'DB_PASSWORD=mysecretpassword', '-it', 'tryton/tryton', 'trytond-admin', '-d', 'tryton', '--all'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Base de datos de Tryton configurada exitosamente.")
        print("Successfully set up Tryton database")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip()
        logger.error(f"Fallo al configurar la base de datos de Tryton: {error_message}")
        print(f"Failed to set up Tryton database")

def main():
    check_docker()
    
    if not is_docker_running():
        logger.error("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")
        raise SystemExit("Docker Desktop no está en ejecución. Por favor, inícialo y vuelve a intentarlo.")

    containers = ["tryton-postgres", "tryton"]
    for container in containers:
        if container_exists(container):
            try:
                subprocess.run(['docker', 'start', container], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                logger.info(f"Contenedor {container} iniciado exitosamente.")
                print(f"Successfully started {container}")
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.decode().strip()
                logger.error(f"Fallo al iniciar el contenedor {container}: {error_message}")
                print(f"Failed to start {container}")
        else:
            logger.error(f"El contenedor {container} no existe. Creando e iniciando el contenedor.")
            print(f"Container {container} does not exist. Creating and starting the container.")
            create_and_start_container(container)
            if container == "tryton-postgres":
                setup_tryton_database()
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
