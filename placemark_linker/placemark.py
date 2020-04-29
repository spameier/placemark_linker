"""module containing the Placemark class"""
import re

from lxml import etree
from shapely.geometry import Point, Polygon, MultiPolygon


class Placemark:
    """A represenation of a placemark in a kml file.

        Args:
            name = The name of this placemark
            geometry = The geometry(coordinates) of this placemark
            data = Additional data contained in the placemark
    """

    def __init__(self, name, geometry, data=None):
        self.name = name
        self.geometry = geometry
        self.data = data
        self.links = {}

    @staticmethod
    def _find(xml, string):
        """find an element inside a xml element."""
        return xml.find(string, xml.nsmap)

    @staticmethod
    def _findall(xml, string):
        """find all elements inside a xml element."""
        return xml.findall(string, xml.nsmap)

    @staticmethod
    def generate_tuple(coordinates):
        """Transform a string in form 'x,y,z' to a tuple in form (x,y,z) or a
        string in form 'x,y,z x,y,z ...' to a list of tuples in form
        [(x,y,z), (x,y,z), ...].
        """
        # remove unwanted tabs and newlines and replace them with spaces
        coordinates = re.sub(r"[^\S]+", " ", coordinates.strip())
        if not " " in coordinates:
            # if the string contains no space, treat it as a comma separated list
            # and return one tuple
            return tuple([float(x) for x in coordinates.split(",")])
        # if the string contains a space, treat it as a space separated list
        # and return a list of tuples
        return [Placemark.generate_tuple(x) for x in coordinates.split(" ")]

    @staticmethod
    def get_name_from_xml(xml):
        """Extract the text of the name tag from placemark in xml."""
        return Placemark._find(xml, "./name").text

    @staticmethod
    def get_geometry_from_xml(xml):
        """Extract geometry from placemark in xml. Only MultiPolygons and Points are supported."""
        geometry = None
        if Placemark._find(xml, ".//MultiGeometry") is not None:
            # a <MultiGeometry> contains many <coordinates> tags
            coordinates = Placemark._findall(xml, ".//coordinates")
            # create a Polygon from each <coordinates> tag
            polygons = [Polygon(Placemark.generate_tuple(c.text)) for c in coordinates]
            # create a MultiPolygon from all the Polygons
            geometry = MultiPolygon(polygons)
        elif Placemark._find(xml, ".//Point") is not None:
            # a <Point> contains one <coordinates> tag
            coordinates = Placemark._find(xml, ".//coordinates").text
            # some <coordinates> tags where empty in the kml files
            if coordinates is None:
                return None
            # create a Point from the coordinates
            geometry = Point(Placemark.generate_tuple(coordinates))
        return geometry

    @staticmethod
    def get_data_from_xml(xml):
        """Extract additional data from the "ExtendedData" tag in xml"""
        schema_data = Placemark._find(xml, "./ExtendedData/SchemaData")
        if schema_data is None:
            return None
        # example:
        # <SchemaData schemaUrl="#Communes">
        #   <SimpleData name="COM_PCODE">MDG11101001</SimpleData>
        #   ...
        # get name attribute of each entry (COM_PCODE in example)
        keys = [x.attrib["name"] for x in schema_data]
        # get text of each entry (MDG11101001 in example)
        values = [x.text for x in schema_data]
        return dict(zip(keys, values))

    @classmethod
    def from_xml(cls, placemark_xml):
        """Create a new Placemark object from an existing xml element"""
        name = cls.get_name_from_xml(placemark_xml)
        geometry = cls.get_geometry_from_xml(placemark_xml)
        data = cls.get_data_from_xml(placemark_xml)
        return cls(name, geometry, data=data)

    @classmethod
    def from_kml(cls, kml_file):
        """Create new Placemark objects from a kml file"""
        root = etree.parse(kml_file).getroot()
        # return a list of placemarks
        return [cls.from_xml(p) for p in Placemark._findall(root, ".//Placemark")]

    def contains(self, other_placemark):
        """Check if this placemark contains another placemark"""
        if self.geometry is None or other_placemark.geometry is None:
            return False
        return self.geometry.contains(other_placemark.geometry)

    def is_inside(self, other_placemark):
        """Check if this placemark is inside another placemark"""
        return other_placemark.contains(self)
