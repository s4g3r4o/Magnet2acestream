import os
import subprocess
import yaml
import re
import json
from colorama import Fore, Style


def load_config(filename):
    if not os.path.exists(filename):
        print(f"{Fore.RED}El archivo de configuración '{filename}' no existe.{Style.RESET_ALL}")
        return None

    with open(filename, "r") as file:
        config = yaml.safe_load(file)

    # Verificar si se proporcionó el archivo de salida en la configuración
    if "output_file" not in config:
        print(f"{Fore.RED}El archivo de salida no está configurado en 'output_file' dentro de {filename}.{Style.RESET_ALL}")
        return None

    # Obtener ruta absoluta para el archivo de salida
    output_file = os.path.abspath(config["output_file"])

    config["output_file"] = output_file

    return config


def main():
    # Cargar la configuración desde el archivo YAML
    config = load_config("config.yaml")

    if not config:
        return

    # Verificar si los archivos de entrada y salida existen
    if not os.path.exists(config["input_file"]):
        print(f"{Fore.RED}El archivo de entrada '{config['input_file']}' no existe.{Style.RESET_ALL}")
        return

    # Verificar si el archivo de salida ya existe y, en caso afirmativo, eliminarlo
    if os.path.exists(config["output_file"]):
        os.remove(config["output_file"])

    # Variables para contar torrents generados correctamente y en fallo
    correct_count = 0
    error_count = 0

    # Abrir el archivo "ids.txt" en modo escritura
    with open(config["output_file"], "w") as ids_file:
        # Leer el archivo "enlaces_magnet.txt" línea por línea
        with open(config["input_file"], "r") as file:
            for line_num, line in enumerate(file, start=1):
                infohash = re.search(r":(\w+)$", line)
                if infohash:
                    infohash = infohash.group(1)
                    command = f'curl "http://127.0.0.1:6878/server/api?api_version=3&method=get_content_id&infohash={infohash}"'
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    try:
                        response_json = json.loads(result.stdout)
                        content_id = response_json["result"]["content_id"]
                        print(f"{Fore.GREEN}[Línea {line_num}] El infohash {infohash} se ha generado correctamente. Su id es {content_id}{Style.RESET_ALL}")
                        ids_file.write(content_id + "\n")
                        correct_count += 1
                    except (json.JSONDecodeError, KeyError):
                        print(f"{Fore.RED}[Línea {line_num}] Este infohash {infohash} No se ha podido conseguir un id. {Style.RESET_ALL}")
                        ids_file.write("0\n")
                        error_count += 1

    print(f"\nProceso completado. Se generaron correctamente {correct_count} torrents y hubo {error_count} errores.")
    print("Los resultados se han guardado en", config["output_file"])


if __name__ == "__main__":
    main()
