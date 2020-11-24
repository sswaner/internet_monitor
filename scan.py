import socket
import logging 
import time
import platform


class HostnameFilter(logging.Filter):
    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True

log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(hostname)s - %(message)s')
handler = logging.FileHandler('netscan.log')
handler.addFilter(HostnameFilter())
handler.setFormatter(log_format)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(log_format)
log = logging.getLogger()
log.addHandler(handler)
log.setLevel(logging.INFO)
log.addHandler(sh)

log.info("script starting")

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

prior_status = True
prior_count = 0

while True:
    test = internet()
    if test:
        log.info(f"SUCCESS, ITERATIONS:{prior_count}")
    else:
        log.warning(f"FAIL, ITERATIONS:{prior_count}")
    # success to fail
    if not test and prior_status:
        log.warning(f"SERVICE DOWN, PRIOR ITERATIONS:{prior_count}")
        prior_count = 0
        prior_status = test
    # fail to success
    if test and not prior_status:
        log.warning(f"SERVICE UP, PRIOR_ITERATIONS:{prior_count}")
        prior_count = 0
        prior_status = test
    # no status change
    if test == prior_status:
        prior_count += 1
        prior_status = test

    time.sleep(60)

log.warning("Script Terminated")


