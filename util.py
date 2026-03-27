
import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="subcommand", choices=["aln2df", "report", "rename", "select"])
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    parser.add_argument("--species_file")
    args = parser.parse_args()

    if args.cmd == "aln2df":
        aln2df(args.input, args.output)

    if args.cmd == "rename":
        rename()

    if args.cmd == "report":
        msg = report(args.input, args.species_file)
        print(msg)

    if args.cmd == "select":
        select(args.input, args.output)


def aln2df(aln: Path, outfile: Path) -> None:
    aln_dict = read_fasta_as_dict(aln)
    seq_length = [len(v) for v in aln_dict.values()][0]
    with open(outfile, "w") as f:
        f.write("header\t")
        f.write("\t".join([str(i+1) for i in range(seq_length)])+"\n")
        for k,v in aln_dict.items():
            f.write(k.lstrip(">")+"\t")
            f.write("\t".join(v)+"\n")


def rename():
    print("Sorry, function 'rename' is under development...")


def report(fasta: Path, outfile: Path) -> str:
    fasta_dict = read_fasta_as_dict(fasta)
    species_list = list()
    pattern = r"\[organism=(.*?)\]"
    for k in fasta_dict.keys():
        match = re.search(pattern, k)
        sp = match.group(1) if match else None
        if sp not in species_list:
            species_list.append(sp)
    number_of_sequence = len(fasta_dict)
    number_of_species = len(species_list)
    if outfile:
        with open(outfile, "w") as f:
            f.write("\n".join(species_list))
    msg = "Number of sequence: {}\nNumber of species: {}".format(number_of_sequence, number_of_species)
    return(msg)


def select(infile: Path, outfile:Path) -> None:
    fasta_dict = read_fasta_as_dict(infile)
    longest_isoforms = dict()
    pattern = r"\[organism=(.*?)\]"
    for k,v in fasta_dict.items():
        match = re.search(pattern, k)
        sp = match.group(1) if match else None
        if sp not in longest_isoforms:
            longest_isoforms[sp] = [k,v]
        elif len(longest_isoforms[sp][1]) < len(v):
            longest_isoforms[sp] = [k,v]
        else:
            continue
    with open(outfile, "w") as f:
        for k,v in longest_isoforms.items():
            [id, seq] = v
            f.write(">"+id+"\n"+seq+"\n")


def read_fasta_as_dict(fasta: Path) -> dict:
    fas2dct = dict()
    tmp_key = ""
    with open(fasta) as f:
        for line in f:
            if line[0]==">":
                tmp_key = line.rstrip("\n")
                fas2dct[tmp_key] = ""
            else:
                fas2dct[tmp_key] = fas2dct[tmp_key] + line.rstrip("\n")
    return(fas2dct)


if __name__ == "__main__":
    main()
