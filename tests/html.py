import unittest

from .base import BaseTest

from vectorformats.formats.html import HTML
from vectorformats.exceptions import ExceptionReport, BaseException

class HTMLTestCase(BaseTest):
    
    def setUp(self):
        self.report = ExceptionReport()
        self.report.add(BaseException("this is a HTML exception test", 500, self.__class__.__name__, "na", "na", "empty"))
        self.report.add(BaseException("this is an other exception test", 501, self.__class__.__name__, "na", "na", "empty"))
    
    def test_from_html_exception_report(self):
        self.assertIn("<td>500</td>", self.report.encode_exception_report())
        self.assertIn("<td>501</td>", self.report.encode_exception_report())


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(HTMLTestCase)
