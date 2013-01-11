import unittest

from vectorformats.formats.kml import KML

from base import BaseTest


class KMLTestCase(BaseTest):

    def decode(self, filename, **kwargs):
        """
        Process a file an return features.
        """
        content = self.read_file(filename)
        kml = KML(**kwargs)
        return kml.decode(content)

    def test_decode_simple_point(self):
        features = self.decode("simple_point.kml")
        self.assertEqual(len(features), 1)
        point = features[0]
        self.assertEqual(point.properties['title'], 'Simple point')
        self.assertEqual(point.properties['description'], 'Here is a simple description.')
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [-122.0822035425683, 37.42228990140251, 0.0])

    def test_decode_simple_path(self):
        features = self.decode("simple_path.kml")
        self.assertEqual(len(features), 1)
        path = features[0]
        self.assertEqual(path.properties['title'], 'Simple path')
        self.assertEqual(path.properties['description'], 'Simple description')
        self.assertEqual(path.geometry['type'], 'LineString')
        self.assertEqual(path.geometry['coordinates'], [[-112.2550785337791, 36.07954952145647, 2357], [-112.2549277039738, 36.08117083492122, 2357], [-112.2552505069063, 36.08260761307279, 2357]])

    def test_decode_simple_polygon(self):
        features = self.decode("simple_polygon.kml")
        self.assertEqual(len(features), 1)
        polygon = features[0]
        self.assertEqual(polygon.properties['title'], 'Simple polygon')
        self.assertEqual(polygon.properties['description'], 'A description.')
        self.assertEqual(polygon.geometry['type'], 'Polygon')
        self.assertEqual(polygon.geometry['coordinates'], [[[-77.05788457660967, 38.87253259892824, 100.0], [-77.05465973756702, 38.87291016281703, 100.0], [-77.0531553685479, 38.87053267794386, 100.0], [-77.05552622493516, 38.868757801256, 100.0]]])


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(KMLTestCase)
