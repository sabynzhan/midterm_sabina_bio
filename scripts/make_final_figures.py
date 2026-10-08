import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

Path("results/figures").mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 1. Sketch size vs scaled parameter
# --------------------------------------------------

df = pd.read_csv(
    "results/sketch_size/sketch_size_summary.csv"
)

plt.figure(figsize=(7, 5))
plt.plot(
    df["scaled"],
    df["file_size_MB"],
    marker="o"
)
plt.xscale("log")
plt.xlabel("Scaled parameter")
plt.ylabel("Sketch file size (MB)")
plt.title("Sketch Size vs. Scaled Parameter")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    "results/figures/sketch_size_vs_scaled.png",
    dpi=300
)
plt.close()


# --------------------------------------------------
# 2. FastANI vs Sourmash validation
# --------------------------------------------------

summary = pd.read_csv(
    "results/validation_50/validation_summary.csv"
)

plt.figure(figsize=(7, 5))
plt.plot(
    summary["scaled"],
    summary["Pearson_r"],
    marker="o"
)
plt.xscale("log")
plt.ylim(0.98, 1.0)
plt.xlabel("Scaled parameter")
plt.ylabel("Pearson correlation")
plt.title("Sourmash vs. FastANI Agreement")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    "results/figures/validation_pearson.png",
    dpi=300
)
plt.close()


# --------------------------------------------------
# 3. Nanopore raw vs filtered
# --------------------------------------------------

nano = pd.DataFrame({
    "Dataset": ["Raw Nanopore", "Q10 filtered"],
    "Reads": [30000, 24766],
    "Hashes": [110563, 85553]
})

plt.figure(figsize=(7, 5))
plt.bar(
    nano["Dataset"],
    nano["Hashes"]
)
plt.ylabel("Number of sketch hashes")
plt.title("Effect of Nanopore Quality Filtering")
plt.tight_layout()
plt.savefig(
    "results/figures/nanopore_filtering.png",
    dpi=300
)
plt.close()


# --------------------------------------------------
# 4. Search latency vs collection size
# --------------------------------------------------

search = pd.DataFrame({
    "Genomes": [100, 200, 500],
    "Time": [2.443, 3.560, 6.865]
})

plt.figure(figsize=(7, 5))
plt.plot(
    search["Genomes"],
    search["Time"],
    marker="o"
)
plt.xlabel("Number of indexed genomes")
plt.ylabel("Search time (seconds)")
plt.title("SBT Search Latency vs. Collection Size")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    "results/figures/search_latency.png",
    dpi=300
)
plt.close()


print("Created final figures:")
for f in Path("results/figures").glob("*.png"):
    print(f)
