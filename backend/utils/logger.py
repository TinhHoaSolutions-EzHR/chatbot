import logging

class LoggerFactory:
    def __init__(self, name):
        # Initialize the logger instance
        self.logger = logging.getLogger(name)
        
        # Configure the logger
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger