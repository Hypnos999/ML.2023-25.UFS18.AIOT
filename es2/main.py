import csv
import random
import time
import logging

import paho.mqtt.properties
import requests
import json
from config import Config
import multiprocessing
from paho.mqtt import publish
from paho.mqtt.enums import MQTTProtocolVersion
from paho import mqtt


def get_logger(
    path: str,
    *,
    name="log",
    format="%(asctime)s: %(message)s",
    console=True
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(format)
    file_handler = logging.FileHandler(path, mode="w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def read_csv(
        file_path: str
) -> list[list[str]]:
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=";")
        data = list(reader)

    return data


def emulate_readings(
    readings_queue: multiprocessing.Queue,
    csv_path: str,
    logger_path: str,
    sleep_time: float
):
    logger = get_logger(logger_path, name='emulate_readings', console=False)
    data = read_csv(csv_path)
    headers = data[0]
    data = data[1:]
    index = 1
    i = 0

    while True:
        logger.info(f'Analyzing item n.{index}')

        d = {k: v for k, v in zip(headers, data[i]) if k != ''}
        logger.info(f'data: {json.dumps(d, indent=2)}')

        readings_queue.put(d | {'_Index': index})
        logger.info('Sended data to main process...')

        index += 1
        i += 1

        if i == len(data) - 1:
            i = 0

        logger.info(f'Process will procede to sleep for {sleep_time}s')
        logger.info('')
        time.sleep(sleep_time)


if __name__ == "__main__":
    config = Config()
    logger = get_logger(config.loggger_path, name='main')
    emulate_readings_process = None

    try:
        readings_queue = multiprocessing.Queue()
        emulate_readings_process = multiprocessing.Process(target=emulate_readings,
                                                           args=[readings_queue, config.csv_path,
                                                                 config.subprocess_loggger_path,
                                                                 config.sleep_betwheen_runs])
        emulate_readings_process.start()
    except:
        logger.error('Couldn\'t start emulate_readings subprocess, aborting the programm...')
        while emulate_readings_process is not None and emulate_readings_process.is_alive():
            emulate_readings_process.terminate()
            emulate_readings_process.join(timeout=60)
        exit(1)

    # start main loop
    try:
        while True:
            if not readings_queue.empty():
                data = readings_queue.get()
                index = data['_Index']
                logger.info(f"Received data with index n.{index}: {json.dumps(data, indent=2)}")

                try:
                    logger.info('Calculating R_meas, Rcl and Rcp...')
                    r_meas = float(data["Value"].replace(',', '.'))
                    rcl = config.linear_transformation(r_meas)
                    rcp = config.polynomial_transformation(r_meas)

                    logger.info(f"R_meas: {r_meas}")
                    logger.info(f"Rcl: {rcl}")
                    logger.info(f"Rcp: {rcp}")

                    try:
                        device_token = data['Access token']
                        payload = {
                            "device": device_token,
                            "distance": rcp,
                            'from': 'flavio'
                        }
                        logger.info("Sendig payload %s", payload)

                        try:
                            # result = client.publish(f"{config.topic}/{device_token}", json.dumps(payload), qos=0, retain=False)
                            # result = client.publish(f"{config.topic}", json.dumps(payload))
                            publish.single(
                                f"{config.topic}/{device_token}",
                                json.dumps(payload),
                                qos=0,
                                hostname=config.brokerurl,
                                port=config.brokerport,
                                # client_id=config.client_id,  # inserendo client_id i dati non vengono visualizzati correttamente --> errore di hivemq.com
                                protocol=MQTTProtocolVersion.MQTTv5
                            )

                        except Exception as e:
                            logger.error("MQTT broker is not connected")
                            logger.exception(e)

                        logger.info('Finished readings')

                    except requests.exceptions.MissingSchema:
                        logger.error('ERROR: The url set in config.py is not valid')

                except Exception as e:
                    logger.info('')
                    logger.info('Exception raised while calculating R_meas, Rcl and Rcp:')
                    logger.exception(e)

                logger.info("")
                logger.info("")

    except Exception as e:
        logger.info('Process raised an error')
        logger.exception(e)
    finally:
        while emulate_readings_process.is_alive():
            emulate_readings_process.terminate()
            emulate_readings_process.join(timeout=60)
