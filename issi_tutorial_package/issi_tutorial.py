import tarfile
import os
import sys

def issi_tutorial(argv):
    input_files = []
    output_files = []
    input_files_string = argv[3]
    output_files_string = argv[4]
    output_location = argv[5]

    if ',' in input_files_string:
        input_files_string = "" + input_files_string + ""
        input_files = input_files_string.split(",")
    else:
        input_files.append(input_files_string)

    for files in input_files:
        if (files.endswith("tar.gz")):
            tar = tarfile.open(files, "r:gz")
            tar.extractall(path=output_location)
            tar.close()

if __name__== "__main__":
    argv = sys.argv
    issi_tutorial(argv)

