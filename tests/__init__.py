from unittest import TestSuite

import wkt, kml, gpx, csv, html

def test_suite():
    suite = TestSuite()
    suite.addTest(wkt.test_suite())
    suite.addTest(kml.test_suite())
    suite.addTest(gpx.test_suite())
    suite.addTest(csv.test_suite())
    suite.addTest(html.test_suite())
    return suite
