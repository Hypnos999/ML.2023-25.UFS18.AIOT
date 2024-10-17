class Config:

    def __init__(
        self,
        logger_path='main.log',
        subprocess_loggger_path='emulate_readings.log',
        csv_path='Copia di Estensimetro Esempio Letture.csv',
        sleep_betwheen_runs=10,

        lin_a_factor=2.6647E-02,
        lin_b_factor=-7.2683E+01,

        pol_a_factor=7.0405E-12,
        pol_b_factor=-1.0504E-07,
        pol_c_factor=2.7117E-02,
        pol_d_factor=-7.3308E+01,
    ):
        self.loggger_path = logger_path
        self.subprocess_loggger_path = subprocess_loggger_path
        self.csv_path = csv_path
        self.sleep_betwheen_runs = sleep_betwheen_runs

        self.lin_a_factor = lin_a_factor
        self.lin_b_factor = lin_b_factor
        self.linear_transformation = lambda r_meas: self.lin_a_factor * r_meas + self.lin_b_factor

        self.pol_a_factor = pol_a_factor
        self.pol_b_factor = pol_b_factor
        self.pol_c_factor = pol_c_factor
        self.pol_d_factor = pol_d_factor
        self.polynomial_transformation = lambda \
            r_meas: self.pol_a_factor * r_meas ** 3 + self.pol_b_factor * r_meas ** 2 + self.pol_c_factor * r_meas + self.pol_d_factor

        # Copy configurations from config file
        self.delay = 5
        self.brokerurl = "broker.hivemq.com"
        self.brokerport = 1883
        # self.brokerport = 8884
        self.topic = 'next/sensordata'
        self.FIRST_RECONNECT_DELAY = 1
        self.RECONNECT_RATE = 2
        self.MAX_RECONNECT_COUNT = 12
        self.MAX_RECONNECT_DELAY = 60
        self.baseurl = "https://zion.nextind.eu",
        self.client_id = 'clientId-l4rysSlboO'

        # if url is None:
        #     self.url = lambda acces_token: f'https://zion.nextind.eu:443/api/v1/{acces_token}/telemetry'
        # else:
        #     self.url = url
        #
        # if headers is None:
        #     self.headers = {
        #         'Content-Type': 'application/json',
        #         'Accept': 'application/json'
        #     }
        # else:
        #     self.headers = headers
