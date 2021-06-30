import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
from script import script

results = script()

# iterate over results and add metrics for each url in grafana docs
class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        for result in results:
            for item in result:
                g = GaugeMetricFamily("FleschScore", 'Help text', labels=["url"])
                g.add_metric([item], result[item])
                yield g


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(3600)
