from unittest import TestSuite

import wkt
import kml
import gpx
import csv
import geojson


def test_suite():
    suite = TestSuite()
    suite.addTest(wkt.test_suite())
    suite.addTest(kml.test_suite())
    suite.addTest(gpx.test_suite())
    suite.addTest(csv.test_suite())
    suite.addTest(geojson.test_suite())
    return suite
