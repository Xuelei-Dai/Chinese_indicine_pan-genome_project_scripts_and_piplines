import argparse
from collections import defaultdict

import numpy as np

def read_fst_scores(flname):
    with open(flname) as fl:
        scores = []
        current_pos = None
        # skip header
        next(fl)
        for ln in fl:
            cols = ln.split()
            Chr = cols[0]
            pos = cols[1]
            score = float(cols[2])
            if np.isnan(score):
                score = 0.0
            if current_pos != pos:
                if current_pos != None:
                    # first entry is true fst
                    yield Chr, current_pos, scores[0], scores[1:]
                scores = [score]
                current_pos = pos
            else:
                scores.append(score)

    # first entry is true fst            
    yield Chr, current_pos, scores[0], scores[1:]

def calculate_pvalues(original, permuted):
    permuted = sorted(permuted)
    idx = np.searchsorted(permuted, original, side="left")
    l = float(len(permuted))
    if l == 0.0:
        pvalue ="None"
    else:
        pvalue = max((l - idx) / l, 1.0 / l)
    return pvalue

def write_pvalues(flname, pvalues):
    with open(flname, "w") as fl:
        for pos, pvalue in pvalues:
            fl.write("\t".join([str(pos), str(pvalue)]))
            fl.write("\n")


def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--permutation-fst",
                        type=str,
                        required=True)

    parser.add_argument("--output-fl",
                        type=str,
                        required=True)

    return parser.parse_args()

if __name__ == "__main__":
    args = parseargs()

    with open(args.output_fl, "w") as fl:
        for Chr, pos, true_fst, permuted_fst in read_fst_scores(args.permutation_fst):
            pvalue = calculate_pvalues(true_fst, permuted_fst)
            if pvalue != "None":
                line="\t".join([str(Chr), str(pos),str(true_fst), str(pvalue)])
                fl.write(f'{line}\n')
        else:
            pass

    
