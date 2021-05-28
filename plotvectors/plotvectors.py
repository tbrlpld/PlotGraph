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

# Creating the argument to grab the vector as a printed string from the script
# call.
parser = argparse.ArgumentParser()
parser.add_argument('--list_str', nargs='*', type=str)
parser.add_argument('--file', nargs='*', type=str)

# Grabing all arguments
args = parser.parse_args()

if args.file:
    filename = args.file[0]
    vectors = []
    with open(filename) as file:
        vectors = extract_numbers(file)
    os.remove(filename)

else:
    # Evaluating the list_str argument as literal
    vectors = ast.literal_eval(args.list_str[0])

# print(vectors)

if len(vectors) == 1:
    plt.plot(vectors[0])
elif len(vectors) > 1:
    for i in range(1, len(vectors), 1):
        plt.plot(vectors[0],vectors[i])
plt.show()
