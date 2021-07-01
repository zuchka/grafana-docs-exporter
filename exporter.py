import time, re
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
                if re.match(r'^https', item):
                    g = GaugeMetricFamily("flesch_score", 'flesch reading ease score per URL', labels=["url"])
                    g.add_metric([item], result[item])
                    yield g
                elif re.match(r'^flesch_average', item):
                    gm = GaugeMetricFamily("average_fre", 'overall FRE for docs repo', labels=["average"])
                    gm.add_metric([item], result[item])
                    yield gm
                elif re.match(r'^docs_sum', item):
                    gs = GaugeMetricFamily("docs_sum", 'total number of docs in /latest', labels=["sum"])
                    gs.add_metric([item], result[item])
                    yield gs


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(3600)
