#!/usr/bin/env python
from collections import defaultdict
import argparse
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-p", "--path", help="path_tracefile")
    parser.add_argument("-e", "--edge", help="edgecovfile")
    parser.add_argument("-o", "--outfile", help="output file")
    return parser.parse_args()

def parse_edge_file(edgefile):
    combedge = defaultdict(dict)
    with open(edgefile) as infile:
            for line in infile:
                parent, child, coverage = line.strip().split()
                combedge[parent][child] = coverage
    return combedge

def extract_coverage(combedge, paths):
    coverage = 0
    coveragelist=[]
    for ind, node in enumerate(paths[:-1]):
        parent = node
        child = paths[ind + 1]
        coveragelist.append(int(combedge[parent][child]))
    nodecover = min(coveragelist)
    return nodecover

if __name__ == "__main__":
    args = parse_args()
    svfile = args.path
    edgefile = args.edge
    combedge = parse_edge_file(edgefile)
    outfile = args.outfile
    with open(svfile) as infile, open(outfile, "a") as outfile:
        for line in infile:
            # biallelic        1_165873        AltDel          497     2       s1,s2,s3        UCD,OBV         s1,s133016,s3   Angus,OBV
            linecomp = line.strip().split()
            sv_comp = linecomp[:3]
            ref_path = linecomp[5].split(",")
            nonref_path = linecomp[-2].split(",")
            ref_cover = extract_coverage(combedge, paths=ref_path)
            nonref_cover = extract_coverage(combedge, paths=nonref_path)

            print(*sv_comp, linecomp[5], linecomp[-2], ref_cover, nonref_cover, file=outfile)

