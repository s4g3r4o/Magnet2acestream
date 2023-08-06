# Programa de Generación de IDs de Acestream

Este programa está diseñado para generar IDs para Acestream utilizando una API local. La generación de IDs se realiza a partir de infohashes de los enlaces magnets proporcionados en un archivo de entrada, y los resultados se almacenan en un archivo de salida. También realiza un seguimiento de los infohashes procesados y sus respectivos IDs para evitar duplicados.

## Requisitos previos

Antes de ejecutar el programa, asegúrate de tener los siguientes requisitos previos instalados:

1. Python: El programa está escrito en Python y requiere tener Python instalado en tu sistema.

2. Paquetes Python: Asegúrate de tener los siguientes paquetes Python instalados:
   - `colorama`: Se utiliza para imprimir mensajes con colores en la consola.
   - `PyYAML`: Se utiliza para cargar la configuración desde un archivo YAML.

   Puedes instalar estos paquetes usando `pip`:

   ```bash
   pip install colorama PyYAML
   ```

## Configuración

Antes de ejecutar el programa, debes configurar los parámetros necesarios en un archivo YAML llamado `config.yaml`. Asegúrate de tener el archivo `config.yaml` en el mismo directorio que el script.

El contenido del archivo `config.yaml` debe ser el siguiente:

```yaml
input_file: ruta/al/archivo_de_entrada.txt
output_file: ruta/al/archivo_de_salida.txt
processed_file: ruta/al/archivo_de_procesados.txt
```

- `input_file`: Ruta al archivo que contiene los enlaces magnets para los cuales se generarán los IDs.
- `output_file`: Ruta al archivo donde se guardarán los IDs generados.
- `processed_file`: Ruta al archivo que almacena los infohashes procesados y sus IDs generados para evitar duplicados y evitar tantas llamadas a la API

## Ejecución del programa

Para ejecutar el programa, simplemente abre una terminal o línea de comandos, navega al directorio donde se encuentra el script y el archivo `config.yaml`, y luego ejecuta el siguiente comando:

```bash
python magnet2acestream.py
```

El programa comenzará a procesar los infohashes del archivo de entrada y generará los IDs correspondientes. Los resultados se guardarán en el archivo de salida especificado en la configuración.

## Detener la ejecución

Durante la ejecución del programa, si deseas detener el proceso manualmente, puedes presionar `Ctrl + C` en la terminal. El programa detectará la señal SIGINT y detendrá la ejecución de manera segura, mostrando un mensaje de confirmación.

## Resultados

Al finalizar el proceso, el programa imprimirá en la consola el número de Acestream para los cuales se generaron correctamente los IDs y el número de errores que ocurrieron durante el proceso. Además, informará la ubicación del archivo de salida donde se guardaron los resultados generados.

¡Listo! Ahora puedes utilizar este programa para generar IDs de Acestream a partir de magnets de manera sencilla y eficiente.
