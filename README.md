# Sketching: Searching a Million Genomes Without Aligning Any

## Bioinformatics Midterm Project — Project 29

This project develops a sketch-based genome similarity search workflow using MinHash sketches instead of full pairwise sequence alignment.

## Project Goal

Pairwise comparison of a large genome collection becomes computationally expensive because the number of comparisons grows approximately quadratically with the number of genomes.

The project uses k-mer sets, Jaccard similarity and MinHash sketches to create compact genome signatures. These signatures can then be indexed and searched efficiently.

The current experimental collection contains 500 real bacterial genomes from NCBI RefSeq.

## Methods

The main parameters are:

- k-mer size: k = 31
- MinHash sketching
- sourmash
- scaled values: 100, 1000 and 5000
- SBT index for similarity search
- FastANI as an alignment-based validation baseline

Jaccard similarity is:

J(A,B) = |A intersection B| / |A union B|

For a MinHash sketch with m sampled hashes, the approximate standard error is:

SE = sqrt(J(1-J)/m)

Larger sketches generally provide more accurate estimates, while smaller sketches require less storage and computation.

## Data

The project uses real bacterial genome data from the NCBI RefSeq collection.

Accession information is stored in:

- data/accessions.txt
- data/accessions_500.txt
- data/genomes_meta.tsv
- data/genomes_500_metadata.tsv

The retrieval date is documented in:

data/retrieval_date.txt

Large genome FASTA files and sequencing reads are excluded from Git.

## Workflow

The main workflow is:

Genome FASTA
    |
    v
k-mer generation
    |
    v
MinHash sketch
    |
    v
Sketch collection
    |
    v
SBT index
    |
    v
Similarity search

The reproducible Snakemake test follows:

sketch -> index -> search

## Reproducibility

The repository contains:

- Snakefile
- environment.yml
- environment-linux-64.lock
- small test genomes
- analysis scripts
- metadata and accession lists
- result files and figures

The test dataset is located in:

data/test/

The complete test workflow can be reproduced with:

snakemake --cores 2

The main test output is:

results/test_search.csv

The workflow summary is:

results/workflow_summary.txt

## Test Result

The test query genome correctly identifies itself with:

Similarity = 1.0

The second test genome has a Jaccard similarity of approximately 0.0782.

This confirms that the sketching, indexing and search workflow works end-to-end.

## Sketch Size Experiment

Three sketch resolutions were tested:

| Scaled | Sketch size |
|---:|---:|
| 100 | 170.00 MB |
| 1000 | 16.89 MB |
| 5000 | 3.54 MB |

Increasing the scaled parameter greatly reduces the sketch size.

The main practical configuration is scaled = 1000 because it provides a good balance between compactness and similarity accuracy.

## FastANI Validation

Sketch similarity was compared with FastANI on a subset of 50 genomes.

The validation contained 675 comparable genome pairs.

| Scaled | Pearson correlation | MAE |
|---:|---:|---:|
| 100 | 0.9961 | 2.90 percentage points |
| 1000 | 0.9963 | 2.97 percentage points |
| 5000 | 0.9933 | 3.83 percentage points |

The results show very high correlation between sketch-based similarity and the FastANI baseline.

## Illumina Analysis

Illumina paired-end reads were sketched directly without assembly.

Quality filtering was performed using fastp.

Before filtering:

- R1: 200,000 reads
- R2: 200,000 reads

After filtering:

- R1: 109,603 reads
- R2: 109,603 reads

The raw and filtered R1 sketches had a Jaccard similarity of approximately 0.691.

This demonstrates that sequencing quality can substantially affect k-mer composition.

## Nanopore Analysis

Nanopore reads were also sketched directly without assembly.

Quality filtering was performed using NanoFilt with Q10.

Results:

- Raw reads: 30,000
- Filtered reads: 24,766
- Raw sketch hashes: 110,563
- Filtered sketch hashes: 85,553

The raw and filtered sketches had a Jaccard similarity of approximately 0.774.

NanoFilt provides quality filtering rather than full sequence-error correction. Therefore, this experiment evaluates quality-based preprocessing and this limitation is documented in the project.

## Search Scaling

SBT search latency was measured for different collection sizes:

| Genomes | Search time |
|---:|---:|
| 100 | 2.443 s |
| 200 | 3.560 s |
| 500 | 6.865 s |

The experiment demonstrates that sketch-based indexing enables rapid search without performing full pairwise genome alignments for every query.

## Figures

Main figures are located in:

results/figures/

They include:

- sketch size versus scaled parameter
- FastANI validation correlation
- Nanopore filtering effect
- search latency versus collection size

## Repository Structure

```text
.
├── Snakefile
├── README.md
├── LICENSE
├── environment.yml
├── environment-linux-64.lock
├── data/
├── scripts/
├── results/
└── .gitignore