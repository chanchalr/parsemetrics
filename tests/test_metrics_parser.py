import unittest
import iterative_metrics

class TestMetricsParser(unittest.TestCase):
    def test_metrics_parser(self):
        parser = iterative_metrics.metric_parser("./config.yaml")
        parser.parse_repo('/Users/chanchalr/personal/iterative/testrepo','test/metrics/data.json')

if __name__ =='__main__':
    unittest.main()