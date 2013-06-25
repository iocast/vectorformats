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
        self.assertEqual(len(features), 4)  # one is invalid, so not imported
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [-124.401, 40.576])
        self.assertEqual(point.properties['Magnitude'], '1.5')

    def test_tab_separated_values(self):
        features = self.decode('point_list.tsv')
        point = features[0]
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [-124.401, 40.576])
        self.assertEqual(point.properties['col1'], 'blah')

    def test_semi_colon_separated_values(self):
        features = self.decode('point_list.scsv')
        point = features[0]
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [-124.401, 40.576])
        self.assertEqual(point.properties['col1'], 'blah')


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(CSVTestCase)
