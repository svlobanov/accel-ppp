import pytest
from common import accel_pppd_process, config, veth, pppd_process


def pytest_addoption(parser):
    parser.addoption("--accel_cmd", action="store", default="accel-cmd")
    parser.addoption("--accel_pppd", action="store", default="accel-pppd")
    parser.addoption("--pppd", action="store", default="pppd")  # pppd client
    parser.addoption(
        "--accel_pppd_max_wait_time", action="store", default=5.0
    )  # start timeout
    parser.addoption(
        "--accel_pppd_max_finish_time", action="store", default=10.0
    )  # fininsh timeout (before kill)


# accel-pppd executable file name
@pytest.fixture()
def accel_pppd(pytestconfig):
    return pytestconfig.getoption("accel_pppd")


# accel-cmd executable file name
@pytest.fixture()
def accel_cmd(pytestconfig):
    return pytestconfig.getoption("accel_cmd")


# accel-pppd configuration as string (should be redefined by specific test)
@pytest.fixture()
def accel_pppd_config():
    return ""


# accel-pppd configuration file name
@pytest.fixture()
def accel_pppd_config_file(accel_pppd_config):
    # test setup:
    filename = config.make_tmp(accel_pppd_config)

    # test execution
    yield filename

    # test teardown:
    config.delete_tmp(filename)


# setup and teardown for tests that required running accel-pppd
@pytest.fixture()
def accel_pppd_instance(accel_pppd, accel_pppd_config_file, accel_cmd, pytestconfig):
    # test setup:
    is_started, accel_pppd_thread, accel_pppd_control = accel_pppd_process.start(
        accel_pppd,
        ["-c" + accel_pppd_config_file],
        accel_cmd,
        pytestconfig.getoption("accel_pppd_max_wait_time"),
    )

    # test execution:
    yield is_started

    # test teardown:
    accel_pppd_process.end(
        accel_pppd_thread,
        accel_pppd_control,
        accel_cmd,
        pytestconfig.getoption("accel_pppd_max_finish_time"),
    )


# setup and teardown for netns and veth pair
@pytest.fixture()
def veth_pair_netns():
    # test setup:
    veth_pair_netns_instance = veth.create_veth_pair_netns()

    # test execution:
    yield veth_pair_netns_instance

    # test teardown:
    veth.delete_veth_pair_netns(veth_pair_netns_instance)


# pppd executable file name
@pytest.fixture()
def pppd(pytestconfig):
    return pytestconfig.getoption("pppd")


# pppd configuration as string (should be redefined by specific test)
# all configs should contain "nodetach" option
@pytest.fixture()
def pppd_config():
    return ""


# pppd configuration as command line args
@pytest.fixture()
def pppd_args(pppd_config):
    return pppd_config.split()


# setup and teardown for tests that required running pppd (after accel-pppd)
@pytest.fixture()
def pppd_instance(accel_pppd_instance, veth_pair_netns, pppd, pppd_args):
    # test setup:
    print("pppd_instance: accel_pppd_instance = " + str(accel_pppd_instance))
    is_started, pppd_thread, pppd_control = pppd_process.start(
        veth_pair_netns["netns"],
        pppd,
        pppd_args,
    )

    # test execution:
    yield is_started

    # test teardown:
    pppd_process.end(pppd_thread, pppd_control)
