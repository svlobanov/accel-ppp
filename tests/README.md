# Requirements

These tests are done for Ubuntu and Debian distros. Please use latest stable Debian or Ubuntu to run the tests.

## Preparations

Install pytest

Using apt: `sudo apt install python3-pytest` or using pip: `sudo pip3 install pytest`

---
Note: tests will be run under sudo. If you prefer install python modules using pip, then do it under sudo as described above.

---

Install additional tools required for tests:
``` bash
sudo apt install iproute2 pppoe
```

Then build accel-ppp in 'build' directory (as usual)

Install accel-pppd (make install or use distro package). Do not run accel-pppd using systemd or other supervisors


## Run tests (without coverage)

```bash
# from root dir (parent for this dir)
sudo python3 -m pytest -Wall tests -v
```

## Preparations (for coverage report)

Perform preparation steps for running tests  without coverage

Install gcovr

Using apt:
```bash
sudo apt install gcovr
```

Using pip
```bash
sudo pip3 install gcovr
```

```bash
# from root dir
mkdir build
cd build
cmake -DCMAKE_C_FLAGS="--coverage -O0" ..
make
sudo make install
```
(Add all other cmake options you need)

## Run tests and generate coverage report

```bash
# from root dir (parent for this dir)
sudo python3 -m pytest -Wall tests -v
sudo gcovr --config=tests/gcovr.conf # default report
sudo gcovr --config=tests/gcovr.conf --csv # csv report
sudo gcovr --config=tests/gcovr.conf --html --html-details --output=tests/report/accel-ppp.html # html reports (most useful)
```

(If `gcovr` command does not exist, use `python3 -m gcovr` instead)

## Remove coverage data

If you want to re-run tests 'from scratch', you may want to remove coverage data. To do this:

```bash
# from root dir (parent for this dir)
sudo gcovr -d # build report and delete
sudo gcovr -d # check that data is deleted (any coverage = 0%)
```