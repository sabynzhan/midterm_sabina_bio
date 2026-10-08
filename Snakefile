from pathlib import Path

TEST_GENOMES = sorted(Path("data/test").glob("*.fna"))

if len(TEST_GENOMES) < 2:
    raise ValueError("Need at least two test genomes in data/test/")

GENOME1 = str(TEST_GENOMES[0])
GENOME2 = str(TEST_GENOMES[1])


rule all:
    input:
        "results/test_search.csv",
        "results/workflow_summary.txt"


rule sketch_test_genomes:
    input:
        genomes=TEST_GENOMES
    output:
        "results/test_sketches.sig.zip"
    shell:
        """
        sourmash sketch dna \
            -p k=31,scaled=1000 \
            --name-from-first \
            {input.genomes} \
            -o {output}
        """


rule sketch_query:
    input:
        GENOME1
    output:
        "results/test_query.sig.zip"
    shell:
        """
        sourmash sketch dna \
            -p k=31,scaled=1000 \
            --name-from-first \
            {input} \
            -o {output}
        """


rule build_index:
    input:
        "results/test_sketches.sig.zip"
    output:
        "results/test_index.sbt.zip"
    shell:
        """
        sourmash index \
            -k 31 \
            --dna \
            -F SBT \
            {output} \
            {input}
        """


rule search:
    input:
        query="results/test_query.sig.zip",
        index="results/test_index.sbt.zip"
    output:
        "results/test_search.csv"
    shell:
        """
        sourmash search \
            {input.query} \
            {input.index} \
            -k 31 \
            -n 5 \
            --threshold 0 \
            -o {output}
        """


rule workflow_summary:
    input:
        search="results/test_search.csv",
        genomes=TEST_GENOMES
    output:
        "results/workflow_summary.txt"
    run:
        Path("results").mkdir(exist_ok=True)

        with open(output[0], "w") as f:
            f.write("Bioinformatics Sketching Project\n")
            f.write("================================\n")
            f.write(f"Test genomes: {len(input.genomes)}\n")
            f.write("Source: NCBI RefSeq bacterial genomes\n")
            f.write("Sketch method: MinHash / sourmash\n")
            f.write("k-mer size: 31\n")
            f.write("Scaled parameter: 1000\n")
            f.write("Workflow: sketch -> index -> search\n")
            f.write("Search query: genome1.fna\n")
            f.write("Result: results/test_search.csv\n")
