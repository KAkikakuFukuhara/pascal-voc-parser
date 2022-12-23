from typing import Dict, List
from argparse import ArgumentParser
from pathlib import Path

import _add_path
from pascal_voc_parser import parser
from pascal_voc_parser.parser import ParsedPascalVOC

if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("xml_dir", type=str, help="xml file dir that have PascalVOC dataset")

    args:Dict[str, str] = vars(argparser.parse_args())

    assert args['xml_dir'] is not None
    xml_dir = Path(args['xml_dir']).absolute()
    assert xml_dir.exists()

    datasets:List[ParsedPascalVOC] = parser.load_datasets(xml_dir)
    dataset = datasets[0]

    # show xml_file path
    print(dataset.xml_file)
    # show img name
    print(dataset.img_name)
    # show img size
    print(f"img hsize:{dataset.name2size['hsize']}")
    print(f"img wsize:{dataset.name2size['wsize']}")
    print(f"img csize:{dataset.name2size['csize']}")
    # show bboxes
    print(f"num bboxes in dataset:{len(dataset.bboxes)}")
    # show bbox
    bbox = dataset.bboxes[0]
    print(f"name:{bbox.name}")
    print(f"difficult:{bbox.difficult}")
    print(f"(x1, y1):{bbox.x1},{bbox.y1}")
    print(f"(x2, y2):{bbox.x2},{bbox.y2}")
    print(f"(cx, cy):{bbox.cx},{bbox.cy}")
    print(f"(w, h):{bbox.w},{bbox.h}")
