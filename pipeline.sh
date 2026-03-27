#!/bin/bash
#SBATCH -o /dev/null
#SBATCH -e /dev/null

shopt -s expand_aliases
mafft="apptainer exec /usr/local/biotools/m/mafft:7.525--h031d066_1 mafft"

config="$1"
workdir=$(dirname ${config})

key=$(jq -r '.gene.key' ${config})
name=$(jq -r '.gene.name' ${config})
taxon=$(jq -r '.taxon' ${config})
uselongest=$(jq -r '.use_longest_isoform' ${config})

case ${key} in
  refseq)
    echo "Command: datasets download gene accession ${name} --ortholog ${taxon}"
    datasets download gene accession ${name} --ortholog ${taxon}
    ;;
  id)
    echo "Command: datasets download gene gene-id ${name} --ortholog ${taxon}"
    datasets download gene gene-id ${name} --ortholog ${taxon}
    ;;
  symbol)
    echo "Command: datasets download gene symbol ${name} --ortholog ${taxon}"
    datasets download gene symbol ${name} --ortholog ${taxon}
    ;;
  *)
    echo 'Error: Use one of {"refseq", "id", "symbol"} as key.' >&2
    exit 1
    ;;
esac

unzip -fo ncbi_dataset.zip -d ${workdir} && rm ncbi_dataset.zip
python3 util.py report -i ${workdir}/ncbi_dataset/data/protein.faa --species_file ${workdir}/species.list

if [ ${uselongest} = "true" ]; then
  python3 util.py select -i ${workdir}/ncbi_dataset/data/protein.faa -o ${workdir}/protein.select.fa
  mafft --auto ${workdir}/protein.select.fa > ${workdir}/${name}.select.aln.fa
  python3 util.py aln2df -i ${workdir}/${name}.select.aln.fa -o ${workdir}/${name}.select.aln.tsv
else
  mafft --auto ${workdir}/ncbi_dataset/data/protein.faa > ${workdir}/${name}.aln.fa
  python3 util.py aln2df -i ${workdir}/${name}.aln.fa -o ${workdir}/${name}.aln.tsv
fi
