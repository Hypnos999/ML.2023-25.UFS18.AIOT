from tactigon_gear import Ble, Hand
from .middleware import TSkinFlow, TSkinAudio
from multiprocessing import Pipe

class CustomTSkin(Ble):
    tskin_flow: TSkinFlow
    tskin_audio: TSkinAudio

    def __init__(self, addres: str, hand: Hand):
        Ble.__init__(self, addres, hand)
        # super().__init__(addres, hand)

        sensor_rx, self._sensor_tx = Pipe(duplex=False)
        audio_rx, self._audio_tx = Pipe(duplex=False)

        self.tskin_flow = TSkinFlow(sensor_rx)
        self.tskin_flow.can_run.set()

        self.tskin_audio = TSkinAudio(audio_rx)
        self.tskin_audio.can_run.set()

    def start(self):
        self.tskin_flow.start()
        self.tskin_audio.start()
        Ble.start(self)

    def join(self, timeout=None):
        Ble.join(self, timeout=timeout)

        self.tskin_flow.can_run.clear()
        self.tskin_flow.terminate()

        self.tskin_audio.can_run.clear()
        self.tskin_audio.terminate()
