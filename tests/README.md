# Requirements

Tests are done for Ubuntu and Debian distros. Please use latest stable Debian or Ubuntu to run tests.

## Preparations

Install pytest

Using apt: `apt install python3-pytest` or using pip: `pip3 install pytest`

Install additional tools required for tests:
``` bash
apt install iproute2 pppoe sudo
```

Then build accel-ppp in 'build' directory (as usual)
Install accel-pppd (make install or use distro package). Do not run accel-pppd using systemd or other supervisors

Most tests require `sudo` for running accel-pppd run. Please configure to allow run sudo without a password

## Run tests (without coverage)

```bash
# from root dir (parent for this dir)
python3 -m pytest -Wall tests -v
```

## Preparations (for coverage report)

Perform preparation steps for running tests  without coverage

Install gcovr

Using apt:
```bash
apt install gcovr
```

Using pip
```bash
pip3 install gcovr
```

```bash
# from root dir
mkdir build
cd build
cmake -DCMAKE_C_FLAGS="--coverage -O0" ..
make
```
(Add all other cmake options you need)

## Run tests and generate coverage report

```bash
# from root dir (parent for this dir)
python3 -m pytest -Wall tests -v
gcovr --config=tests/gcovr.conf # default report
gcovr --config=tests/gcovr.conf --csv # csv report
gcovr --config=tests/gcovr.conf --html --html-details --output=tests/report/accel-ppp.html # html reports (most useful)
```

(If `gcovr` command does not exist, use `python3 -m gcovr` instead)

## Remove coverage data

If you want to re-run tests 'from scratch', you may want to remove coverage data. To do this:

```bash
# from root dir (parent for this dir)
gcovr -d # build report and delete
gcovr -d # check that data is deleted (any coverage = 0%)
```