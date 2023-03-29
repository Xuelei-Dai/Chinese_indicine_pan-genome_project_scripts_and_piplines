import argparse
import random,gzip

header_left = "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT"

def generate_lines(sample_names, snps_gen):
    header = [header_left]
    header.extend(sample_names)
    header = "\t".join(header)

    labels_header = ("major_freq", "unknown_freq0", "unknown_freq1")

    yield header

    for chrom, pos, snps in snps_gen:
        cols = [chrom, str(pos), '.', "A", "T", "0", "PASS", "AC=30;AF=0.357;AN=84;DP=804;PercentNBaseSolid=0.0000;set=AGC", "GT"]
        cols.extend(snps)

        yield "\t".join(cols)

def vcf_writer(flname, stream):
    with open(flname, "w") as fl:
        for ln in stream:
            fl.write(ln)
            fl.write("\n")

def read_vcf(flname):
    fl = gzip.open(flname,'rb')
    snps = []
    for ln in fl:
        ln = ln.decode().strip()
        if ln.startswith("##"):
            continue
        if ln.startswith("#"):
            header = ln
            header_cols = header.split()
            sample_names = header_cols[9:]
            yield sample_names
            continue
            
        cols = ln.split()
        chrom = cols[0]
        pos = int(cols[1])
        yield (chrom, pos,cols[9:])

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-vcf",
                        type=str,
                        required=True)

    parser.add_argument("--chunk-size",
                        type=int,
                        required=True)

    parser.add_argument("--output-base",
                        type=str,
                        required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parseargs()

    vcf_reader = read_vcf(args.input_vcf)

    sample_names = next(vcf_reader)

    chunk = []
    chunk_count = 1
    for variants in vcf_reader:
        chunk.append(variants)

        if len(chunk) == args.chunk_size:
            flname = args.output_base + "%03d.vcf" % chunk_count
            lines = generate_lines(sample_names, chunk)
            print ("Writing chunk %s" % chunk_count)
            vcf_writer(flname, lines)
            chunk = []
            chunk_count += 1

    if len(chunk) > 0:
        print ("Writing chunk %s" % chunk_count)
        flname = args.output_base + "%03d.vcf" % chunk_count
        lines = generate_lines(sample_names, chunk)
        vcf_writer(flname, lines)

    

    
