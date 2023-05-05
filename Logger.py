import logging
import datetime
import os

class Logger:
    def __init__(self, log_path, log_level=logging.DEBUG):
        self.log_path = log_path
        self.log_level = log_level
    
    def create_logger(self):
        date_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        logger = logging.getLogger()
        logger.setLevel(level=self.log_level)
        
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        handler = logging.FileHandler(os.path.join(self.log_path, 'log_' + date_time))
        handler.setLevel(self.log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger