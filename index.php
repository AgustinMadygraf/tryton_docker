<?php
"""
index.php
Ejecutar un script de Python con Pipenv desde PHP
"""
// Definir la ruta completa de pipenv
$pipenv_path = 'C:\Users\\MAQ-BOLSAS\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\Scripts\\pipenv.exe'; // Ajusta la ruta de pipenv
$script_path = 'C:\\AppServ\\www\\Tryton\\run.py'; // Ajusta la ruta de run.py

// Verificar si las rutas existen
if (!file_exists($pipenv_path)) {
    die("Error: pipenv.exe no se encuentra en la ruta especificada.");
}
if (!file_exists($script_path)) {
    die("Error: run.py no se encuentra en la ruta especificada.");
}

// Ejecutar el comando
$command = escapeshellcmd($pipenv_path . ' run python ' . $script_path);
$output = shell_exec($command . ' 2>&1');

// Mostrar el resultado
if ($output === null) {
    echo "Error ejecutando el script.";
} else {
    echo "<pre>$output</pre>";
}
?>