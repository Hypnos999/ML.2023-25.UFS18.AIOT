from multiprocessing import Process, Event
from multiprocessing.connection import _ConnectionBase
import wave


class TSkinAudio(Process):
    audio_rx: _ConnectionBase

    def __init__(self, audio_rx):
        Process.__init__(self)

        self.audio_rx = audio_rx
        self.can_run = Event()

    def run(self):
        while self.can_run.is_set():
            if self.audio_rx.poll():
                # audio = self.audio_rx.recv_bytes()
                with wave.open("test.wav", "wb") as audio_file:
                    audio_file.setnchannels(1)
                    audio_file.setframerate(16000)
                    audio_file.setsampwidth(2)

                    while self.audio_rx.poll(1):
                        audio_bytes = self.audio_rx.recv_bytes()
                        audio_file.writeframes(audio_bytes)
