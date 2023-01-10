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
        self.name2size:Dict[int]
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
        root.find("filename").text = str(self.img_name)
        root.find("size").find("height").text = str(self.name2size['hsize'])
        root.find("size").find("width").text = str(self.name2size['wsize'])
        root.find("size").find("depth").text = str(self.name2size['csize'])
        for i, obj in enumerate(root.iter("object")):
            obj.find("name").text = str(self.bboxes[i].name)
            obj.find("difficult").text = str(self.bboxes[i].difficult)
            xmlbox = obj.find("bndbox")
            xmlbox.find("xmin").text = str(int(self.bboxes[i].x1))
            xmlbox.find("ymin").text = str(int(self.bboxes[i].y1))
            xmlbox.find("xmax").text = str(int(self.bboxes[i].x2))
            xmlbox.find("ymax").text = str(int(self.bboxes[i].y2))

        tree.write(str(_path))


def _load_xml_as_elemtree(path:str) -> et.ElementTree:
    _path = Path(path)

    with _path.open("r") as f:
        tree = et.parse(f)
    return tree


def _parse_filename(root:et.Element) -> Optional[str]:
    """ get filename from element tree
    """
    element = root.find("filename")
    return element.text if element is not None else None


def _parse_imgsize(root:et.Element) -> Optional[Dict[str, int]]:
    node = root.find('size')
    if node is None:
        return None
    hsize = int(node.find('height').text)
    wsize = int(node.find('width').text)
    csize = int(node.find('depth').text)
    return {'hsize':hsize, 'wsize':wsize, 'csize':csize}


def _parse_bboxes(root:et.Element) -> List[Bbox]:
    """ get bboxes from result that parse xml
    """
    bboxes :List[Bbox]= []

    for obj in root.iter("object"):
        xmlbox = obj.find("bndbox")
        bbox = Bbox()
        bbox.name = obj.find("name").text
        bbox.difficult = obj.find("difficult").text
        bbox.x1 = float(xmlbox.find("xmin").text)
        bbox.y1 = float(xmlbox.find("ymin").text)
        bbox.x2 = float(xmlbox.find("xmax").text)
        bbox.y2 = float(xmlbox.find("ymax").text)

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
