import sys
import os
from typing import Dict, Any, List
from pathlib import Path
from argparse import ArgumentParser

import tqdm

import _add_path
from pascal_voc_parser import parser as voc_parser
from pascal_voc_parser.parser import ParsedPascalVOC

FILE_DIR = Path(os.path.abspath(__file__)).parent.absolute()


def parse_args() -> Dict[str, Any]:
    argparser = ArgumentParser()
    argparser.add_argument("xml_dir", type=str, help="dir that have PascalVOC dataset")
    argparser.add_argument("-o", "--out_dir", type=str, default=f"{FILE_DIR}/new_xmls",
                            help="dir that save new xml")

    args:Dict[str, Any] = vars(argparser.parse_args())

    return args


def main(args:Dict[str, Any]):
    # check xml dir
    xml_dir = Path(args['xml_dir']).absolute()
    assert xml_dir.exists()

    # parse pascal voc
    datasets:List[ParsedPascalVOC] = voc_parser.load_datasets(xml_dir)
    assert len(datasets) > 0

    # resize
    ratio = 0.5
    for di in tqdm.tqdm(range(len(datasets)), desc="Resize"):
        datasets[di].name2size['wsize'] = round(datasets[di].name2size['wsize'] * ratio)
        datasets[di].name2size['hsize'] = round(datasets[di].name2size['hsize'] * ratio)
        for bj in range(len(datasets[di].bboxes)):
            datasets[di].bboxes[bj].x1 = round(datasets[di].bboxes[bj].x1 * ratio)
            datasets[di].bboxes[bj].y1 = round(datasets[di].bboxes[bj].y1 * ratio)
            datasets[di].bboxes[bj].x2 = round(datasets[di].bboxes[bj].x2 * ratio)
            datasets[di].bboxes[bj].y2 = round(datasets[di].bboxes[bj].y2 * ratio)

    # mkdir
    out_dir = Path(args['out_dir']).absolute()
    out_dir.mkdir(parents=True, exist_ok=True)
    # save
    for dataset in tqdm.tqdm(datasets, desc="Save"):
        new_file = f"{out_dir}/{dataset.xml_file.name}"
        dataset.save_new_xml(new_file)


if __name__ == "__main__":
    args = parse_args()
    main(args)