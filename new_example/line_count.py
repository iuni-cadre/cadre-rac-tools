import os
import sys
_input_filenames = []
_input_dir = '.'
_output_dir = '.'


def count_lines(filename):
    """
    opens a file and counts the lines
    """
    try:
        full_path = '{0}/{1}'.format(_input_dir, filename)
        count = len(open(full_path, 'rb').readlines())
    except FileNotFoundError:
        print( "Error: Could not find file {0}".format(full_path))
        return 0
    return count


def write_file(filename, content):
    """
    Writes a file to the output directory
    """
    write_file = open('{0}/count_{1}'.format(_output_dir, filename), 'w')
    write_file.write(content)
    write_file.close()
    return None
        



if __name__ == "__main__":
    """
    How to run script:
        copy example files to input directory
        run with python line_count.py example1.csv,example2.csv /efs/input /efs/output

    What it does:
        gets the list of filenames from the commandline
        counts the lines from each file in /efs/input (which will be available within docker)
    """

    #Required cadre boilerplate to get commandline arguments:
    try:
        _input_filenames = sys.argv[1].split(',')
        _input_dir = sys.argv[2]
        _output_dir = sys.argv[3]
    except IndexError:
        print("Missing Parameter")
        sys.exit(1)
    except:
        print("Unknown Error")
        sys.exit(1)

    total_line_count = 0

    for filename in _input_filenames:
        count = count_lines(filename)
        total_line_count += count
        write_file(filename, "Line Count: {0}\n".format(str(count)))
        print("{0} - {1}".format(filename, count))

    write_file('total_lines.txt', "Grand Total Count: {0}\n".format(str(total_line_count)))
    print("Contents of output directory: " + str(os.listdir(_output_dir)))
