#!/usr/bin/env python3

import sys

iFilePath = sys.argv[1]
oFilePath = sys.argv[2]

with open(iFilePath, "r") as file:
    lines = file.readlines()

    lines = [line.strip() for line in lines]
    lines = [line for line in lines if not line.startswith("*")]

    assert lines[0] == "$OR;D2"

    lines = lines[1:]

    fromTime, toTime = lines[0].split()

    fromTimeH, fromTimeM = fromTime.split(".")
    fromTime = int(fromTimeH) * 60 + int(fromTimeM)

    toTimeH, toTimeM = toTime.split(".")
    toTime = int(toTimeH) * 60 + int(toTimeM)

    factor = float(lines[1])

    lines = lines[2:]

    lines = [[int(float(x)) for x in line.split()] for line in lines]

    flows = {}
    for source, sink, flow in lines:
        if source not in flows:
            flows[source] = {}
        flows[source][sink] = flow


def merge(toMerge):
    result = toMerge[0]
    toMerge = toMerge[1:]

    for source in toMerge:
        for sink in flows[source]:
            f = flows[source][sink]
            flows[source][sink] -= f
            flows[result][sink] += f

    for sink in toMerge:
        for source in flows:
            if sink in flows[source]:
                f = flows[source][sink]
                flows[source][sink] -= f
                flows[source][result] += f

    for source in toMerge:
        del flows[source]

    for source in flows:
        sinks = list(flows[source].keys())
        for sink in sinks:
            if sink in toMerge:
                del flows[source][sink]


merge([85, 86, 119, 120])

with open(oFilePath, "w") as f:
    f.write("$OR;D2\n")
    f.write("* From-Time  To-Time\n")
    f.write(
        "{:0>2}.{:0>2} {:0>2}.{:0>2}\n".format(
            fromTime // 60, fromTime % 60, toTime // 60, toTime % 60
        )
    )
    f.write("* Factor\n")
    f.write(f"{factor}\n")
    f.write("* Matrix\n")
    for source in flows:
        for sink in flows[source]:
            if flows[source][sink] != 0:
                f.write(f"{source} {sink} {flows[source][sink]}\n")
