import unittest

from vectorformats.formats.csv import CSV

from base import BaseTest


class CSVTestCase(BaseTest):

    def decode(self, filename, **kwargs):
        """
        Process a file an return features.
        """
        content = self.read_file(filename)
        csv = CSV(**kwargs)
        return csv.decode(content)

    def test_simple_load(self):
        features = self.decode('point_list.csv')
        point = features[0]
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [-124.401, 40.576])
        self.assertEqual(point.properties['Magnitude'], '1.5')


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(CSVTestCase)
