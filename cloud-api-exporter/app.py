import time
from prometheus_client import start_http_server
import argparse
from exporter.database_metrics import DatabaseMetrics, DatabaseMetricsTransformer
from exporter.metrics_exporter import MetricsExporter
from exporter.fetcher import MetricsFetcher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'Redis Cloud API Prometheus Exporter',
                    description = 'Expose Redis Cloud API stats through Prometheus')
    parser.add_argument('-a', '--api-account-key', required=True)
    parser.add_argument('-u', '--api-user-secret-key', required=True)
    parser.add_argument('-e', '--database-endpoint', required=True)

    args = parser.parse_args()

    fetcher = MetricsFetcher(args.database_endpoint, args.api_account_key, args.api_user_secret_key)
    transformer = DatabaseMetricsTransformer()
    exporter = MetricsExporter()
    start_http_server(8000)
    while(True):
        stats = fetcher.fetch_database_metrics()
        for stat in stats:
            metrics = transformer.get_database_metrics(stat)
            exporter.update(metrics)
        time.sleep(30)