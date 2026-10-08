#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/genomes data/batches
tail -n +2 data/genomes_meta.tsv | cut -f1 > data/accessions.txt
split -l 25 -d data/accessions.txt data/batches/b_
for b in data/batches/b_??; do
  n=$(basename "$b")
  [ -f data/batches/$n.done ] && continue
  for try in 1 2 3 4 5; do
    rm -rf data/batches/$n.zip data/batches/$n.unz
    if datasets download genome accession --inputfile "$b" --include genome \
         --filename data/batches/$n.zip --no-progressbar \
       && unzip -q -o data/batches/$n.zip -d data/batches/$n.unz; then
      for f in data/batches/$n.unz/ncbi_dataset/data/*/*.fna; do
        acc=$(basename "$(dirname "$f")"); cp "$f" "data/genomes/$acc.fna"
      done
      touch data/batches/$n.done; echo "$n ok"; break
    else
      echo "$n retry $try"; sleep $((try*5))
    fi
  done
done
ls data/genomes/*.fna | wc -l
