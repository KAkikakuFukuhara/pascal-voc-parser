from typing import Optional, Union, List
from pathlib import Path
import xml.etree.ElementTree as et


def parse_xml(path):
    with path.open("r") as f:
        etree:et.ElementTree = et.parse(f)

    str2data = {}
    root = etree.getroot()
    str2data['objects'] = []
    for ch in list(root):
        if ch.tag == "object":
            str2data['objects'].append(_parse_elem(ch)['object'])
        else:
            str2data.update(_parse_elem(ch))
    return str2data


def _parse_elem(elem:et.Element):
    childs = list(elem)
    if len(childs) == 0:
        dict_ = {elem.tag:elem.text}
        if elem.text is not None:
            try:
                dict_[elem.tag] = int(elem.text) # type:ignore
            except:
                try:
                    dict_[elem.tag] = float(elem.text) # type:ignore
                except:
                    pass
    else:
        dict_ = {elem.tag:{}}
        for ch in childs:
            dict_[elem.tag].update(_parse_elem(ch))
    return dict_


def save_to_xml(dict_:dict, out:Path):
    etree = et.ElementTree(et.Element('annotation'))
    # etree._setroot(et.Element("annotation"))
    root = etree.getroot()
    keys = ['folder', 'filename', 'path', 'source', 'size', 'segmented']
    for k in keys:
        if k not in dict_.keys():
            continue
        root.append(_to_elem(k, dict_[k]))
    for obj_ in dict_['objects']:
        root.append(_to_elem('object', obj_))
    etree.write(str(out))


def _to_elem(tag:str, data:Union[dict, int, str, float]):
    elem = et.Element(tag)
    if type(data) != dict:
        elem.text = str(data)
    else:
        for k, v in data.items():
            elem.append(_to_elem(k, v))
    return elem
