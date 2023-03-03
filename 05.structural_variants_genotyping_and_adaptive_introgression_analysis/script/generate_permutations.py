import argparse
import gzip
import random

header_left = "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT"


def generate_lines(sample_names, snps_gen):
    header = [header_left]
    header.extend(sample_names)
    header = "\t".join(header)

    labels_header = ("major_freq", "unknown_freq0", "unknown_freq1")

    yield header

    for chrom, pos, snps in snps_gen:
        cols = [chrom, str(pos), ".", "A", "T", "0", "PASS",
                "AC=30;AF=0.357;AN=84;DP=804;PercentNBaseSolid=0.0000;set=AGC", "GT"]
        cols.extend(snps)

        yield "\t".join(cols)


def vcf_writer(flname, stream):
    with gzip.open(flname, "wt") as fl:
        for ln in stream:
            fl.write(ln)
            fl.write("\n")


def read_vcf(flname):
    with open(flname) as fl:
        snps = []
        for ln in fl:
            if ln.startswith("##"):
                continue

            if ln.startswith("#"):
                header = ln
                continue

            cols = ln.split()
            chrom = cols[0]
            pos = int(cols[1])
            snps.append((chrom, pos, cols[9:]))

        header_cols = header.split()
        sample_names = header_cols[9:]
    return sample_names, snps


def generate_permutations(snps, n_permutations):
    for chrom, pos, variants in snps:
        # unpermuted version
        yield chrom, pos, variants
        for i in range(n_permutations):
            new_pos = str(pos) + "_" + str(i)
            random.shuffle(variants)
            yield chrom, new_pos,variants


def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-vcf",
                        type=str,
                        required=True)

    parser.add_argument("--n-permutations",
                        type=int,
                        required=True)

    parser.add_argument("--output-gz-vcf",
                        type=str,
                        required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parseargs()

    sample_names, original_snps = read_vcf(args.input_vcf)

    permutations = generate_permutations(original_snps,
                                         args.n_permutations)

    lines = generate_lines(sample_names,
                           permutations)

    vcf_writer(args.output_gz_vcf,
               lines)

