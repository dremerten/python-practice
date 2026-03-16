import csv
from collections import namedtuple
import pprint

Tree = namedtuple("Tree", ["index", "width", "height", "volume"])

with open("trees.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    breakpoint()
    # Store all Tree objects inside a tuple using a comprehension.
    trees = tuple(
        Tree(
            int(row["Idx"]),
            float(row["Width (in)"]),
            int(row["Height (ft)"]),
            float(row["Volume(ft^3)"])
        )
        for row in reader
    )

pprint.pprint(trees, indent=4)
