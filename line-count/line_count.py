import os
import sys


def line_count(argv):
    input_files = []
    output_file = []
    input_file_string = argv[3]
    output_files_string = argv[4]
    output_location = argv[5]
    if ',' in input_file_string:
        input_file_string = "" + input_file_string + ""
        input_files = input_file_string.split(",")
    else:
        input_files.append(input_file_string)
    if ',' in output_files_string:
        output_files_string = "" + output_files_string + ""
        output_file = output_files_string.split(',')
    else:
        output_file.append(output_files_string)
    output_count = 0
    for files in input_files:
        count = len(open(files, 'rb').readlines())
        output_file_name = output_location + '/' + output_file[output_count]
        file = open(output_file_name, 'w')
        file.write("Number of lines in the file: " + str(count))
        file.close()
        output_count += 1


if __name__ == "__main__":
    argv = sys.argv
    line_count(argv)
