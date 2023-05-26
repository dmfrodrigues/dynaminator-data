#!/usr/bin/python3

from xml.dom import minidom

from sys import argv

netFile = minidom.parse(argv[1])

locationEl = netFile.getElementsByTagName("location")[0]
xOffsetStr, yOffsetStr = locationEl.getAttribute("netOffset").split(",")
xOffset, yOffset = float(xOffsetStr), float(yOffsetStr)

x, y = xOffset, yOffset
# x, y = 10, 20

xMinStr, yMinStr, xMaxStr, yMaxStr = locationEl.getAttribute("convBoundary").split(",")
xMin, yMin, xMax, yMax = float(xMinStr), float(yMinStr), float(xMaxStr), float(yMaxStr)

locationEl.setAttribute("netOffset", f"{xOffset-x},{yOffset-y}")
locationEl.setAttribute("convBoundary", f"{xMin-x},{yMin-y},{xMax-x},{yMax-y}")

# Parse net file
for edge in netFile.getElementsByTagName("edge"):
    if edge.hasAttribute("shape"):
        edgeShape = [(float(p[0]) - x, float(p[1]) - y) for p in 
            [coord.split(",") for coord in edge.getAttribute("shape").split(" ") if coord != ""]
        ]
        edge.setAttribute("shape", " ".join([f"{p[0]:.2f},{p[1]:.2f}" for p in edgeShape]))

    for lane in edge.getElementsByTagName("lane"):
        if lane.hasAttribute("shape"):
            laneShape = [(float(p[0]) - x, float(p[1]) - y) for p in 
                [coord.split(",") for coord in lane.getAttribute("shape").split(" ") if coord != ""]
            ]
            lane.setAttribute("shape", " ".join([f"{p[0]:.2f},{p[1]:.2f}" for p in laneShape]))
        
for junction in netFile.getElementsByTagName("junction"):
    if junction.hasAttribute("shape"):
        junctionShape = [(float(p[0]) - x, float(p[1]) - y) for p in 
            [coord.split(",") for coord in junction.getAttribute("shape").split(" ") if coord != ""]
        ]
        junction.setAttribute("shape", " ".join([f"{p[0]:.2f},{p[1]:.2f}" for p in junctionShape]))
        
        xPosStr, yPosStr = junction.getAttribute("x"), junction.getAttribute("y")
        xPos, yPos = float(xPosStr), float(yPosStr)
        xPos -= x
        yPos -= y
        junction.setAttribute("x", f"{xPos:.2f}")
        junction.setAttribute("y", f"{yPos:.2f}")

print(netFile.toxml())
