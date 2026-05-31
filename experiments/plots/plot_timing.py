import matplotlib.pyplot as plt


def plot_times(sizes, times, path="timing_plot.png"):
    plt.figure(figsize=(6, 4))
    plt.plot(sizes, times, marker="o")
    plt.xlabel("number of qubits")
    plt.ylabel("seconds")
    plt.title("Transfer matrix evaluation timing")
    plt.grid(True)
    plt.savefig(path)
    print(f"Saved timing plot to {path}")
