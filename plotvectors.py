# Required installs:
#   python3.5
#   python3-tk
#   matplotlib
import matplotlib.pyplot as plt
import sys
import argparse
import ast

# Creating the argument to grab the vector as a printed string from the script 
# call.
parser = argparse.ArgumentParser() 
parser.add_argument('-list_str', nargs='*', type=str)

# Grabing all arguments
args = parser.parse_args()

# Evaluating the list_str argument as literal
vectors = ast.literal_eval(args.list_str[0])
# print(vectors)

if len(vectors) == 1:
    plt.plot(vectors[0])
elif len(vectors) > 1:
    for i in range(1, len(vectors), 1):
        plt.plot(vectors[0],vectors[i])
plt.show()
