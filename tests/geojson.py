import unittest

from vectorformats.formats.geojson import GeoJSON

from base import BaseTest


class GeoJSONTestCase(BaseTest):

    def decode(self, filename, **kwargs):
        content = self.read_file(filename)
        geojson = GeoJSON(**kwargs)
        return geojson.decode(content)

    def test_simple_point(self):
        features = self.decode('simple_point.json')
        point = features[0]
        self.assertEqual(len(features), 1)  # one is invalid, so not imported
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [125.6, 10.1])
        self.assertEqual(point.properties['name'], 'Dinagat Islands')

    def test_collection(self):
        features = self.decode('collection.json')
        self.assertEqual(len(features), 3)
        point = features[0]
        self.assertEqual(point.geometry['type'], 'Point')
        self.assertEqual(point.geometry['coordinates'], [102.0, 0.5])
        self.assertEqual(point.properties['prop0'], 'value0')
        linestring = features[1]
        self.assertEqual(linestring.geometry['type'], 'LineString')
        polygon = features[2]
        self.assertEqual(polygon.geometry['type'], 'Polygon')

    def test_encode(self):
        content = self.read_file('collection.json')
        geojson = GeoJSON()
        features = geojson.decode(content)
        data = GeoJSON.encode(geojson, features, to_string=False, bbox=True)
        self.assertEqual(data['type'], 'FeatureCollection')

    def test_bbox(self):
        content = self.read_file('collection.json')
        geojson = GeoJSON()
        features = geojson.decode(content)
        data = GeoJSON.encode(geojson, features, to_string=False, bbox=True)
        self.assertEqual(data['bbox'], [100.0, 0.0, 105.0, 1.0])

def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(GeoJSONTestCase)
