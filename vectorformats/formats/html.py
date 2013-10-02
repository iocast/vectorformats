import os

from .format import Format

from mako.template import Template

class HTML (Format):
    """Uses Mako to format a list of features."""
    
    default_file = os.path.join(os.path.dirname(__file__), "../assets/templates/default.html")
    exception_file = os.path.join(os.path.dirname(__file__), "../assets/templates/exception_report.html")
    """Default template file to use."""

    def encode(self, result, **kwargs):
        output = Template(filename=self.default_file).render(searchList = [{'features':result, 'datasource':self.datasource.name}, self])
        return str(output)

    def encode_exception_report(self, exceptionReport, *args, **kwargs):
        return Template(filename=self.exception_file).render(exception_report=exceptionReport)
