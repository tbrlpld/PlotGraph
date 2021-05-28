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
import argparse
import ast
import os

# Required non-standard modules:
import matplotlib.pyplot as plt

from common import extract_numbers

def show_error_message(message):
    ax = plt.axes()
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
    # check vector format
    column_length_issue = False
    first_length = len(vectors[0])
    for i in range(1, len(vectors), 1):
        if len(vectors[i]) != first_length:
            column_length_issue = True
            break
    if column_length_issue:
        show_error_message("selected columns have different numbers of rows")
    elif first_length == 1:
        show_error_message("need at least two rows of numbers to draw a graph")
    else:
        # vector format is OK
        for i in range(1, len(vectors), 1):
            plt.plot(vectors[0],vectors[i])
else:
    show_error_message("no numbers in selection")

plt.show()
