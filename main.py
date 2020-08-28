from raspFunctions import *
from time import sleep

def start():
    raspberry = RaspFunctions()
    raspberry.setGPIO()
    if raspberry.readPIR():
        raspberry.readCamera()
    print(f"Record--> {RaspFunctions.record}")

if __name__ == '__main__':
    num = 0
    try:
        while True:
            start()
            num += 1
            print(f'Number of executions= {num}')
            time.sleep(5)
    except KeyboardInterrupt:
        print('Exited')
        exit()