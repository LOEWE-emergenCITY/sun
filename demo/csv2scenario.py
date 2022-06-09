#!/usr/bin/python3

# load the csv file
import csv
import sys
import re
# argv 1 is the csv file
# argv 2 is the output file
scenario = open(sys.argv[2], 'r').readlines()

bbox = [50, 110, 500, 500]

with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        for i in range(0, len(scenario)):
            if row[0] in scenario[i] and "<position" in scenario[i+1]:

                # x = bbox[0] - float(row[1])
                x = bbox[0] + float(row[1])
                scenario[i+1] = re.sub(r'x="\d+\.\d+"', 'x="' +
                                       str(x) + '"', scenario[i+1])
                y = bbox[1] + (bbox[3] - float(row[2]))
                scenario[i+1] = re.sub(r'y="\d+\.\d+"', 'y="' +
                                       str(y) + '"', scenario[i+1])

                break

print("".join(scenario))
