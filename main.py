import csv
import time
import logging


def get_logger(
    name: str = "log",
    format: str = "%(asctime)s: %(message)s",
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(f"{name}.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def read_csv(
    file_path="Copia di Estensimetro Esempio Letture.csv"
) -> list[list[str]]:
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        data = list(reader)

    return data


def get_rcl(
    r_meas: float,
    a: float = 0.0,
    b: float = 0.0
) -> float:
    rcl = a * r_meas + b

    return rcl


def get_rcp(
    r_meas: float,
    a: float = 0.0,
    b: float = 0.0,
    c: float = 0.0,
    d: float = 0.0
) -> float:
    rcp = a * r_meas ** 3 + b * r_meas ** 2 + c * r_meas + d

    return rcp


def get_criteria() -> bool:
    """Return True if |mpe_plus_u| < |mpe_pol| else False"""
    mpe_plus_u = 0.0867
    mpe_pol = 0.3

    if abs(mpe_plus_u) < abs(mpe_pol):
        return True
    else:
        return False


if __name__ == "__main__":
    logger = get_logger()
    timer = time.time() - 30
    index = 1
    while True:

        # wait 30 sec betwheen one run and another one
        if time.time() - timer < 30.0:
            continue
        else:
            logger.info(f"Started cycle n.{index}")
            index += 1

        data = read_csv()
        logger.info("Read csv")

        # exluding the headers row with [1:]
        for i, row in enumerate(data[1:]):
            logger.info("")
            logger.info(f"Analyzing row n.{i+1}")

            value = float(row[data[0].index("Value")])
            rcl = get_rcl(value)
            rcp = get_rcp(value)

            logger.info(f"Value: {value}, Rcl: {rcl}, Rcp: {rcp}")

            criteria = get_criteria()
            logger.info(f"Criteria: {criteria}")

        logger.info("Finished cycle")
        logger.info("")
        logger.info("")
        timer = time.time()
