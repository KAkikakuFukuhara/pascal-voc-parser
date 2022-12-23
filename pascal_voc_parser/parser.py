from typing import Optional, List, Dict
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


    def parse_file(self, xml_path:Path) -> None:
        self.xml_file = xml_path

        with self.xml_file.open("r") as f:
            tree = et.parse(f)
        root = tree.getroot()

        self.img_name = Path(_parse_filename(root))
        self.name2size= _parse_imgsize(root)
        self.bboxes = _parse_bboxes(root)


def _parse_filename(root:et.ElementTree) -> Optional[str]:
    """ get filename from element tree
    """
    element = root.find("filename")
    return element.text if element is not None else None


def _parse_imgsize(root:et.ElementTree) -> Optional[Dict[str, int]]:
    node = root.find('size')
    if node is None:
        return None
    hsize = int(node.find('height').text)
    wsize = int(node.find('width').text)
    csize = int(node.find('depth').text)
    return {'hsize':hsize, 'wsize':wsize, 'csize':csize}


def _parse_bboxes(root:et.ElementTree) -> List[Bbox]:
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


def load_datasets(xml_dir:Path) -> List[ParsedPascalVOC]:
    _xml_dir = Path(xml_dir)
    xml_files = [Path(p) for p in glob.glob(f"{_xml_dir}/*.xml")]
    assert len(xml_files) > 0

    datasets:List[ParsedPascalVOC] = []
    for f in tqdm.tqdm(xml_files, desc="parsing xml"):
        dataset = ParsedPascalVOC()
        dataset.parse_file(f)
        datasets.append(dataset)

    return datasets
