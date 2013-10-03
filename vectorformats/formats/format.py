
class Format(object):
    """Base Format class. To set properties on your subclasses, you can
       pass them as kwargs to your format constructor."""
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def encode(self, features, **kwargs):
        ''' encodes a list of features '''
        raise NotImplementedError("Not implemented")
    
    def encode_exception_report(self, exception_report, **kwargs):
        ''' encoding a exception report '''
        raise NotImplementedError("Not implemented")

    def decode(self, data, **kwargs):
        ''' decodes data to a vector format '''
        raise NotImplementedError("Not implemented")


    def getFormatedAttributName(self, name):
        attrib_name = name
        
        attrib_pos = name.find(' as "')
        if attrib_pos >= 0:
            attrib_name = name[attrib_pos+5:-1]
            
        return attrib_name
    
    def escapeSQL(self, value):
        newValue = value
        newValue = value.replace("'", "''")
        
        return newValue 
    