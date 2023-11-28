from pathlib import Path
from xml.etree import ElementTree as et


class Annotation:
    @classmethod
    def parse_xml(cls, path:Path):
        tree = parse_xml(path)
        root = tree.getroot()
        return cls(
            get_text(root, "folder"),
            get_text(root, "filename"),
            get_text(root,"path"),
            get_sources(root),
            get_size(root),
            int(get_text(root, "segmented")),
            get_objects(root)
        )


    def __init__(self,
            folder:str,
            filename:str,
            path:str,
            sources:dict,
            size:"Size",
            segmented:int,
            objects:list):
        self.folder:str
        self.filename:str
        self.path:str
        self.sources:dict
        self.size:Size
        self.segmented:int
        self.objects:list


class Size:
    def __init__(self, width:int, height:int, depth:int):
        self.width = width
        self.height = height
        self.depth = depth


class Object_:
    def __init__(self):
        self.name:str
        self.pose:str
        self.truncated:int
        self.difficult:int
        self.bndbox:Bbox


class Bbox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin:float
        self.ymin:float
        self.xmax:float
        self.ymax:float


    @property
    def x1(self):
        return self.xmin


    @property
    def x2(self):
        return self.xmax


    @property
    def y1(self):
        return self.ymin


    @property
    def y2(self):
        return self.ymax


    @property
    def w(self):
        return self.xmax - self.xmin


    @property
    def h(self):
        return self.ymax - self.ymin


    @property
    def cx(self):
        return (self.xmax + self.xmin) / 2


    @property
    def cy(self):
        return (self.ymax + self.ymin) / 2


def parse_xml(xml_path:Path) -> et.ElementTree:
    with xml_path.open("r") as f:
        tree:et.ElementTree = et.parse(f)
    return tree


def get_text(root:et.Element, key:str) -> str:
    elem = root.find(key)
    assert elem is not None
    assert elem.text is not None
    return elem.text


def get_sources(root:et.Element):
    elem = root.find("sources")
    assert elem is not None
    assert elem.text is not None
    childs = list(elem)
    if len(childs) == 0:
        