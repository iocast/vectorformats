'''
Created on Jul 30, 2011

@author: michel
'''

import types

from xml.sax.saxutils import escape
from xml.dom import minidom

from ..feature import Feature
from .format import Format


class GPX(Format):

    def encode(self, features, **kwargs):
        results = ["""<?xml version="1.0" encoding="UTF-8"?>
        <gpx version="1.0">"""]
        results.append("<name>%s</name>" % self.layername)

        for feature in features:
            results.append(self.encode_feature(feature))

        results.append("</gpx>")
        return "\n".join(results)

    def encode_feature(self, feature):
        xml = []

        if feature.geometry['type'] == 'Point':
            xml.append("""<wpt lon="%s" lat="%s">""" % (str(feature.geometry["coordinates"][0]), str(feature.geometry["coordinates"][1])))
            if "name" in feature.properties:
                if isinstance(feature.properties["name"], types.NoneType):
                    xml.append("""<name>%s</name>""" % str(feature.id))
                else:
                    xml.append("""<name>%s</name>""" % escape(feature.properties["name"]))
            else:
                xml.append("""<name>%s</name>""" % str(feature.id))
            if "ele" in feature.properties:
                xml.append("""<ele>%s</ele>""" % feature.properties["ele"])
            xml.append("""</wpt>""")

        elif feature.geometry['type'] == 'LineString':
            xml.append("<trk>")

            if "name" in feature.properties:
                if isinstance(feature.properties["name"], types.NoneType):
                    xml.append("""<name>%s</name>""" % str(feature.id))
                else:
                    xml.append("""<name>%s</name>""" % escape(feature.properties["name"]))
            else:
                xml.append("""<name>%s</name>""" % str(feature.id))

            xml.append("<trkseg>")

            coords = feature["geometry"]["coordinates"]
            for coord in coords:
                xml.append("""<trkpt lon="%s" lat="%s">""" % (str(coord[0]), str(coord[1])))

                if "ele" in feature.properties:
                    xml.append("""<ele>%s</ele>""" % feature.properties["ele"])

                xml.append("</trkpt>")

            xml.append("</trkseg></trk>")

        elif feature.geometry['type'] == 'Polygon':
            xml.append("<trk>")

            if "name" in feature.properties:
                if isinstance(feature.properties["name"], types.NoneType):
                    xml.append("""<name>%s</name>""" % str(feature.id))
                else:
                    xml.append("""<name>%s</name>""" % escape(feature.properties["name"]))
            else:
                xml.append("""<name>%s</name>""" % str(feature.id))

            xml.append("<trkseg>")

            coords = feature["geometry"]["coordinates"][0]
            for coord in coords:
                xml.append("""<trkpt lon="%s" lat="%s">""" % (str(coord[0]), str(coord[1])))

                if "ele" in feature.properties:
                    xml.append("""<ele>%s</ele>""" % feature.properties["ele"])

                xml.append("</trkpt>")

            xml.append("</trkseg></trk>")

        return "\n".join(xml)

    def decode(self, data):
        features = []

        doc = minidom.parseString(data)
        for node in doc.documentElement.childNodes:
            if node.nodeType != doc.ELEMENT_NODE:
                continue
            if node.nodeName not in ['wpt', 'trk']:
                continue
            feature = self.node_to_feature(node)
            features.append(feature)

        return features

    def node_to_feature(self, node):
        feature = Feature()
        if node.nodeName == "wpt":
            coords = self.node_to_coordinates(node)
            feature.geometry = {
                'type': 'Point',
                'coordinates': coords
            }
        elif node.nodeName == "trk":
            coords = []
            for subnode in node.getElementsByTagName('trkseg')[0].childNodes:
                if subnode.nodeType != node.ELEMENT_NODE:
                    continue
                coords.append(self.node_to_coordinates(subnode))
            feature.geometry = {
                'type': 'LineString',
                'coordinates': coords
            }
        else:
            # FIXME: how to handle routes?
            # A route is a list of *ordered* waypoints
            raise Exception("GPX parser only handle waypoint and track")
        self.populate_property_from_node(node, feature, "name")
        self.populate_property_from_node(node, feature, "desc")
        self.populate_property_from_node(node, feature, "cmt")
        self.populate_property_from_node(node, feature, "sym")
        return feature

    def node_to_coordinates(self, node):
        lat = float(node.getAttribute('lat'))
        lon = float(node.getAttribute('lon'))
        coords = [lon, lat]
        if node.getElementsByTagName('ele'):
            ele = float(node.getElementsByTagName('ele')[0].firstChild.nodeValue)
            coords.append(ele)
        return coords

    def populate_property_from_node(self, node, feature, name):
        try:
            subnode = node.getElementsByTagName(name)[0]
        except IndexError:
            pass
        else:
            feature.properties[name] = subnode.firstChild.nodeValue
