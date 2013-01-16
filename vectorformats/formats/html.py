from .format import Format

from Cheetah.Template import Template

class HTML (Format):
    """Uses Cheetah to format a list of features."""

    default_file = "assets/templates/default.html"
    exception_file = "assets/templates/exception_report.html"
    """Default template file to use."""

    def encode(self, result, **kwargs):
        template = self.template(self.default_file)

        output = Template(template, searchList = [{'features':result, 'datasource':self.datasource.name}, self])
        
        return str(output)

    def encode_exception_report(self, exceptionReport):
        template = self.template(self.exception_file)
        
        output = Template(template, searchList = [{'exception_report':exceptionReport}, self])
        
        return str(output)
    
    
    def template(self, template_file):
        return file(template_file).read()
