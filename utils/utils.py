from multiprocessing import Process, Event, Queue
import multiprocessing
from .sim_client import PathFollowing2
from playsound import playsound
import time

# stop_speech_event = Event()

def speech_moving(dir_wav="/home/toonies/Learn/Tensorbot/data/speechs/vi/hoanthanh.wav", mode = "finish"):
    if mode == "finish":
        return playsound("/home/toonies/Learn/Tensorbot/data/speechs/vi/hoanthanh.wav")
    elif mode == "avoid":
        return playsound("/home/toonies/Learn/Tensorbot/data/speechs/vi/tranhduong.wav")
    elif mode == "start":
        return playsound("/home/toonies/Learn/Tensorbot/data/speechs/vi/batdau.wav")

def dummy_func(val_return1):
    global stop_speech_event
    print("Function 1: starting")
    for i in range(7):
        time.sleep(1)
        print(i)
        if i == 5:
            stop_speech_event.set()

    val_return1.put(i)
    return 1

def Run_Parallel_Func(func1, func2, val_input1= [(0,0)]):
    val_return1 = Queue()
    func1_temp = Process(target=func1, args=(val_return1,))
    func1_temp.start()

    func2_temp = Process(target=func2)
    func2_temp.start()

    return_value = val_return1.get()
    func2_temp.terminate()

    return return_value

if __name__ == "__main__":
    # return_value = Run_Parallel_Func(dummy_func, speech_moving, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)])
    # print("Return value:", return_value)
    speech_moving()
