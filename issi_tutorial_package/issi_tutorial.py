import tarfile
import os
import sys

def issi_tutorial(argv):
    input_files = []
    input_files_string = argv[1]
    input_dir = argv[2]
    output_location = argv[3]

    if ',' in input_files_string:
        input_files_string = "" + input_files_string + ""
        input_file_names = input_files_string.split(",")
        for file_name in input_file_names:
            input_files.append(input_dir + "/" + file_name)
    else:
        input_files.append(input_dir + "/" + input_files_string)

    for files in input_files:
        if (files.endswith("tar.gz")):
            tar = tarfile.open(files, "r:gz")
            tar.extractall(path=output_location)
            tar.close()

if __name__== "__main__":
    argv = sys.argv
    issi_tutorial(argv)

