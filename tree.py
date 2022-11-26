#!/usr/bin/python

import os
import sys
import argparse
from functools import partial
import re


class Tree:
    def __init__(self):
        self.dirCount = 0
        self.fileCount = 0

    @staticmethod
    def get_folder_size(start_path='.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size

    @staticmethod
    def remove_char(file, index):
        with open(file, 'r') as f:
            data = f.read()
        with open(file, 'w') as f:
            f.write(data[:index] + data[index + 1:])
        # print("Char removed : ", data[index])

    def register(self, absolute):
        if os.path.isdir(absolute):
            self.dirCount += 1
        else:
            self.fileCount += 1

    def summary(self):
        return str(self.dirCount) + " directories, " + str(self.fileCount) + " files"

    def walk(self, directory, key=lambda x: x.lower(), prefix="", max_depth=0, exclude=None, depth=0, separate=False,
             show_hidden=False, reverse=False, emotes=False, no_develop=None):

        if depth > max_depth:
            return

        # Indicate if the files must be separated from the directories
        if separate is False:
            filepaths = sorted([filepath for filepath in os.listdir(directory)], key=partial(key, directory), reverse=reverse)
        else:
            files = sorted([filepath for filepath in os.listdir(directory) if os.path.isfile(os.path.join(directory, filepath))],
                           key=partial(key, directory), reverse=reverse)
            folders = sorted([filepath for filepath in os.listdir(directory) if os.path.isdir(os.path.join(directory, filepath))],
                             key=partial(key, directory), reverse=reverse)
            filepaths = files + folders

        # hidden files
        if show_hidden is False:
            filepaths = [filepath for filepath in filepaths if filepath[0] != "."]

        # exclude files with regex
        if exclude is not None:
            filepaths = [filepath for filepath in filepaths if not re.match("(\./)?" + exclude, os.path.join(directory, filepath))]

        for index in range(len(filepaths)):
            absolute = os.path.join(directory, filepaths[index])
            self.register(absolute)

            if index == len(filepaths) - 1:

                if os.path.isdir(absolute):
                    print(f"\n{prefix}└── {'📁 ' * emotes}[{filepaths[index]}]({absolute})", "\\", end="")
                    if no_develop is not None and re.match("(\./)?" + no_develop, absolute):
                        print(prefix + "&nbsp;" * 12 + "└── ..." + "\\")
                    else:
                        self.walk(absolute, key=key, prefix=prefix + "&nbsp;" * 12, depth=depth+1, max_depth=max_depth,
                                  exclude=exclude, separate=separate, show_hidden=show_hidden, reverse=reverse,
                                  emotes=emotes, no_develop=no_develop)
                else:
                    print(f"\n{prefix}└── {'📄 ' * emotes}[{filepaths[index]}]({absolute})", "\\", end="")

            else:
                if os.path.isdir(absolute):
                    print(f"\n{prefix}├── {'📁 ' * emotes}[{filepaths[index]}]({absolute})", "\\", end="")
                    if no_develop is not None and re.match("(\./)?" + no_develop, absolute):
                        print(prefix + "│" + "&nbsp;" * 8 + "└── ..." + "\\")
                    else:
                        self.walk(absolute, key=key, prefix=prefix + "│" + "&nbsp;" * 8, depth=depth+1, max_depth=max_depth,
                                  exclude=exclude, separate=separate, show_hidden=show_hidden, reverse=reverse,
                                  emotes=emotes, no_develop=no_develop)
                else:
                    print(f"\n{prefix}├── {'📄 ' * emotes}[{filepaths[index]}]({absolute})", "\\", end="")

    def display(self, directory=".", file=None, max_depth=0, exclude=None, order="default", separate=False,
                show_hidden=False, reverse=False, emotes=False, summary=False, display_from_directory=False,
                no_develop=None):

        # Criteria for sorting
        if order == "time":
            def key(folder, filepath):
                return os.path.getmtime(os.path.join(folder, filepath))

        elif order == "size":
            def key(folder, filepath):
                file = os.path.join(folder, filepath)
                if os.path.isfile(file):
                    return os.path.getsize(file)

                # os.path.getsize does not work on directories
                # it returns the size of the file that describes the directory
                elif os.path.isdir(file):
                    return self.get_folder_size(file)
                else:
                    return 0

        else:  # order == "default"
            def key(folder, filepath):
                return filepath.lower()

        if file is not None:
            original = sys.stdout
            current_directory = os.getcwd()
            with open(file, "w") as f:
                sys.stdout = f
                if display_from_directory is True:
                    os.chdir(directory)
                    directory = "."
                print(directory, "\\", end="")
                self.walk(directory, key=key, max_depth=max_depth, exclude=exclude, separate=separate,
                          show_hidden=show_hidden, reverse=reverse, emotes=emotes, no_develop=no_develop)
                os.chdir(current_directory)
                print()
                if summary:
                    print(self.summary())
            sys.stdout = original

            # Remove the last "\"
            index = -2 - (len(self.summary()) + 1) * summary
            self.remove_char(file, index)

        else:
            current_directory = os.getcwd()
            if display_from_directory is True:
                os.chdir(directory)
                directory = "."
            print(directory, "\\", end="")
            self.walk(directory, key=key, max_depth=max_depth, exclude=exclude, separate=separate,
                      show_hidden=show_hidden, reverse=reverse, emotes=emotes, no_develop=no_develop)
            os.chdir(current_directory)

            # Remove the last "\"
            print("\b ")

            if summary:
                print(self.summary())


def main():
    parser = argparse.ArgumentParser(description='Markdown tree')
    parser.add_argument('-D', '--directory', type=str, default='.', help='Directory to display, default is current directory')
    parser.add_argument('-f', '--file', type=str, help='File to write the tree, default is stdout')
    parser.add_argument('-d', '--max-depth', type=int, default=5, help='Maximum depth of the tree, default is 5')
    parser.add_argument('-e', '--exclude', type=str, default=None, help='Exclude files matching the pattern')
    parser.add_argument('-o', '--order', type=str, default="default", help='Criteria for sorting, can be "default", "time" or "size", default is "default"')
    parser.add_argument('-s', '--separate', action='store_true', help='Separate files from directories')
    parser.add_argument('-H', '--show-hidden', action='store_true', help='Show hidden files')
    parser.add_argument('-r', '--reverse', action='store_true', help='Reverse the order of the files')
    parser.add_argument('-E', '--emotes', action='store_true', help='Use emotes')
    parser.add_argument('-S', '--summary', action='store_true', help='Display a summary of the tree')
    parser.add_argument('-F', '--display-from-directory', action='store_true', help='Display the tree from the directory (the directory you specified will be treated as ".")')
    parser.add_argument('-N', '--no-develop', type=str, default=None, help='Do not display the files in the directory matching the pattern, display "..." instead')
    args = parser.parse_args()

    tree = Tree()
    tree.display(args.directory, args.file, args.max_depth, args.exclude, args.order, args.separate, args.show_hidden,
                 args.reverse, args.emotes, args.summary, args.display_from_directory, args.no_develop)


if __name__ == "__main__":
    main()

