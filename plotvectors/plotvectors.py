# PlotGraph - Package for Sublime Text 3 to plot selected number colums as graph.
# Copyright (C) 2017-2020 Tibor Leupold
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys

try:
    import ast
    import argparse
except ImportError:
    print("python path: {0}".format(sys.executable if sys.executable != None else "not available"))
    print("python version: {0}".format(sys.version))
    print()
    print("PlotGraph requires the modules argparse and ast, which are missing.")
    print("Please update to a newer python version (2.7/3.2 or better).")
    exit(1)

try:
    import matplotlib.pyplot as plt
except ImportError as error:
    print("python path: {0}".format(sys.executable if sys.executable != None else "not available"))
    print("python version: {0}".format(sys.version))
    print()
    print("{0}: {1}".format(error.__class__.__name__, error))
    print()
    print("PlotGraph requires matplotlib to be installed.")
    print("To install:")
    print("  python -m pip install -U pip")
    print("  python -m pip install -U matplotlib")
    exit(1)

from common import extract_numbers

def show_error_message(message):
    ax = plt.gca()
    ax.text(0.5, 0.5, message,
            ha="center", va="center",
            transform=ax.transAxes,
            wrap=True)

# Arguments
# --list_str to grab the vector as a printed string
#            from the script call, or
# --file to read the selection from a file

parser = argparse.ArgumentParser()
parser.add_argument('--list_str', nargs='*', type=str)
parser.add_argument('--file', nargs='*', type=str)

# Grabbing all arguments
args = parser.parse_args()

if args.file:
    filename = args.file[0]
    vectors = []
    with open(filename) as file:
        vectors = extract_numbers(file)
    os.remove(filename)

else:
    vectors = ast.literal_eval(args.list_str[0])

if len(vectors) == 1:
    if len(vectors[0]) == 1:
        show_error_message("cannot draw a diagram from a single number")
    else:
        plt.plot(vectors[0])

elif len(vectors) > 1:
    vector_x = vectors[0]
    vectors_y = vectors[1:]

    # check vector format
    column_length_issue = False
    for vector_y in vectors_y:
        if len(vector_y) != len(vector_x):
            column_length_issue = True
            break
    if column_length_issue:
        show_error_message("selected columns have different numbers of rows")
    elif len(vector_x) == 1:
        show_error_message("need at least two rows of numbers to draw a graph")
    else:
        # vector format is OK
        for i, vector_y in enumerate(vectors_y):
            plt.plot(vector_x, vector_y, label=str(i+1))

        # after ten plots colors are repeating, so it makes no sense to label them
        plot_count = len(vectors_y)
        if plot_count <= 10:
            plt.gca().legend(bbox_to_anchor=(0., 1.05, 1., .1),
                              loc='lower left',
                              handlelength=1.0,
                              borderaxespad=0.2,
                              borderpad=0.2,
                              mode = "expand" if plot_count > 7 else None,
                              ncol=len(vectors_y))
            #plt.gca().legend(bbox_to_anchor=(1.0, 1.0),
            #                  loc='upper left',
            #                  handlelength=0.5,
            #                  borderaxespad=0.2,
            #                  borderpad=0.2)
else:
    show_error_message("no numbers in selection")

plt.show()
