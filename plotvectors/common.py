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

import re

# http://stackoverflow.com/questions/354038/ \
# how-do-i-check-if-a-string-is-a-number-float-in-python

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_index(l, index):
    try:
        l[index]
        return True
    except IndexError:
        return False

def extract_numbers(line_iter):
    vectors = []
    for line in line_iter:
        numbers_in_line = []
        # Only keeping lines that are not empty.
        if line:
            # Split the line into "words".
            # http://stackoverflow.com/a/23720594/6771403
            words_in_line = re.split("[, !?:;$#]+", line)
            # Collect the words which are numbers in the numbers_in_line variable
            for word in words_in_line:
                if is_number(word):
                    numbers_in_line = numbers_in_line + \
                                        [float(word)]

            if numbers_in_line:
                # Take the i-th number in the line and put it into
                # the i-th vector/list in vectors.
                # If there is no i-th vector yet, create it before.
                for i in range(0,len(numbers_in_line),1):
                    if not is_index(vectors, i):
                        vectors.append([])
                    vectors[i].append(numbers_in_line[i])

    return vectors
