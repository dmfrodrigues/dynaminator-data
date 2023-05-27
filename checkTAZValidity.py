#!/usr/bin/python3

from xml.dom import minidom
import sys

netFile = minidom.parse(sys.argv[1])
tazFile = minidom.parse(sys.argv[2])

edgeIDs = set(edge.getAttribute("id") for edge in netFile.getElementsByTagName("edge"))

usedEdgeIDs = set()

returnCode = 0

for taz in tazFile.getElementsByTagName("taz"):
    tazID = taz.getAttribute("id")
    
    for source in taz.getElementsByTagName("tazSource"):
        sourceID = source.getAttribute("id")
        if sourceID not in edgeIDs:
            print(f"Error: TAZ {tazID}, source {sourceID} not found")
            returnCode = -1
    
    for sink in taz.getElementsByTagName("tazSink"):
        sinkID = source.getAttribute("id")
        if sinkID not in edgeIDs:
            print(f"Error: TAZ {tazID}, sink {sinkID} not found")
            returnCode = -1
    
    tazEdgeIDs = \
        [edge.getAttribute("id") for edge in taz.getElementsByTagName("tazSource")] + \
        [edge.getAttribute("id") for edge in taz.getElementsByTagName("tazSink")]
    for edge in tazEdgeIDs:
        if edge in usedEdgeIDs:
            print("Warning: TAZ {tazID}, edge {edge} is also present in another edge")
    
    usedEdgeIDs |= set(edge)

sys.exit(returnCode)
