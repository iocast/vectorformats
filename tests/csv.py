import unittest

from vectorformats.formats.csv import CSV
from vectorformats.feature import Feature

from .base import BaseTest


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


    def test_encode(self):
        feat = Feature(1, {"type":"Point", "coordinates":[1,1]}, {"a":"b"})
        c = CSV()
        self.assertEqual('id,geometry 1,POINT(1.000000 1.000000) ', c.encode([feat]).getvalue().replace("\r\n", " "))
        self.assertEqual('geometry,a,b,id POINT(1.000000 1.000000),,,1 ', c.encode([feat], ["geometry","a","b","id"]).getvalue().replace("\r\n", " "))
        self.assertEqual('geometry,id POINT(1.000000 1.000000),1 ', c.encode([feat], props=["geometry","id"],fixed_props=True).getvalue().replace("\r\n", " "))


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(CSVTestCase)
