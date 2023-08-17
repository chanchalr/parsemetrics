import unittest
import iterative_metrics

class TestMetricsParser(unittest.TestCase):
    def test_metrics_parser(self):
        parser = iterative_metrics.metric_parser("./config.yaml")
        print("testing parse repo")
        parser.parse_repo('/Users/chanchalr/personal/iterative/testrepo','test/metrics/data.json')
        first_commit = parser.fetch_repo_data(count=1)
        print(first_commit)
        second_commit = parser.fetch_repo_data(commit_id=first_commit[0]["commit_id"],count=1)
        print(second_commit)
        first_again = parser.fetch_repo_data(commit_id=second_commit[0]["commit_id"],count=1,direction="back")
        self.assertEqual(first_again[0]["commit_id"],first_commit[0]["commit_id"])



if __name__ =='__main__':
    unittest.main()