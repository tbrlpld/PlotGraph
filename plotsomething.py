# Required installs:
#   python3.5
#   python3-tk
#   matplotlib
print("This is plotsomething.py")
import matplotlib.pyplot as plt
import sys
import argparse
import ast

parser = argparse.ArgumentParser() 
parser.add_argument('-list_str', nargs='*', type=str)

args = parser.parse_args()
vectors = ast.literal_eval(args.list_str[0])
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
