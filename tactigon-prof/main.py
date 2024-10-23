import time
from customTskin import CustomTskin, Hand, OneFingerGesture

if __name__ == "__main__":
    # tskin = CustomTskin(....)
    with CustomTskin("C0:83:23:39:22:57", Hand.RIGHT) as tskin:
        while True:
            if not tskin.connected:
                print("Connecting...")
                time.sleep(0.1)
                continue

            touch = tskin.touch
            print(touch)

            if touch and (touch.one_finger == OneFingerGesture.SINGLE_TAP or True):
                print("ascolto.....")
                tskin.select_audio()
                time.sleep(10)
                tskin.select_sensors()
                print("ho finito")

            time.sleep(tskin.TICK)


