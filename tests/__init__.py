from unittest import TestSuite

import wkt
import kml
import gpx
import csv


def test_suite():
    suite = TestSuite()
    suite.addTest(wkt.test_suite())
    suite.addTest(kml.test_suite())
    suite.addTest(gpx.test_suite())
    suite.addTest(csv.test_suite())
    return suite
