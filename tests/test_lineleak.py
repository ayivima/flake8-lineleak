import pickle
import unittest

import flake8_lineleak


class PicklingTestCase(unittest.TestCase):
    def test_pickling(self):
        screener = flake8_lineleak.Screener()
        pickled = pickle.dumps(screener)
        reloaded = pickle.loads(pickled)
        self.assertEqual(screener, reloaded)


if __name__ == "__main__":
    unittest.main()
