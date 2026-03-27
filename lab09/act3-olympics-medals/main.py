'''
    Olympics Medals
    Author: Saksham Rathi
'''

from argparse import ArgumentParser as ap
import os

parser = ap()
parser.add_argument('--path', type=str, required=True)
args = parser.parse_args()

totalData = {}

for fileName in os.listdir(args.path):
    with open(os.path.join(args.path, fileName), 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('-')
            country = parts[0]
            gold, silver, bronze = int(parts[1]), int(parts[2]), int(parts[3])
            if country not in totalData:
                totalData[country] = [0, 0, 0]
            totalData[country][0] += gold
            totalData[country][1] += silver
            totalData[country][2] += bronze

sorted_data = dict(sorted(totalData.items(), key=lambda x: (-x[1][0], x[0])))
print(sorted_data)
