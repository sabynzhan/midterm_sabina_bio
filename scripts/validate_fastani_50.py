import pandas as pd
import numpy as np
from pathlib import Path

FASTANI = "results/fastani_50.txt"
MAPPING = "data/gcf_to_accession_50.tsv"


def load_mapping():
    m = pd.read_csv(
        MAPPING,
        sep=r"\s+",
        header=None,
        names=["gcf", "accession"]
    )
    return dict(zip(m["gcf"], m["accession"]))


def load_fastani(path, mapping):
    df = pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=[
            "query",
            "reference",
            "ANI",
            "fragments",
            "total_fragments"
        ]
    )

    # Convert GCF filenames to FASTA accessions
    df["query"] = (
        df["query"]
        .str.split("/")
        .str[-1]
        .str.replace(".fna", "", regex=False)
        .map(mapping)
    )

    df["reference"] = (
        df["reference"]
        .str.split("/")
        .str[-1]
        .str.replace(".fna", "", regex=False)
        .map(mapping)
    )

    df = df.dropna(subset=["query", "reference"])

    # Remove self-comparisons
    df = df[df["query"] != df["reference"]].copy()

    # Keep only one direction of each pair
    df["pair"] = df.apply(
        lambda r: tuple(sorted([r["query"], r["reference"]])),
        axis=1
    )

    df = df.drop_duplicates("pair")

    return df


def load_sourmash(path):
    df = pd.read_csv(path)

    # Sourmash stores genome names in column headers
    labels = list(df.columns)

    accessions = [
        str(x).split()[0]
        for x in labels
    ]

    df.index = accessions
    df.columns = accessions

    return df


def compare_results(fastani, sourmash, scaled):

    rows = []

    for _, r in fastani.iterrows():

        q = r["query"]
        ref = r["reference"]

        if q not in sourmash.index:
            continue

        if ref not in sourmash.columns:
            continue

        sm = float(sourmash.loc[q, ref]) * 100
        ani = float(r["ANI"])

        rows.append({
            "query": q,
            "reference": ref,
            "fastANI": ani,
            "sourmash_ANI": sm,
            "absolute_error": abs(sm - ani),
            "signed_error": sm - ani,
            "sourmash_zero": sm == 0
        })

    result = pd.DataFrame(rows)

    if result.empty:
        raise RuntimeError(
            f"No matching pairs found for scaled={scaled}"
        )

    nonzero = result[result["sourmash_ANI"] > 0].copy()

    summary = {
        "scaled": scaled,
        "FastANI_pairs": len(result),
        "Sourmash_nonzero_pairs": len(nonzero),
        "Sourmash_zero_pairs": int(
            result["sourmash_zero"].sum()
        ),
        "MAE_all_pairs": result["absolute_error"].mean(),
        "MAE_nonzero": (
            nonzero["absolute_error"].mean()
            if len(nonzero) else np.nan
        ),
        "Bias_nonzero": (
            nonzero["signed_error"].mean()
            if len(nonzero) else np.nan
        ),
        "Pearson_r": (
            nonzero["fastANI"].corr(
                nonzero["sourmash_ANI"]
            )
            if len(nonzero) > 1 else np.nan
        )
    }

    return result, summary


def main():

    Path("results/validation_50").mkdir(
        parents=True,
        exist_ok=True
    )

    mapping = load_mapping()

    fastani = load_fastani(
        FASTANI,
        mapping
    )

    print("FastANI unique pairs:", len(fastani))

    all_summary = []

    for scaled in [100, 1000, 5000]:

        print()
        print("=" * 50)
        print(f"Processing scaled={scaled}")
        print("=" * 50)

        path = (
            f"results/validation_50/"
            f"compare_{scaled}.csv"
        )

        sourmash = load_sourmash(path)

        print(
            "Sourmash genomes:",
            len(sourmash)
        )

        pairs, summary = compare_results(
            fastani,
            sourmash,
            scaled
        )

        pairs.to_csv(
            f"results/validation_50/"
            f"pairs_{scaled}.csv",
            index=False
        )

        all_summary.append(summary)

        print()
        print("Pairs matched:", len(pairs))
        print(
            "Non-zero Sourmash:",
            summary["Sourmash_nonzero_pairs"]
        )
        print(
            "Zero Sourmash:",
            summary["Sourmash_zero_pairs"]
        )
        print(
            "MAE:",
            round(summary["MAE_all_pairs"], 4)
        )
        print(
            "Bias:",
            round(summary["Bias_nonzero"], 4)
        )
        print(
            "Pearson r:",
            round(summary["Pearson_r"], 4)
        )

    summary_df = pd.DataFrame(all_summary)

    summary_df.to_csv(
        "results/validation_50/"
        "validation_summary.csv",
        index=False
    )

    print()
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    print(
        summary_df.to_string(index=False)
    )

    print()
    print(
        "Saved: "
        "results/validation_50/validation_summary.csv"
    )


if __name__ == "__main__":
    main()
