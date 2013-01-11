from unittest import TestSuite

import kml, gpx

def test_suite():
    suite = TestSuite()
    suite.addTest(kml.test_suite())
    suite.addTest(gpx.test_suite())
    return suite