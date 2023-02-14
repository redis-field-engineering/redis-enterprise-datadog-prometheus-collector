import prometheus_client
from prometheus_client import Gauge, Info

# Disable collection of Python platform metrics
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

class MetricsExporter:
    def __init__(self):
        self.throughput_gauge = Gauge("redise_estimated_max_throughput", "Estimated max throughput", ["database"])
        self.persistence_info = Info("redise_data_persistence", "Indicate the type of data persistence enabled", ["database"])

    def update(self, metrics):
        if metrics.estimated_ops_per_second != None:
            self.throughput_gauge.labels(database=metrics.database_name).set(metrics.estimated_ops_per_second)
        if metrics.data_persistence != None:
            self.persistence_info.labels(database=metrics.database_name).info({"persistence": metrics.data_persistence})