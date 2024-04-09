import unittest

import bcpapi
import json


class BcpApiTest(unittest.TestCase):
    def test(self):
        with open('bindays.json') as input:
            bins = json.load(input)
            input.close()

            tommorows_bins = bcpapi.tommorows_bins(bins)

            self.assertEqual(2, len(tommorows_bins))
            self.assertEqual('Food Waste', tommorows_bins[0]['BinType'])
            self.assertEqual('Rubbish', tommorows_bins[1]['BinType'])
