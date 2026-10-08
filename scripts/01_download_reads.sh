#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
BASE=https://ftp.sra.ebi.ac.uk/vol1/fastq
dl() { curl -fL --retry 8 --retry-delay 5 --retry-all-errors -C - -o "$2" "$1"; echo "$(date -I) $1" >> logs/accessions.log; }
dl $BASE/ERR103/094/ERR10317394/ERR10317394.fastq.gz   data/raw/nano.fastq.gz
dl $BASE/ERR401/000/ERR4019840/ERR4019840_1.fastq.gz   data/raw/ill_1.fastq.gz
dl $BASE/ERR401/000/ERR4019840/ERR4019840_2.fastq.gz   data/raw/ill_2.fastq.gz
seqtk sample -s42 data/raw/ill_1.fastq.gz 200000 | gzip > data/sub/ill_1.fastq.gz
seqtk sample -s42 data/raw/ill_2.fastq.gz 200000 | gzip > data/sub/ill_2.fastq.gz
seqtk sample -s42 data/raw/nano.fastq.gz  30000  | gzip > data/sub/nano.fastq.gz
