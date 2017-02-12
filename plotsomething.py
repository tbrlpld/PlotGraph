# Required installs:
#   python3.5
#   python3-tk
#   matplotlib
print("This is plotsomething.py")
import matplotlib.pyplot as plt
import sys
import argparse

# Creating the argument to grab the vector as a printed string from the script 
# call.
parser = argparse.ArgumentParser() 
parser.add_argument('-list_str', nargs='*', type=str)

# Grabing all arguments
args = parser.parse_args()

# Evaluating the list_str argument as literal
vectors = eval(args.list_str[0])
print(vectors)

if vectors:
    plt.plot(vectors[:])
    plt.show() 
