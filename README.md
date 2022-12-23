# README

![](https://img.shields.io/badge/python-3.7|3.8|3.9-blue.svg)


## tag status

|    tag    | valid |
| --------- | ----- |
| folder    | [ ]   |
| filename  | [x]   |
| source    | [ ]   |
| owner     | [ ]   |
| size      | [x]   |
| segmented | [ ]   |
| object    | [x]   |

- object

|    tag    | valid |
| --------- | ----- |
| name      | [x]   |
| pose      | [ ]   |
| truncated | [ ]   |
| occluded  | [ ]   |
| difficult | [x]   |
| bndbox    | [x]   |
| part      | [ ]   |
| actions   | [ ]   |
| point     | [ ]   |

- ref
  - https://mikebird28.hatenablog.jp/entry/2020/11/25/234837

## install

```bash
pip install git+ssh://git@github.com:KAkikakuFukuhara/pascal-voc-parser.git
```

## usage

```python
from pascal_voc_parser import parser as pvparser

xml_dir = "Hoge"
datasets = pvparser.load_datasets(xml_dir)
```

- example
tools/parse_example

