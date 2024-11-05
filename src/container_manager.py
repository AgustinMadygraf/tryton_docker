"""
Path: src/container_manager.py
Este módulo se encarga de gestionar los contenedores Docker necesarios para Tryton.
"""

import subprocess
from src.logs.config_logger import LoggerConfigurator
from .utils.command_utils import countdown

logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

DOCKER_COMMANDS = {
    "tryton-postgres": [
        'docker', 'run', '--name', 'tryton-postgres', '-e', 'POSTGRES_PASSWORD=mysecretpassword',
        '-e', 'POSTGRES_DB=tryton', '-d', 'postgres'
    ],
    "tryton": [
        'docker', 'run', '--name', 'tryton', '-p', '8000:8000', '--link',
        'tryton-postgres:postgres', '-e', 'DB_PASSWORD=mysecretpassword', '-d', 'tryton/tryton'
    ]
}

class ContainerManager:
    """Clase que se encarga de gestionar los contenedores Docker necesarios para Tryton."""
    def __init__(self):
        self.logger = logger

    def run_docker_command(self, docker_command, success_message, error_message):
        """Ejecuta un comando Docker y maneja los errores."""
        try:
            result = subprocess.run(docker_command, check=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.info(success_message)
            return result.stdout.decode()
        except subprocess.CalledProcessError as e:
            self.logger.error("%s: %s", error_message, e.stderr.decode().strip())
            raise

    def check_if_container_exists(self, container_name):
        """Verifica si un contenedor Docker está en ejecución."""
        try:
            result = subprocess.run(['docker', 'ps', '--filter',
                f'name={container_name}', '--format', '{{.Names}}'], check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            running_containers = result.stdout.decode().splitlines()
            return container_name in running_containers
        except subprocess.CalledProcessError as e:
            self.logger.error("Error verificando contenedor %s: %s",
                              container_name, e.stderr.decode().strip())
            return False

    def check_if_container_stopped(self, container_name):
        """Verifica si un contenedor Docker existe pero está detenido."""
        try:
            result = subprocess.run(['docker', 'ps', '-a', '--filter',
                f'name={container_name}', '--filter', 'status=exited', '--format',
                '{{.Names}}'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stopped_containers = result.stdout.decode().splitlines()
            return container_name in stopped_containers
        except subprocess.CalledProcessError as e:
            self.logger.error("Error verificando contenedor detenido %s: %s",
                              container_name, e.stderr.decode().strip())
            return False

    def start_container(self, container_name):
        """Inicia un contenedor Docker existente."""
        try:
            subprocess.run(['docker', 'start', container_name], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.info("Contenedor %s iniciado exitosamente.", container_name)
        except subprocess.CalledProcessError as e:
            self.logger.error("Fallo al iniciar el contenedor %s: %s",
                              container_name, e.stderr.decode().strip())
            raise

    def create_and_start_container(self, container_name):
        """Crea e inicia los contenedores Docker necesarios para Tryton."""
        while True:
            try:
                subprocess.run(DOCKER_COMMANDS[container_name], check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.logger.info("Contenedor %s creado e iniciado exitosamente.", container_name)
                break
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.decode().strip()
                self.logger.error("Fallo al crear e iniciar el contenedor %s: %s",
                                  container_name, error_message)
                countdown(10, "Reintentando creación y inicio del contenedor")

    def setup_tryton_database(self):
        """Configura la base de datos para Tryton."""
        while True:
            try:
                subprocess.run(['docker', 'run', '--link', 'tryton-postgres:postgres',
                    '-e', 'DB_PASSWORD=mysecretpassword', '-it', 'tryton/tryton', 'trytond-admin',
                    '-d', 'tryton', '--all'], check=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.logger.info("Base de datos de Tryton configurada exitosamente.")
                break
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.decode().strip()
                self.logger.error("Fallo al configurar la base de datos de Tryton: %s",
                                  error_message)
                countdown(10, "Reintentando configuración de la base de datos de Tryton")
