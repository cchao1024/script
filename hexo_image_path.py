#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

root_path = '/Users/cchao/github/hexo/source/_posts'


def rename(cur_root, item, old_str, new_str):
    abs_path = os.path.join(cur_root, item)
    print('文件名：' + abs_path)
    if os.path.splitext(item)[1] != '.md':
        return
    file_data = ""
    with open(abs_path, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(file_data)


for (root, dirs, files) in os.walk(root_path):
    for item_file in files:
        rename(root, item_file, '](../images/', '](../../images/')
