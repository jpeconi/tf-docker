"""
Usage:
# Create train data:
python xml_to_csv.py -p project-name

"""

import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    """Iterates through all .xml files (generated by labelImg) in a given directory and combines them in a single Pandas datagrame.

    Parameters:
    ----------
    path : {str}
        The path containing the .xml files
    Returns
    -------
    Pandas DataFrame
        The produced dataframe
    """

    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                    int(root.find('size')[0].text),
                    int(root.find('size')[1].text),
                    member[0].text,
                    int(member[4][0].text),
                    int(member[4][1].text),
                    int(member[4][2].text),
                    int(member[4][3].text)
                    )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height',
                'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Sample TensorFlow XML-to-CSV converter")
    parser.add_argument("-p",
                        "--project",
                        help="project name",
                        type=str)
    args = parser.parse_args()

    project_dir = os.path.join("/tensorflow", "workspace", args.project)

    assert(os.path.isdir(project_dir))

    train_dir = os.path.join(project_dir, "images", "train")
    test_dir = os.path.join(project_dir, "images", "test")

    assert(os.path.isdir(train_dir))
    assert(os.path.isdir(test_dir))

    for i, d in enumerate([train_dir, test_dir]):
        xml_df = xml_to_csv(d)
        out = "train" if i == 0 else "test"
        xml_df.to_csv(
            os.path.join("/tensorflow", "workspace", args.project, "annotations", out + "_labels.csv"), index=None)
        print(f'Successfully converted {out}ing xml to csv.')


if __name__ == '__main__':
    main()