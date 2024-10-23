from multiprocessing import Process, Event
from multiprocessing.connection import _ConnectionBase

class TSkinFlow(Process):
    def __init__(self, sensor_rx):
        Process.__init__(self)

        self.sensor_rx = sensor_rx
        self.can_run = Event()

    def run(self):
        while self.can_run.is_set():
            if self.sensor_rx.poll():
                acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = self.sensor_rx.recv()
                print(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z)