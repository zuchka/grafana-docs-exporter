## grafana-docs-exporter

### A Prometheus exporter for monitoring & analyzing Grafana Labs' technical documentation

[public endpoint](https://readability.zuchka.dev)

![grafana-docs-exporter dashboard](./dashboard.png)

* note: this app uses a forked version of [py-readability-metrics](https://github.com/cdimascio/py-readability-metrics). That library will not analyze strings with less than 100 words.