import urllib.request, urllib.parse, urllib.error, time, csv, io

BASE = "https://www.ebi.ac.uk/ena/portal/api/search"

def fetch(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "aitu-bio-project"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read().decode()
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            print(f"retry {i+1}/{tries}: {e}", flush=True)
            time.sleep(2 ** i)
    raise RuntimeError("ENA unreachable")

def query(q, fields, limit):
    params = urllib.parse.urlencode({
        "result": "read_run", "query": q, "fields": fields,
        "limit": limit, "format": "tsv"})
    txt = fetch(f"{BASE}?{params}")
    return list(csv.DictReader(io.StringIO(txt), delimiter="\t"))

def main():
    nano = query('tax_tree(562) AND instrument_platform="OXFORD_NANOPORE" '
                 'AND library_strategy="WGS" AND library_source="GENOMIC"',
                 "run_accession,sample_accession,base_count,read_count,fastq_ftp", 100)
    nano = [r for r in nano if r["base_count"] and 2e8 <= int(r["base_count"]) <= 3e9]
    print(len(nano), "nanopore candidates", flush=True)
    found = 0
    for r in nano:
        ill = query(f'sample_accession="{r["sample_accession"]}" AND instrument_platform="ILLUMINA"',
                    "run_accession,base_count,read_count,library_layout,fastq_ftp", 10)
        if ill:
            print("\nPAIR sample", r["sample_accession"])
            print(" nanopore:", r["run_accession"], r["base_count"], r["fastq_ftp"])
            for i in ill:
                print(" illumina:", i["run_accession"], i["base_count"], i["library_layout"], i["fastq_ftp"])
            found += 1
            if found == 5:
                break
        time.sleep(0.5)

main()
