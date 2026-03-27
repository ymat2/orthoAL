# OrthoAL

Pipeline to retrieve, align, and format ortholog sequences for personal use.
[`pipeline.sh`](./pipeline.sh) is expected to be executed as SLURM batch job on NIG supercomputer.


## Requirements

- Python3 (>=3.12)
- [NCBI datasets CLI](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/command-line-tools/download-and-install/)
- some alignment tool
  - MAFFT


## Usage

Make working directory and write `config.json` in the directory:

```sh
mkdir proj
touch proj/config.json
```

Run `pipeline.sh` with config.json as an argument.
All outputs are generated in the working directory:

```sh
sbatch pipeline.sh proj/config.json
```

The contents of `config.json` should be:

```json
{
  "gene": {
    "key": "symbol",
    "name": "cftr"
  },
  "taxon": "mammals",
  "use_longest_isoform": true
}
```

- `"gene": "key"` should be one of `"symbol", "id", or "refseq"`
- `"use_longest_isoform"` controls whether to use only the longest isoforms per species for alignment
- See more:
  [How-to guides for downloading an ortholog data packages](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/how-tos/genes/download-ortholog-data-package/)
