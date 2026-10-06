set -euo pipefail
mkdir -p data
datasets summary genome taxon bacteria --reference --assembly-level complete --limit 200 --as-json-lines | dataformat tsv genome --fields accession | tail -n +2 > data/acc.txt
date -I > data/retrieval_date.txt
datasets download genome accession --inputfile data/acc.txt --include genome --filename data/genomes.zip
unzip -oq data/genomes.zip -d data/genomes
