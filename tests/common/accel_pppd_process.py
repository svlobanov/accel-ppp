from subprocess import Popen, PIPE
from common import process
from threading import Thread
import time


def accel_pppd_thread_func(accel_pppd, args, accel_pppd_control):
    process = Popen(["sudo", accel_pppd] + args, stdout=PIPE, stderr=PIPE)
    print(process)
    accel_pppd_control["process"] = process
    print("accel_pppd_thread_func: before communicate")
    process.communicate()
    print("accel_pppd_thread_func: after communicate")
    process.wait()
    print("accel_pppd_thread_func: after wait")


def start(accel_pppd, args, accel_cmd, max_wait_time):
    accel_pppd_control = {}
    accel_pppd_thread = Thread(
        target=accel_pppd_thread_func,
        args=(accel_pppd, args, accel_pppd_control),
    )
    accel_pppd_thread.start()

    # wait until accel-pppd replies to 'show version'
    # accel-pppd needs some time to be accessible
    sleep_time = 0.0
    is_started = False
    while sleep_time < max_wait_time:
    #while 1 < 2:
        (exit, out, err) = process.run([accel_cmd, "show version"])
        if exit != 0: #0
            time.sleep(0.01) # 0.01
            sleep_time += 0.01
        else:
            is_started = True
            break

    return (is_started, accel_pppd_thread, accel_pppd_control)


def end(accel_pppd_thread, accel_pppd_control):
    print("accel_pppd_end: begin")
    if "process" in accel_pppd_control:
        accel_pppd_control["process"].kill()
    accel_pppd_thread.join()
    print("accel_pppd_end: finished")
