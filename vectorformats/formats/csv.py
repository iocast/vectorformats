from __future__ import absolute_import
import csv
import StringIO

from .format import Format
from .wkt import to_wkt
from ..feature import Feature


class CSV (Format):
    """Encode simple features to CSV; supports only point geometries."""

    include_id = True

    def encode(self, features, props=None, fixed_props=False, **kwargs):
        """
        >>> feat = Feature(1, {"type":"Point", "coordinates":[1,1]}, {"a":"b"})
        >>> c = CSV()
        >>> c.encode([feat]).replace("\\r\\n", " ")
        'id,a,geometry 1,b,"1,1" '
        >>> c.encode([feat], ["geometry","a","b","id"]).replace("\\r\\n", " ")
        'geometry,a,b,id "1,1",b,,1 '
        >>> c.encode([feat], props=["geometry","id"],fixed_props=True).replace("\\r\\n", " ")
        'geometry,id "1,1",1 '
        """

        s = StringIO.StringIO()
        w = csv.writer(s)

        if props is None:
            props = []

        if not "id" in props and self.include_id:
            props.append("id")

        if not fixed_props:
            for feature in features:
                for key in feature.properties.keys():
                    if not key in props:
                        props.append(key)

        if not "geometry" in props:
            props.append("geometry")

        w.writerow(props)

        for feature in features:
            #if feature.geometry['type'] != "Point":
            #    continue
            row = []
            for key in props:
                if key == "id":
                    row.append(feature.id)
                elif key == "geometry":
                    geom = to_wkt(feature.geometry)
                    #geom = ",".join(map(str, feature.geometry['coordinates']))
                    row.append(geom)
                elif key in feature.properties:
                    val = feature.properties[key]
                    if isinstance(val, unicode):
                        val = val.encode("utf-8")
                    row.append(val)
                else:
                    row.append("")
            w.writerow(row)
        s.seek(0)
        return s

    def encode_exception_report(self, exceptionReport):
        s = StringIO.StringIO()
        w = csv.writer(s)

        w.writerow(["exceptionCode", "locator", "layer", "ExceptionText", "ExceptionDump"])

        for exception in exceptionReport:
            w.writerow([str(exception.code), exception.locator, exception.layer, exception.message, exception.dump])

        return s

    def determine_col(self, strings):
        for idx, col in enumerate(self.first_row):
            col = col.lower()
            for s in strings:
                if col.startswith(s) or col.endswith(s):
                    return idx
        return None

    def decode(self, data):
        features = []
        reader = csv.reader(data.split('\n'), delimiter=",")
        for idx, row in enumerate(reader):
            if not row:
                continue
            if idx == 0:
                self.first_row = row
                # Determine cols name
                latitude_index = self.determine_col(['lat', 'latitude', ])
                longitude_index = self.determine_col(['lon', 'lng', 'longitude', ])
                if latitude_index is None or longitude_index is None:
                    break
            else:
                feature = Feature()
                lat = float(row[latitude_index])
                lng = float(row[longitude_index])
                feature.geometry = {'type': 'Point', 'coordinates': [lng, lat]}
                feature.properties.update(dict(zip(self.first_row, row)))
                features.append(feature)
        return features
