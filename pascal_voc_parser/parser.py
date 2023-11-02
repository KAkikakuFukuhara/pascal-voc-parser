from typing import Optional, List, Dict, Union
from pathlib import Path
import glob
import xml.etree.ElementTree as et

import tqdm

class Bbox:
    def __init__(self):
        self.name:str
        self.difficult:str
        self.x1:float
        self.x2:float
        self.y1:float
        self.y2:float


    def __str__(self) -> str:
        text = f"Bbox({self.name})"
        return text


    @property
    def cx(self) -> float:
        return (self.x2 + self.x1) / 2


    @property
    def cy(self) -> float:
        return (self.y2 + self.y1) / 2


    @property
    def w(self) -> float:
        return self.x2 - self.x1


    @property
    def h(self) -> float:
        return self.y2 - self.y1


class ParsedPascalVOC:
    def __init__(self):
        self.xml_file:Path
        self.img_name:Path
        self.name2size:Dict[str, int]
        self.bboxes:List[Bbox]


    def parse_file(self, xml_path:Union[str, Path]) -> None:
        _xml_path = Path(xml_path)
        self.xml_file = _xml_path

        tree:et.ElementTree = _load_xml_as_elemtree(self.xml_file)
        root:et.Element = tree.getroot()

        self.img_name = Path(_parse_filename(root))
        self.name2size= _parse_imgsize(root)
        self.bboxes = _parse_bboxes(root)


    def save_new_xml(self, path:str):
        _path = Path(path)

        assert _path.suffix == ".xml", "[Error] New file name suffix only '.xml'"
        assert _path != self.xml_file , "[Error] Writing to the same file is prohibited"

        is_equal_name = self.xml_file.name == _path.name
        if not is_equal_name:
            self.img_name = Path(f"{_path.stem}{self.img_name.suffix}")

        tree:et.ElementTree = _load_xml_as_elemtree(self.xml_file)
        root:et.Element = tree.getroot()

        # write new value
        root.find("filename").text = str(self.img_name) # type:ignore
        root.find("size").find("height").text = str(self.name2size['hsize']) # type:ignore
        root.find("size").find("width").text = str(self.name2size['wsize']) # type:ignore
        root.find("size").find("depth").text = str(self.name2size['csize']) # type:ignore
        for i, obj in enumerate(root.iter("object")):
            obj.find("name").text = str(self.bboxes[i].name) # type:ignore
            obj.find("difficult").text = str(self.bboxes[i].difficult) # type:ignore
            xmlbox = obj.find("bndbox")
            xmlbox.find("xmin").text = str(int(self.bboxes[i].x1)) # type:ignore
            xmlbox.find("ymin").text = str(int(self.bboxes[i].y1)) # type:ignore
            xmlbox.find("xmax").text = str(int(self.bboxes[i].x2)) # type:ignore
            xmlbox.find("ymax").text = str(int(self.bboxes[i].y2)) # type:ignore

        tree.write(str(_path))


def _load_xml_as_elemtree(path:Path) -> et.ElementTree:
    _path = Path(path)

    with _path.open("r") as f:
        tree = et.parse(f)
    return tree


def _parse_filename(root:et.Element) -> str:
    """ get filename from element tree
    """
    element = root.find("filename")
    return str(element.text) if element is not None else ""


def _parse_imgsize(root:et.Element) -> Dict[str, int]:
    node = root.find('size')
    if node is None:
        return {}
    hsize = int(node.find('height').text) # type:ignore
    wsize = int(node.find('width').text) # type:ignore
    csize = int(node.find('depth').text) # type:ignore
    return {'hsize':hsize, 'wsize':wsize, 'csize':csize}


def _parse_bboxes(root:et.Element) -> List[Bbox]:
    """ get bboxes from result that parse xml
    """
    bboxes :List[Bbox]= []

    for obj in root.iter("object"):
        xmlbox = obj.find("bndbox")
        bbox = Bbox()
        bbox.name = obj.find("name").text # type:ignore
        bbox.difficult = obj.find("difficult").text # type:ignore
        bbox.x1 = float(xmlbox.find("xmin").text) # type:ignore
        bbox.y1 = float(xmlbox.find("ymin").text) # type:ignore
        bbox.x2 = float(xmlbox.find("xmax").text) # type:ignore
        bbox.y2 = float(xmlbox.find("ymax").text) # type:ignore

        bboxes.append(bbox)

    return bboxes


def load_datasets(xml_dir:Union[str, Path]) -> List[ParsedPascalVOC]:
    _xml_dir = Path(xml_dir)
    xml_files = [Path(p) for p in glob.glob(f"{_xml_dir}/*.xml")]
    assert len(xml_files) > 0

    datasets:List[ParsedPascalVOC] = []
    for f in tqdm.tqdm(xml_files, desc="parsing xml"):
        dataset = ParsedPascalVOC()
        dataset.parse_file(f)
        datasets.append(dataset)

    return datasets
