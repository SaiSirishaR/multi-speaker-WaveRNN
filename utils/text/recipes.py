from utils.files import get_files
from pathlib import Path
from typing import Union


def ljspeech(path: Union[str, Path]):
    csv_file = get_files('../../../data/LJSpeech-1.1/', extension='.csv')
    print("csv file is", csv_file, "path is", path)
    assert len(csv_file) == 1

    text_dict = {}

    with open(csv_file[0], encoding='utf-8') as f :
        for line in f :
            split = line.split('|')
            print("split is", split[-1])
            text_dict[split[0]] = split[-1]
    print("dict is", text_dict)
    return text_dict


def arctic(text_path):

    text_dict = {}

    f = open(text_path)

    for line in f:
        split = line.split('/n')[0]
#        print("split0 is", split.split(' ')[0], "split 1 is", ' '.join(k for k in split.split()[1:]))
#        print("split is", split, "split 1 is", split[-1])
        text_dict[split.split(' ')[0]] = ' '.join(k for k in split.split()[1:])
    print("dict is", text_dict)
    return text_dict



