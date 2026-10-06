set -euo pipefail
find data/genomes -name "*.fna" > data/fna_list.txt
wc -l data/fna_list.txt
TIMEFORMAT='%R sec'
{ time sourmash sketch dna -p k=31,scaled=1000 --name-from-first --from-file data/fna_list.txt -o data/sketches.sig.zip ; } 2> data/sketch_time.txt
{ time sourmash compare data/sketches.sig.zip -k 31 --ani --csv data/compare.csv -o data/compare.np ; } 2> data/compare_time.txt
tail -n 1 data/sketch_time.txt data/compare_time.txt
ls -lh data/sketches.sig.zip data/compare.csv
