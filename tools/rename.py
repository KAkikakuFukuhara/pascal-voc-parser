import sys
import os
from typing import Dict, Any, List
from argparse import ArgumentParser
from pathlib import Path

import tqdm

import _add_path
from pascal_voc_parser import parser as voc_parser
from pascal_voc_parser.parser import ParsedPascalVOC

FILE_DIR = Path(os.path.abspath(__file__)).parent


def parse_args() -> Dict[str, Any]:
    argparser = ArgumentParser()
    argparser.add_argument("xml_dir", type=str, help="xml fir dir that have PascalVOC dataset")
    argparser.add_argument("-o", "--out_dir", type=str, default=f"{FILE_DIR}/new_xmls",
                           help="dir that save renamed xml")

    args:Dict[str, Any] = vars(argparser.parse_args())

    return args


def main(args):
    # check xml dir
    xml_dir = Path(args['xml_dir']).absolute()
    assert xml_dir.exists()

    # load datasets
    datasets:List[ParsedPascalVOC] = voc_parser.load_datasets(xml_dir)

    # make out dir
    out_dir = Path(args['out_dir']).absolute()
    out_dir.mkdir(parents=bool, exist_ok=True)

    # rename
    for i in tqdm.tqdm(range(len(datasets)), desc="save_new_xml"):
        renamed_file = Path(f"{out_dir}/{i:>05}.xml")
        datasets[i].save_new_xml(renamed_file)


if __name__ == "__main__":
    args = parse_args()
    main(args)
