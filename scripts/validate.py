import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load_sourmash(path):
    m = pd.read_csv(path)
    m.index = [c.split()[0] for c in m.columns]
    m.columns = m.index
    return m

def load_skani(path):
    s = pd.read_csv(path, sep="\t")
    s["a"] = s["Ref_name"].str.split().str[0]
    s["b"] = s["Query_name"].str.split().str[0]
    return s[s["a"] != s["b"]].copy()

def paired(m, s):
    ok = s["a"].isin(m.index) & s["b"].isin(m.index)
    s = s[ok].copy()
    s["sm"] = [m.at[a, b] * 100 for a, b in zip(s["a"], s["b"])]
    return s

def summarize(p):
    d = p[p["sm"] > 0]
    err = d["sm"] - d["ANI"]
    return pd.Series({
        "pairs_skani": len(p),
        "pairs_both": len(d),
        "sketch_missed": int((p["sm"] == 0).sum()),
        "mae_ani_points": err.abs().mean(),
        "bias_ani_points": err.mean(),
        "pearson_r": d["sm"].corr(d["ANI"]),
    })

def plot(p, path):
    d = p[p["sm"] > 0]
    lim = [d["ANI"].min(), 100]
    plt.figure(figsize=(5, 5))
    plt.scatter(d["ANI"], d["sm"], s=8)
    plt.plot(lim, lim, "r--")
    plt.xlabel("skani ANI (%)")
    plt.ylabel("sourmash ANI (%)")
    plt.savefig(path, dpi=200, bbox_inches="tight")

def main():
    p = paired(load_sourmash("data/compare.csv"), load_skani("data/skani_all.txt"))
    res = summarize(p)
    res.to_csv("results/validation_summary.csv")
    plot(p, "results/ani_validation.png")
    print(res)

main()
