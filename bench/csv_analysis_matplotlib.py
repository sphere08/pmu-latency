import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_FILE = os.path.join("../results/csv_files", "latency_results.csv")

def load_data():
    if not os.path.exists(RESULTS_FILE):
        return None
    df = pd.read_csv(RESULTS_FILE)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df

def compute_metrics(df):
    def safe_div(a, b):
        return a / b.replace(0, float("nan"))
    df["IPC_core"] = safe_div(df["cpu_core/instructions"], df["cpu_core/cycles"])
    df["IPC_atom"] = safe_div(df["cpu_atom/instructions"], df["cpu_atom/cycles"])
    df["CacheMissRate_core"] = safe_div(df["cpu_core/cache-misses"], df["cpu_core/cache-references"])
    df["CacheMissRate_atom"] = safe_div(df["cpu_atom/cache-misses"], df["cpu_atom/cache-references"])
    df["BranchMissRate_core"] = safe_div(df["cpu_core/branch-misses"], df["cpu_core/branch-instructions"])
    df["BranchMissRate_atom"] = safe_div(df["cpu_atom/branch-misses"], df["cpu_atom/branch-instructions"])
    return df

def plot_metrics(df):
    output_dir = "../results/matplotlib_graphs"
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10,6))
    plt.plot(df["timestamp"], df["IPC_core"], label="Core IPC")
    plt.plot(df["timestamp"], df["IPC_atom"], label="Atom IPC")
    plt.xticks(rotation=45)
    plt.ylabel("Instructions per Cycle (IPC)")
    plt.title("Atom vs Core IPC over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "ipc_trend.png"))
    plt.close()

    plt.figure(figsize=(10,6))
    plt.plot(df["timestamp"], df["CacheMissRate_core"], label="Core Cache Miss Rate")
    plt.plot(df["timestamp"], df["CacheMissRate_atom"], label="Atom Cache Miss Rate")
    plt.xticks(rotation=45)
    plt.ylabel("Cache Miss Rate")
    plt.title("Cache Miss Rate over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "cache_miss_trend.png"))
    plt.close()

    plt.figure(figsize=(10,6))
    plt.plot(df["timestamp"], df["BranchMissRate_core"], label="Core Branch Miss Rate")
    plt.plot(df["timestamp"], df["BranchMissRate_atom"], label="Atom Branch Miss Rate")
    plt.xticks(rotation=45)
    plt.ylabel("Branch Misprediction Rate")
    plt.title("Branch Misprediction Rate over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "branch_miss_trend.png"))
    plt.close()

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        df = compute_metrics(df)
        plot_metrics(df)
