import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = []

times = {
    100: None,
    1000: 11.443,
    5000: 4.034
}

for scaled in [100, 1000, 5000]:
    path = f"results/sketch_size/sketch_{scaled}.sig.zip"
    size_mb = os.path.getsize(path) / (1024 * 1024)

    rows.append({
        "scaled": scaled,
        "file_size_MB": round(size_mb, 2),
        "comparison_time_sec": times[scaled]
    })

df = pd.DataFrame(rows)
df.to_csv("results/sketch_size/sketch_size_summary.csv", index=False)

plt.figure(figsize=(6, 4))
plt.plot(df["scaled"], df["file_size_MB"], marker="o")
plt.xscale("log")
plt.xlabel("Scaled parameter")
plt.ylabel("Sketch file size (MB)")
plt.title("Sketch size vs. scaled parameter")
plt.tight_layout()
plt.savefig("results/sketch_size/sketch_size.png", dpi=200)
print(df)
