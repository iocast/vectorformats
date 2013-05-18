class Feature (object):

    def __init__(self, id=None, geometry=None, geometry_attr=None, srs=None,
                 props=None, layer=None):
        self._layer = layer
        self._id = id
        self._geometry = geometry
        self._geometry_attr = geometry_attr
        self._srs = srs
        self._properties = props or {}

    @property
    def layer(self):
        return self._layer

    @property
    def id(self):
        return self._id

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        self._geometry = geometry

    @property
    def geometry_attribute(self):
        return self._geometry_attr

    @geometry_attribute.setter
    def geometry_attribute(self, value):
        self._geometry_attr = value

    @property
    def srs(self):
        return self._srs

    @srs.setter
    def srs(self, value):
        self._srs = value

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = properties

    def get_bbox(self):
        minx = miny = 2**31
        maxx = maxy = -2**31
        try:

            coords = self.geometry["coordinates"]

            if self.geometry["type"] == "Point":
                minx = coords[0]
                maxx = coords[0]
                miny = coords[1]
                maxy = coords[1]

            elif self.geometry["type"] == "LineString":
                for coord in coords:
                    if coord[0] < minx: minx = coord[0]
                    if coord[0] > maxx: maxx = coord[0]
                    if coord[1] < miny: miny = coord[1]
                    if coord[1] > maxy: maxy = coord[1]

            elif self.geometry["type"] == "Polygon":
                for ring in coords:
                    for coord in ring:
                        if coord[0] < minx: minx = coord[0]
                        if coord[0] > maxx: maxx = coord[0]
                        if coord[1] < miny: miny = coord[1]
                        if coord[1] > maxy: maxy = coord[1]

            return (minx, miny, maxx, maxy)

        except Exception as e:
            raise Exception("Unable to determine bounding box for feature: %s. \nGeometry:\n %s" % (e, self.geometry))

    def to_dict(self):
        return {
            "id": self.id,
            "geometry": self.geometry,
            "geometry_attr": self.geometry_attr,
            "srs": self.srs,
            "properties": self.properties
        }
