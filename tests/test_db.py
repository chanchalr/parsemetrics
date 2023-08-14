import unittest
import iterative_metrics

class TestDb(unittest.TestCase):
    def test_db_conn(self):
        config = iterative_metrics.config.config("./config.yaml")
        #db = iterative_metrics.db.postgresdb.postgres_db(config.get_component("database"))
        db = iterative_metrics.db.getDb(config.get_component("database"))

if __name__ =='__main__':
    unittest.main()