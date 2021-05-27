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
# Required modules:
#   matplotlib

import matplotlib.pyplot as plt
import argparse
import os
import re
import sys

from common import is_number, is_index

parser = argparse.ArgumentParser()
parser.add_argument('--file', nargs='*', type=str)

# Grabing all arguments
args = parser.parse_args()

# Evaluating the list_str argument as literal
filename = args.file[0]

vectors = []
with open(filename) as file:
    for line in file:
        numbers_in_line = []
        if line:
            words_in_line = re.split("[, !?:;$#]+", line)
            for word in words_in_line:
                if is_number(word):
                    numbers_in_line = numbers_in_line + [float(word)]
            if numbers_in_line:
                for i in range(0,len(numbers_in_line),1):
                    if not is_index(vectors, i):
                        vectors.append([])
                    vectors[i].append(numbers_in_line[i])

os.remove(filename)

if len(vectors) == 1:
    plt.plot(vectors[0])
    plt.show()
elif len(vectors) > 1:
    for i in range(1, len(vectors), 1):
        plt.plot(vectors[0],vectors[i])
    plt.show()
