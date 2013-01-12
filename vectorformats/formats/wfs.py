import re

from .format import Format

class WFS(Format):
    """WFS-like GML writer."""
    layername = "layer"
    namespaces = {'fs' : 'http://featureserver.org/fs',
                  'wfs' : 'http://www.opengis.net/wfs',
                  'ogc' : 'http://www.opengis.net/ogc',
                  'xsd' : 'http://www.w3.org/2001/XMLSchema',
                  'gml' : 'http://www.opengis.net/gml',
                  'xsi' : 'http://www.w3.org/2001/XMLSchema-instance'}
    
    def encode(self, features, **kwargs):
        results = ["""<?xml version="1.0" ?><wfs:FeatureCollection
   xmlns:fs="http://featureserver.org/fs"
   xmlns:wfs="http://www.opengis.net/wfs"
   xmlns:gml="http://www.opengis.net/gml"
   xmlns:ogc="http://www.opengis.net/ogc"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">
        """]
        for feature in features:
            results.append( self.encode_feature(feature))
        results.append("""</wfs:FeatureCollection>""")
        
        return "\n".join(results)        
    
    def encode_feature(self, feature):
        layername = re.sub(r'\W', '_', feature.layer)
        
        attr_fields = [] 
        for key, value in feature.properties.items():           
            #key = re.sub(r'\W', '_', key)
            attr_value = value
            if hasattr(attr_value,"replace"): 
                attr_value = attr_value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if isinstance(attr_value, str):
                attr_value = unicode(attr_value, "utf-8")
            attr_fields.append( "<fs:%s>%s</fs:%s>" % (key, attr_value, key) )
            
        
        xml = "<gml:featureMember gml:id=\"%s\"><fs:%s fid=\"%s\">" % (str(feature.id), layername, str(feature.id))
        
        if hasattr(feature, "geometry_attr"):
            xml += "<fs:%s>%s</fs:%s>" % (feature.geometry_attr, self.geometry_to_gml(feature.geometry, feature.srs), feature.geometry_attr)
        else:
            xml += self.geometry_to_gml(feature.geometry, feature.srs)
        
        xml += "%s</fs:%s></gml:featureMember>" % ("\n".join(attr_fields), layername)  
        return xml
    
    def geometry_to_gml(self, geometry, srs):
        """
        >>> w = WFS()
        >>> print w.geometry_to_gml({'type':'Point', 'coordinates':[1.0,2.0]})
        <gml:Point><gml:coordinates>1.0,2.0</gml:coordinates></gml:Point>
        >>> w.geometry_to_gml({'type':'LineString', 'coordinates':[[1.0,2.0],[2.0,1.0]]})
        '<gml:LineString><gml:coordinates>1.0,2.0 2.0,1.0</gml:coordinates></gml:LineString>'
        """
        
        if "EPSG" not in str(srs):
            srs = "EPSG:" + str(srs)
        
        if geometry['type'] == "Point":
            coords = ",".join(map(str, geometry['coordinates']))
            return "<gml:Point srsName=\"%s\"><gml:coordinates decimal=\".\" cs=\",\" ts=\" \">%s</gml:coordinates></gml:Point>" % (str(srs), coords)
            #coords = " ".join(map(str, geometry['coordinates']))
            #return "<gml:Point srsDimension=\"2\" srsName=\"%s\"><gml:pos>%s</gml:pos></gml:Point>" % (str(srs), coords)
        elif geometry['type'] == "LineString":
            coords = " ".join(",".join(map(str, coord)) for coord in geometry['coordinates'])
            return "<gml:LineString><gml:coordinates decimal=\".\" cs=\",\" ts=\" \" srsName=\"%s\">%s</gml:coordinates></gml:LineString>" % (str(srs), coords)
            #return "<gml:curveProperty><gml:LineString srsDimension=\"2\" srsName=\"%s\"><gml:coordinates>%s</gml:coordinates></gml:LineString></gml:curveProperty>" % (str(srs), coords)
        elif geometry['type'] == "Polygon":
            coords = " ".join(map(lambda x: ",".join(map(str, x)), geometry['coordinates'][0]))
            #out = """
            #    <gml:exterior>
            #        <gml:LinearRing>
            #            <gml:coordinates decimal=\".\" cs=\",\" ts=\" \">%s</gml:coordinates>
            #        </gml:LinearRing>
            #    </gml:exterior>
            #""" % coords 
            out = """
                <gml:exterior>
                    <gml:LinearRing srsDimension="2">
                        <gml:coordinates>%s</gml:coordinates>
                    </gml:LinearRing>
                </gml:exterior>
            """ % coords 
            
            inner_rings = []
            for inner_ring in geometry['coordinates'][1:]:
                coords = " ".join(map(lambda x: ",".join(map(str, x)), inner_ring))
                #inner_rings.append("""
                #    <gml:interior>
                #        <gml:LinearRing>
                #            <gml:coordinates decimal=\".\" cs=\",\" ts=\" \">%s</gml:coordinates>
                #        </gml:LinearRing>
                #    </gml:interior>
                #""" % coords) 
                inner_rings.append("""
                    <gml:interior>
                        <gml:LinearRing srsDimension="2">
                            <gml:coordinates>%s</gml:coordinates>
                        </gml:LinearRing>
                    </gml:interior>
                """ % coords) 
            
            return """
                            <gml:Polygon srsName="%s">
                                %s %s
                            </gml:Polygon>""" % (srs, out, "".join(inner_rings))
        else:
            raise Exception("Could not convert geometry of type %s." % geometry['type'])
    
    
    def encode_exception_report(self, exceptionReport):
        results = ["""<?xml version="1.0" encoding="UTF-8"?>
        <ExceptionReport xmlns="http://www.opengis.net/ows/1.1"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.opengis.net/ows/1.1 owsExceptionReport.xsd"
        version="1.0.0"
        xml:lang="en">
        """]
        for exception in exceptionReport:
            results.append("<Exception exceptionCode=\"%s\" locator=\"%s\" layer=\"%s\"><ExceptionText>%s</ExceptionText><ExceptionDump>%s</ExceptionDump></Exception>" % (exception.code, exception.locator, exception.layer, exception.message, exception.dump))
        results.append("""</ExceptionReport>""")
        return "\n".join(results)
    
    def encode_transaction(self, response, **kwargs):
        failedCount = 0
        
        summary = response.getSummary()
        result = """<?xml version="1.0" encoding="UTF-8"?>
        <wfs:TransactionResponse version="1.1.0"
            xsi:schemaLocation='http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd'
            xmlns:og="http://opengeo.org"
            xmlns:ogc="http://www.opengis.net/ogc"
            xmlns:tiger="http://www.census.gov"
            xmlns:cite="http://www.opengeospatial.net/cite"
            xmlns:nurc="http://www.nurc.nato.int"
            xmlns:sde="http://geoserver.sf.net"
            xmlns:analytics="http://opengeo.org/analytics"
            xmlns:wfs="http://www.opengis.net/wfs"
            xmlns:topp="http://www.openplans.org/topp"
            xmlns:it.geosolutions="http://www.geo-solutions.it"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:sf="http://www.openplans.org/spearfish"
            xmlns:ows="http://www.opengis.net/ows"
            xmlns:gml="http://www.opengis.net/gml"
            xmlns:za="http://opengeo.org/za"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:tike="http://opengeo.org/#tike">
                <wfs:TransactionSummary>
                    <wfs:totalInserted>%s</wfs:totalInserted>
                    <wfs:totalUpdated>%s</wfs:totalUpdated>
                    <wfs:totalDeleted>%s</wfs:totalDeleted>
                    <wfs:totalReplaced>%s</wfs:totalReplaced>
                </wfs:TransactionSummary>
            <wfs:TransactionResults/> """ % (str(summary.getTotalInserted()), str(summary.getTotalUpdated()), str(summary.getTotalDeleted()), str(summary.getTotalReplaced()))
        
        insertResult = response.getInsertResults()
        result += "<wfs:InsertResults>"
        for insert in insertResult:
            result += """<wfs:Feature handle="%s">
                    <ogc:ResourceId fid="%s"/>
                </wfs:Feature>""" % (str(insert.getHandle()), str(insert.getResourceId()))
            if len(insert.getHandle()) > 0:
                failedCount += 1
        result += """</wfs:InsertResults>"""

        updateResult = response.getUpdateResults()
        result += "<wfs:UpdateResults>"
        for update in updateResult:
            result += """<wfs:Feature handle="%s">
                    <ogc:ResourceId fid="%s"/>
                </wfs:Feature>""" % (str(update.getHandle()), str(update.getResourceId()))
            if len(update.getHandle()) > 0:
                failedCount += 1

        result += """</wfs:UpdateResults>"""

        replaceResult = response.getReplaceResults()
        result += "<wfs:ReplaceResults>"
        for replace in replaceResult:
            result += """<wfs:Feature handle="%s">
                    <ogc:ResourceId fid="%s"/>
                </wfs:Feature>""" % (str(replace.getHandle()), str(replace.getResourceId()))
            if len(replace.getHandle()) > 0:
                failedCount += 1
        result += """</wfs:ReplaceResults>"""
        
        
        deleteResult = response.getDeleteResults()
        result += "<wfs:DeleteResults>"
        for delete in deleteResult:
            result += """<wfs:Feature handle="%s">
                <ogc:ResourceId fid="%s"/>
                </wfs:Feature>""" % (str(delete.getHandle()), str(delete.getResourceId()))
            if len(delete.getHandle()) > 0:
                failedCount += 1
        result += """</wfs:DeleteResults>"""

        
        result += """<wfs:TransactionResult> 
                        <wfs:Status> """
        
        if (len(insertResult) + len(updateResult) + len(replaceResult)) == failedCount:
            result += "<wfs:FAILED/>"
        elif (len(insertResult) + len(updateResult) + len(replaceResult)) > failedCount and failedCount > 0:
            result += "<wfs:PARTIAL/>"
        else:
            result += "<wfs:SUCCESS/>"
                        
                        
        result += """</wfs:Status>
                </wfs:TransactionResult>""" 


        result += """</wfs:TransactionResponse>"""
        
        return result

