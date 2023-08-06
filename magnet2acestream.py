import os
import subprocess
import yaml
import re
import json
import signal
from colorama import Fore, Style
from datetime import datetime

def load_config(filename):
    if not os.path.exists(filename):
        print(f"{Fore.RED}El archivo de configuración '{filename}' no existe.{Style.RESET_ALL}")
        return None

    with open(filename, "r") as file:
        config = yaml.safe_load(file)

    if "output_file" not in config:
        print(f"{Fore.RED}El archivo de salida no está configurado en 'output_file' dentro de {filename}.{Style.RESET_ALL}")
        return None

    config["input_file"] = os.path.abspath(config["input_file"])
    config["output_file"] = os.path.abspath(config["output_file"])
    config["processed_file"] = os.path.abspath(config["processed_file"])

    return config

# Variable global para controlar si se debe detener la ejecución
should_stop = False

def signal_handler(signum, frame):
    global should_stop
    should_stop = True
    print(f"\n{Fore.RED}Señal recibida. Deteniendo la ejecución...{Style.RESET_ALL}")

def main():
    config = load_config("config.yaml")

    if not config:
        return

    if not os.path.exists(config["input_file"]):
        print(f"{Fore.RED}El archivo de entrada '{config['input_file']}' no existe.{Style.RESET_ALL}")
        return

    processed_ids = {}
    if os.path.exists(config["processed_file"]):
        with open(config["processed_file"], "r") as processed_file:
            for line in processed_file:
                infohash, content_id = line.strip().split(',')
                processed_ids[infohash] = content_id

    correct_count = 0
    error_count = 0

    # Asociar la función signal_handler al manejo de la señal SIGINT (Ctrl + C)
    signal.signal(signal.SIGINT, signal_handler)

    with open(config["output_file"], "w+") as ids_file:
        with open(config["input_file"], "r") as file:
            for line_num, line in enumerate(file, start=1):
                if should_stop:
                    print(f"\n{Fore.RED}Deteniendo el programa...{Style.RESET_ALL}")
                    break

                infohash = re.search(r":(\w+)$", line)
                if infohash:
                    infohash = infohash.group(1)
                    if infohash in processed_ids:
                        content_id = processed_ids[infohash]
                        if content_id == "0":
                            print(f"{Fore.YELLOW}[Línea {line_num}] El infohash {infohash} no ha podido conseguir un id previamente. Se omite la comprobación.{Style.RESET_ALL}")
                            ids_file.write("0\n")
                            ids_file.flush()
                            error_count += 1
                        else:
                            print(f"{Fore.BLUE}[Línea {line_num}][{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] El infohash {infohash} ya ha sido comprobado previamente. Su id es {content_id}{Style.RESET_ALL}")
                            ids_file.write(content_id + "\n")
                            ids_file.flush()
                            correct_count += 1
                    else:
                        command = f'curl "http://127.0.0.1:6878/server/api?api_version=3&method=get_content_id&infohash={infohash}"'
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        try:
                            response_json = json.loads(result.stdout)
                            content_id = response_json["result"]["content_id"]
                            print(f"{Fore.GREEN}[Línea {line_num}][{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] El infohash {infohash} se ha generado correctamente. Su id es {content_id}{Style.RESET_ALL}")
                            ids_file.write(content_id + "\n")
                            ids_file.flush()
                            correct_count += 1
                            processed_ids[infohash] = content_id
                            with open(config["processed_file"], "a") as processed_file:
                                processed_file.write(f"{infohash},{content_id}\n")
                        except (json.JSONDecodeError, KeyError):
                            print(f"{Fore.RED}[Línea {line_num}][{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] Este infohash {infohash} No se ha podido conseguir un id. {Style.RESET_ALL}")
                            ids_file.write("0\n")
                            ids_file.flush()
                            error_count += 1
                            processed_ids[infohash] = "0"
                            with open(config["processed_file"], "a") as processed_file:
                                processed_file.write(f"{infohash},0\n")

    print(f"\nProceso completado. Se generaron correctamente {correct_count} torrents y hubo {error_count} errores.")
    print("Los resultados se han guardado en", config["output_file"])

if __name__ == "__main__":
    main()
