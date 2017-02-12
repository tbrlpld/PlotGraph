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

# print(details.split(","))


# vectors = details.split("[]")
# print(vectors)

# print(sys.argv)
# vectors = sys.argv[1]
# print(vectors)
# print("vectors = {0}".format(vectors))
# plt.plot([1,2,3,4,3,4])
# plt.show() 
