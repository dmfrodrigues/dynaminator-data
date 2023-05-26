import glob
import re
import subprocess

pattern_glob = "tiles/porto*_*.jpeg"
pattern = "tiles/porto(.*)_(.*)\.jpeg"
regex = re.compile(pattern)

xMin, xMax, yMin, yMax = 1e6, -1e6, 1e6, -1e6

for filename in glob.glob(pattern_glob):
    matches = regex.search(filename)
    x, y = int(matches.group(1)), int(matches.group(2))
    xMin = min(xMin, x)
    xMax = max(xMax, x)
    yMin = min(yMin, y)
    yMax = max(yMax, y)

for x in range(xMin, xMax + 1):
    paths = [f"tiles/porto{x}_{y}.jpeg" for y in range(yMin, yMax + 1)]
    subprocess.run(["convert", "-append"] + paths + [f"tiles/{x}.jpeg"])

paths = [f"tiles/{x}.jpeg" for x in range(xMin, xMax + 1)]

print(len(paths))
print(paths)

subprocess.run(["convert", "+append"] + paths + ["porto.jpeg"])
