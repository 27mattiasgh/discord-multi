import logging
import threading
from colorama import Fore






def thread_function():
        print('xxx')



datetime_format = "%(asctime)s: %(message)s"

logging.basicConfig(format=datetime_format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("[MAIN]    forming thread")

x = threading.Thread(target=thread_function, args=())

x.start()


