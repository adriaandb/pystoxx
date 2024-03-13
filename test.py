from threading import Thread
import time

import test2
import test_class



Testclass = test_class.Test('naam1')
print(Testclass.name)

def main():
    i = 0
    while True:
        print('main thread '+ str(i) +': '+ Testclass.name)
        i +=1
        time.sleep(5)

def start_controller(testclass):
    test2.run_gui(Testclass)


thread_main = Thread(name='main' , target=main)
thread_controller = Thread(name='controller', target=start_controller, args=(Testclass,))


if __name__ == "__main__":

    thread_main.start()
    thread_controller.start()

