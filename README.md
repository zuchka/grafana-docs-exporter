## grafana-docs-exporter

### A Prometheus exporter for monitoring & analyzing Grafana Labs' technical documentation

[public endpoint](https://readability.zuchka.dev)

![grafana-docs-exporter dashboard](./dashboard.png)

This exporter uses `git` to pull the newest versions of Grafana's documentation from the official repo. It then programmatically builds all the URLs to scrape those pages, just like Hugo does when it builds the actual documentation pages. These URLs are then scraped, parsed, analyzed, and exposed in Prometheus format for scraping. 

To add these metrics to your own Prometheus instance, just add this job to your `prometheus.yml`:

```yml
  - job_name: 'grafanadocs_hosted'
    scheme: https
    metrics_path: '/'
    static_configs:
    - targets: ['readability.zuchka.dev']
```

* note: this app uses a forked version of [py-readability-metrics](https://github.com/cdimascio/py-readability-metrics). That library will not analyze strings with less than 100 words.