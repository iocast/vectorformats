import os

from .format import Format

from mako.template import Template

class HTML (Format):
    """Uses Mako to format a list of features."""
    
    default_file = os.path.join(os.path.dirname(__file__), "../assets/templates/default.html")
    exception_file = os.path.join(os.path.dirname(__file__), "../assets/templates/exception_report.html")

    def __init__(self, default_file=None, exception_file=None):
        if default_file is not None:
            self.default_file = default_file
        if exception_file is not None:
            self.exception_file = exception_file

    def encode(self, result, **kwargs):
        output = Template(filename=self.default_file).render(searchList = [{'features':result, 'datasource':self.datasource.name}, self])
        return str(output)

    def encode_exception_report(self, exceptionReport, **kwargs):
        return Template(filename=self.exception_file).render(exception_report=exceptionReport)
    