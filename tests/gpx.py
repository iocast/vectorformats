import unittest

from vectorformats.formats.gpx import GPX

from base import BaseTest


class GPXTestCase(BaseTest):

    def decode(self, filename, **kwargs):
        """
        Process a file an return features.
        """
        content = self.read_file(filename)
        gpx = GPX(**kwargs)
        return gpx.decode(content)

    def test_decode_simple_point(self):
        features = self.decode("simple_point.gpx")
        self.assertEqual(len(features), 1)
        point = features[0]
        self.assertEqual(point.properties['name'], 'Simple Point')
        self.assertEqual(point.properties['desc'], 'Simple description')
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [-121.72904, 45.44283, 1374.0])

    def test_decode_simple_path(self):
        features = self.decode("simple_path.gpx")
        self.assertEqual(len(features), 1)
        path = features[0]
        self.assertEqual(path.properties['name'], 'Simple path')
        self.assertEqual(path.properties['desc'], 'Simple description')
        self.assertEqual(path.geometry['type'], 'LineString')
        self.assertEqual(path.geometry['coordinates'], [[-121.7295456, 45.4431641], [-121.7290800, 45.4428615], [-121.7279085, 45.4425697]])

    def test_decode_simple_point_with_empty_field(self):
        features = self.decode("empty_field.gpx")
        self.assertEqual(len(features), 1)
        point = features[0]
        self.assertNotIn('name', point.properties)
        self.assertEqual(point.properties['desc'], 'Simple description')
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [-121.72904, 45.44283, 1374.0])


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(GPXTestCase)
