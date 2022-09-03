from common import process


def t1est_accel_pppd_version(accel_pppd):
    (exit, out, err) = process.run([accel_pppd, "--version"])

    # test that accel-pppd --version exits with code 0, prints
    # nothing to stdout and prints to stdout
    assert exit == 0 and err == "" and "accel-ppp " in out and len(out.split(" ")) == 2
