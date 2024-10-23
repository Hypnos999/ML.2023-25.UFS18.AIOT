import time

from custom_tskin import CustomTSkin, Hand
import logging

if __name__ == "__main__":
    with CustomTSkin('C0:83:23:39:22:57', Hand.RIGHT) as tskin:
        tskin.select_audio()

        while True:
            if not tskin.connected:
                print('Connecting to tskin...')
                time.sleep(0.25)
                continue

            acc = tskin.acceleration

            print(tskin.battery)
            print(f'Acceleration: {acc}')
            time.sleep(tskin.TICK)
