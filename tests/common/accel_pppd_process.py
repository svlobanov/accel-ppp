from subprocess import Popen, PIPE
from common import process
from threading import Thread
import time


def accel_pppd_thread_func(accel_pppd_control):
    # process = Popen([accel_pppd] + args, stdout=PIPE, stderr=PIPE)
    # print(process)
    process = accel_pppd_control["process"]
    print("accel_pppd_thread_func: before communicate")
    process.communicate()
    print("accel_pppd_thread_func: after communicate")
    process.wait()
    print("accel_pppd_thread_func: after wait")


def start(accel_pppd, args, accel_cmd, max_wait_time):
    accel_pppd_process = Popen([accel_pppd] + args, stdout=PIPE, stderr=PIPE)
    accel_pppd_control = {"process": accel_pppd_process}
    accel_pppd_thread = Thread(
        target=accel_pppd_thread_func,
        args=[accel_pppd_control],
    )
    accel_pppd_thread.start()

    # wait until accel-pppd replies to 'show version'
    # accel-pppd needs some time to be accessible
    sleep_time = 0.0
    is_started = False
    while sleep_time < max_wait_time:
        (exit, out, err) = process.run([accel_cmd, "show version"])
        if exit != 0:  # does not reply
            time.sleep(0.01)
            sleep_time += 0.01
        else:  # replied
            is_started = True
            break

    return (is_started, accel_pppd_thread, accel_pppd_control)


def end(accel_pppd_thread, accel_pppd_control, accel_cmd, max_wait_time):
    print("accel_pppd_end: begin")
    process.run(
        [accel_cmd, "shutdown hard"]
    )  # send shutdown hard command (in coverage mode it helps saving coverage data)
    print("accel_pppd_end: after shutdown hard")
    # if "process" not in accel_pppd_control:
    #    print("accel_pppd_end: proccess not in accel_pppd_control. nothing to do")
    #    accel_pppd_thread.join()  # wait until thread is finished
    #    return

    sleep_time = 0.0
    is_finished = False
    while sleep_time < max_wait_time:
        if accel_pppd_control["process"].poll() is None:  # not terminated yet
            time.sleep(0.01)
            sleep_time += 0.01
            # print("accel_pppd_end: sleep 0.01")
        else:
            is_finished = True
            print(
                "accel_pppd_end: finished via shutdown hard in (sec): "
                + str(sleep_time)
            )
            break

    if not is_finished:
        print("accel_pppd_end: kill process: " + str(accel_pppd_control["process"]))
        accel_pppd_control["process"].kill()  # kill -9 if 'shutdown hard' didn't help

    accel_pppd_thread.join()  # wait until thread is finished
    print("accel_pppd_end: end")
