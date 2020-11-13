# -*- coding: utf-8 -*-
import glob
import pathlib
import csv

filepaths = glob.glob("license_templete/*")
license_body_templete = {}
for filepath in filepaths:
    filename = pathlib.Path(filepath).name
    with open(filepath, 'r', encoding='utf-8') as f:
        license_body_templete[filename] = f.read()

# make section2, 3
with open('license_table.tsv', 'r', encoding='utf-8') as read_file, \
     open('2_third_party_list.txt', 'w', encoding='utf-8') as write_file2, \
     open('3_license_details.txt', 'w', encoding='utf-8') as write_file3:
    for index, cols in enumerate(csv.reader(read_file, delimiter='\t')):
        (name, version, license_key, since, owner, url) = tuple(cols)

        # section2
        write_file2.write('{index}.\t{name} {version} ({url})\n'.format(
            index=(index+1), name=name, version=version, url=url))

        # section3
        begin_templete = \
            '%% {name} NOTICES AND INFORMATION BEGIN HERE'.format(name=name)
        begin_templete += \
            '\n=========================================\n'
        
        body = license_body_templete[license_key].format(
            name=name, version=version, since=since, owner=owner)

        end_templete = \
            '========================================='
        end_templete += \
            '\nEND OF {name} NOTICES AND INFORMATION\n\n'.format(name=name)
        
        templete = begin_templete + body + end_templete
        write_file3.write(templete)
    write_file2.write('\n\n')

# merge section1-3
with open('../../ThirdPartyNotices.txt', 'w', encoding='utf-8') as write_file:
    with open('1_preface.txt', 'r', encoding='utf-8') as read_file:
        write_file.write(read_file.read())
    with open('2_third_party_list.txt', 'r', encoding='utf-8') as read_file:
        write_file.write(read_file.read())
    with open('3_license_details.txt', 'r', encoding='utf-8') as read_file:
        write_file.write(read_file.read())