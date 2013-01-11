import unittest

from vectorformats.formats.wkt import from_wkt, to_wkt

class WKTTestCase(unittest.TestCase):

    def test_from_wkt_multipoint(self):
        wkt = 'MULTIPOINT (1.0000000000000000 2.0000000000000000, 2.0000000000000000 3.0000000000000000)'
        self.assertEqual(from_wkt(wkt), {'type': 'MultiPoint', 'coordinates': [[1.0, 2.0], [2.0, 3.0]]})

    def test_from_wkt_point(self):
        wkt = 'POINT (1.0000000000000000 2.0000000000000000)'
        self.assertEqual(from_wkt(wkt), {'type': 'Point', 'coordinates': [1.0, 2.0]})

    def test_from_wkt_linestring(self):
        wkt = 'LINESTRING (0.0000000000000000 1.0000000000000000, 1.0000000000000000 2.0000000000000000)'
        self.assertEqual(from_wkt(wkt), {'type': 'LineString', 'coordinates': [[0.0, 1.0], [1.0, 2.0]]})

    def test_from_wkt_multilinestring(self):
        wkt = 'MULTILINESTRING ((0.0000000000000000  1.0000000000000000, 1.0000000000000000 2.0000000000000000),  (10.0000000000000000 11.0000000000000000, 11.0000000000000000  12.0000000000000000))'
        self.assertEqual(from_wkt(wkt), {'type': 'MultiLineString', 'coordinates': [[[0.0, 1.0], [1.0, 2.0]], [[10.0, 11.0], [11.0, 12.0]]]})
    
    def test_from_wkt_linestring2(self):
        wkt = 'LINESTRING (0.0000000000000000 1.0000000000000000, 1.0000000000000000 2.0000000000000000)'
        self.assertEqual(from_wkt(to_wkt(from_wkt(wkt))), {'type': 'LineString', 'coordinates': [[0.0, 1.0], [1.0, 2.0]]})

    def test_from_wkt_multipolygon(self):
        wkt = 'MULTIPOLYGON(((0 0 0,4 0 0,4 4 0,0 4 0,0 0 0),(1 1 0,2 1 0,2 2 0,1 2 0,1 1 0)),((-1 -1 0,-1 -2 0,-2 -2 0,-2 -1 0,-1 -1 0)))'
        self.assertEqual(from_wkt(wkt), {'type': 'MultiPolygon', 'coordinates': [[[0.0, 0.0, 0.0], [4.0, 0.0, 0.0], [4.0, 4.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 0.0]], [[1.0, 1.0, 0.0], [2.0, 1.0, 0.0], [2.0, 2.0, 0.0], [1.0, 2.0, 0.0], [1.0, 1.0, 0.0]], [[-1.0, -1.0, 0.0], [-1.0, -2.0, 0.0], [-2.0, -2.0, 0.0], [-2.0, -1.0, 0.0], [-1.0, -1.0, 0.0]]]})

    def test_to_wkt_multipolygon(self):
        wkt = 'MULTIPOLYGON(((0 0 0,4 0 0,4 4 0,0 4 0,0 0 0),(1 1 0,2 1 0,2 2 0,1 2 0,1 1 0)),((-1 -1 0,-1 -2 0,-2 -2 0,-2 -1 0,-1 -1 0)))'
        self.assertEqual(to_wkt(from_wkt(wkt)), 'MultiPolygon(((0.000000 0.000000 0.000000,4.000000 0.000000 0.000000,4.000000 4.000000 0.000000,0.000000 4.000000 0.000000,0.000000 0.000000 0.000000)), ((1.000000 1.000000 0.000000,2.000000 1.000000 0.000000,2.000000 2.000000 0.000000,1.000000 2.000000 0.000000,1.000000 1.000000 0.000000)), ((-1.000000 -1.000000 0.000000,-1.000000 -2.000000 0.000000,-2.000000 -2.000000 0.000000,-2.000000 -1.000000 0.000000,-1.000000 -1.000000 0.000000)))')


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(WKTTestCase)

