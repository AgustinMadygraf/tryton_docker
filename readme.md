# Tryton Installer and Starter

## Descripción del Proyecto

Este proyecto tiene como propósito ser un instalador y/o iniciador de Tryton. Facilita la instalación y el inicio del sistema Tryton en una PC que se utilizará como servidor. 

## Problema que Resuelve

Instalar y configurar Tryton puede ser una tarea compleja para los usuarios que desean utilizar su PC como servidor. Este proyecto automatiza el proceso de instalación y configuración, asegurando que Tryton y sus contenedores Docker se configuren correctamente.

## Usuarios Objetivo

Este proyecto está dirigido a usuarios que desean utilizar su PC como servidor para Tryton. Está diseñado para simplificar el proceso de instalación y configuración, permitiendo a los usuarios enfocarse en el uso de Tryton en lugar de en su instalación.

## Requisitos del Proyecto

Todas las dependencias necesarias están listadas en el archivo `Pipfile`. Asegúrate de tener `pipenv` instalado para gestionar las dependencias del proyecto.

## Estructura del Proyecto

```bash
Tryton/
    readme.md
    run.py
    src/
        app.py
        docker_manager.py
        container_manager.py
        docker_operations.py
        __init__.py
        logs/
            config_logger.py
            logging.json
            __pycache__/
        utils/
            command_utils.py
            __pycache__/
    tests/
        test_app.py
        test_docker_operations.py
        test_container_manager.py
        integration/
            test_integration.py
    workflows/
```

## Instrucciones de Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/AgustinMadygraf/Tryton.git
    ```

2. Instala las dependencias usando `pipenv`:
    ```bash
    pipenv install
    ```

3. Activa el entorno virtual:
    ```bash
    pipenv shell
    ```

## Uso del Proyecto

1. Ejecuta el script principal para iniciar la instalación y configuración de Tryton:
    ```bash
    python src/main.py
    ```

2. Sigue las instrucciones en pantalla para completar la instalación y el inicio de Tryton.

## Ejemplo de Uso

A continuación se muestra un ejemplo de cómo utilizar este proyecto:

```bash
$ git clone https://github.com/AgustinMadygraf/Tryton.git
$ pipenv install
$ pipenv shell
$ python src/main.py
```

## Ejecución de Pruebas

Para ejecutar las pruebas unitarias y de integración, sigue estos pasos:

1. Asegúrate de estar en el entorno virtual:
    ```bash
    pipenv shell
    ```

2. Ejecuta las pruebas unitarias:
    ```bash
    pytest tests
    ```

3. Ejecuta las pruebas de integración:
    ```bash
    pytest tests/integration
    ```

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas contribuir, por favor sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Envía los cambios a tu fork (`git push origin feature/nueva-funcionalidad`).
5. Crea un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.