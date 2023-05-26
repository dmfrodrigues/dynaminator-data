#!/usr/bin/python3

from xml.dom import minidom

from sys import argv

netFile = minidom.parse(argv[1])
tazFile = minidom.parse(argv[2])

# Parse net file
edgeShapes = {}
for edge in netFile.getElementsByTagName("edge"):
    edgeID = edge.getAttribute("id")
    edgeShape = [(float(p[0]), float(p[1])) for p in 
        [coord.split(",") for coord in edge.getAttribute("shape").split(" ") if coord != ""]
    ]
    for lane in edge.getElementsByTagName("lane"):
        laneID = lane.getAttribute("id")
        laneShape = [(float(p[0]), float(p[1])) for p in 
            [coord.split(",") for coord in lane.getAttribute("shape").split(" ") if coord != ""]
        ]
        edgeShape += laneShape
    
    edgeShapes[edgeID] = edgeShape

for taz in tazFile.getElementsByTagName("taz"):
    xMin, xMax, yMin, yMax = 1e12, -1e12, 1e12, -1e12
    
    srcIDs = [u.getAttribute("id") for u in taz.getElementsByTagName("tazSource")]
    snkIDs = [u.getAttribute("id") for u in taz.getElementsByTagName("tazSink")]
    edgeIDs = srcIDs + snkIDs
    
    for edgeID in edgeIDs:
        if edgeID not in edgeShapes:
            print("Edge not found: " + edgeID)
            exit(1)
        edgeShape = edgeShapes[edgeID]
        for p in edgeShape:
            xMin = min(xMin, p[0])
            xMax = max(xMax, p[0])
            yMin = min(yMin, p[1])
            yMax = max(yMax, p[1])

    shape = f"{xMin},{yMin} {xMax},{yMin} {xMax},{yMax} {xMin},{yMax} {xMin},{yMin}"
    taz.setAttribute("shape", shape)

print(tazFile.toxml())
