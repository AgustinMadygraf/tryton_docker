# ToDo List for `tryton_docker` Project Setup

- [x] **Paso 1:** Instalar Docker Desktop en Windows 11
  - **Descripción:** Asegúrate de tener Docker Desktop instalado y funcionando en tu sistema Windows 11.
  - **Instrucciones:**
    - Descarga Docker Desktop desde [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
    - Sigue las instrucciones de instalación en la página oficial.
    - Verifica la instalación ejecutando `docker --version` en PowerShell o CMD.
  - **Resultado Esperado:** Docker debería estar en funcionamiento y listo para usar.

- [ ] **Paso 2:** Crear el archivo `docker-compose.yml`
  - **Descripción:** Configura el archivo `docker-compose.yml` para definir los servicios de Tryton, PostgreSQL, Flask, Vue.js, y Nginx.
  - **Instrucciones:**
    - En la carpeta raíz del proyecto (`tryton_docker`), crea un archivo llamado `docker-compose.yml`.
    - Copia y pega la siguiente configuración en el archivo:
      ```yaml
      version: '3.8'

      services:
        tryton:
          image: tryton/tryton:latest
          container_name: tryton
          ports:
            - "8000:8000"
          environment:
            - TRYTON_DATABASE_HOST=db
            - TRYTON_DATABASE_USER=tryton
            - TRYTON_DATABASE_PASSWORD=tryton
            - TRYTON_DATABASE_NAME=tryton
          depends_on:
            - db

        db:
          image: postgres:13
          container_name: tryton_db
          environment:
            POSTGRES_USER: tryton
            POSTGRES_PASSWORD: tryton
            POSTGRES_DB: tryton
          volumes:
            - tryton_db_data:/var/lib/postgresql/data

        nginx:
          image: nginx:latest
          container_name: tryton_nginx
          ports:
            - "8000:8000"
          volumes:
            - ./nginx.conf:/etc/nginx/nginx.conf:ro
          depends_on:
            - tryton
            - flask
            - vue

        flask:
          build: ./path/to/your/flask/app  # Cambia esto a la ruta de tu app Flask
          container_name: madybot
          environment:
            - FLASK_ENV=development
          ports:
            - "5000:5000"

        vue:
          build: ./path/to/your/vue/app  # Cambia esto a la ruta de tu app Vue.js
          container_name: chatbot
          ports:
            - "8080:8080"

      volumes:
        tryton_db_data:
      ```
  - **Resultado Esperado:** Archivo `docker-compose.yml` creado con la configuración adecuada para cada servicio.

- [ ] **Paso 3:** Crear el archivo de configuración de Nginx (`nginx.conf`)
  - **Descripción:** Configura Nginx como proxy inverso para redirigir el tráfico a los servicios adecuados.
  - **Instrucciones:**
    - En la raíz del proyecto, crea un archivo llamado `nginx.conf`.
    - Agrega el siguiente contenido:
      ```nginx
      events {}

      http {
          server {
              listen 8000;

              # Ruta para Vue.js (Chatbot)
              location /chatbot/ {
                  proxy_pass http://chatbot:8080;
                  proxy_set_header Host $host;
                  proxy_set_header X-Real-IP $remote_addr;
                  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                  proxy_set_header X-Forwarded-Proto $scheme;
              }

              # Ruta para Flask (MadyBotPy)
              location /api/flask/ {
                  proxy_pass http://madybot:5000;
                  proxy_set_header Host $host;
                  proxy_set_header X-Real-IP $remote_addr;
                  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                  proxy_set_header X-Forwarded-Proto $scheme;
              }

              # Ruta para Tryton (ERP)
              location / {
                  proxy_pass http://tryton:8000;
                  proxy_set_header Host $host;
                  proxy_set_header X-Real-IP $remote_addr;
                  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                  proxy_set_header X-Forwarded-Proto $scheme;
              }
          }
      }
      ```
  - **Resultado Esperado:** Archivo `nginx.conf` configurado para redirigir el tráfico al contenedor adecuado.

- [ ] **Paso 4:** Construir e iniciar los contenedores de Docker
  - **Descripción:** Ejecuta Docker Compose para construir e iniciar todos los servicios.
  - **Instrucciones:**
    - En la terminal, navega a la carpeta raíz de `tryton_docker`.
    - Ejecuta el siguiente comando:
      ```bash
      docker-compose up -d
      ```
  - **Resultado Esperado:** Todos los contenedores definidos en `docker-compose.yml` se inician correctamente en segundo plano.

- [ ] **Paso 5:** Verificar el estado de los contenedores
  - **Descripción:** Asegúrate de que todos los contenedores están en ejecución.
  - **Instrucciones:**
    - Ejecuta `docker ps` para ver los contenedores en ejecución.
    - Verifica que los contenedores `tryton`, `tryton_db`, `tryton_nginx`, `madybot` y `chatbot` estén en ejecución.
  - **Resultado Esperado:** Todos los contenedores necesarios están en ejecución.

- [ ] **Paso 6:** Acceder a la aplicación Tryton en `localhost:8000`
  - **Descripción:** Verifica que Tryton está accesible en `http://localhost:8000`.
  - **Instrucciones:**
    - Abre un navegador y navega a `http://localhost:8000`.
    - Inicia sesión en Tryton para confirmar que está en funcionamiento.
  - **Resultado Esperado:** La aplicación Tryton está funcionando en el navegador.

- [ ] **Paso 7:** Verificar el acceso al Chatbot Vue.js en `localhost:8000/chatbot`
  - **Descripción:** Verifica que Vue.js (Chatbot) está accesible a través de Nginx.
  - **Instrucciones:**
    - Abre un navegador y navega a `http://localhost:8000/chatbot`.
    - Confirma que el frontend de Vue.js se carga correctamente.
  - **Resultado Esperado:** La interfaz de Vue.js para el Chatbot está disponible y funcional.

- [ ] **Paso 8:** Verificar el acceso a Flask (MadyBotPy) en `localhost:8000/api/flask`
  - **Descripción:** Verifica que la API de Flask está accesible a través de Nginx.
  - **Instrucciones:**
    - Realiza una solicitud a `http://localhost:8000/api/flask` para confirmar que la API de Flask responde.
    - Puedes utilizar herramientas como `curl` o Postman para probar la API.
  - **Resultado Esperado:** La API de Flask responde correctamente a las solicitudes.

- [ ] **Paso 9:** Configurar Ngrok para acceso externo (opcional)
  - **Descripción:** Exponer el puerto `8000` de Nginx a internet utilizando ngrok.
  - **Instrucciones:**
    - Instala Ngrok si no lo tienes ya instalado.
    - En la terminal, ejecuta:
      ```bash
      ngrok http 8000
      ```
    - Copia la URL pública proporcionada por Ngrok.
  - **Resultado Esperado:** La aplicación completa es accesible a través de una URL pública de Ngrok.

- [ ] **Paso 10:** Monitorear logs y verificar errores
  - **Descripción:** Revisa los logs de la aplicación para asegurarte de que no haya errores en los servicios.
  - **Instrucciones:**
    - Consulta los logs en `src/logs/sistema.log` para errores o advertencias.
    - Usa `docker logs <nombre_contenedor>` para ver los logs de cada contenedor.
  - **Resultado Esperado:** Todos los servicios funcionan sin errores y los logs indican un funcionamiento correcto.
