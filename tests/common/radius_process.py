from subprocess import Popen, PIPE
from threading import Thread


def radius_thread_func(radius_control):
    process = radius_control["process"]
    print("radius_thread_func: before communicate")
    (out, err) = process.communicate()
    print(
        "radius_thread_func: after communicate out=" + str(out) + " err=" + str(err)
    )
    process.wait()
    print("radius_thread_func: after wait")


def start(radius, args):
    print("radius_start: begin")
    radius_process = Popen([radius] + args, stdout=PIPE, stderr=PIPE)
    radius_control = {"process": radius_process}
    radius_thread = Thread(
        target=radius_thread_func,
        args=[radius_control],
    )
    radius_thread.start()

    is_started = True

    return (is_started, radius_thread, radius_control)


def end(radius_thread, radius_control):
    print("radius_end: begin")
    if radius_control["process"].poll() is not None: # terminated
        print("radius_end: already terminated. nothing to do")
        radius_thread.join() 
        return

    print("radius_end: kill process: " + str(radius_control["process"]))
    radius_control["process"].kill()  # kill -9

    radius_thread.join()  # wait until thread is finished
    print("radius_end: end")
