"""Plot project DeepRMSA-FLX and SP-FF/KSP-FF curves for paper Fig. 7."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent


def read_csv_curve(name):
    with (ROOT / name).open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    return (
        [int(row["requests_simulated"]) for row in rows],
        [float(row["blocking_probability"]) for row in rows],
    )


def read_deep_curve():
    episode_values = [
        float(line.strip())
        for line in (ROOT / "BP.dat").read_text().splitlines()
        if line.strip()
    ]
    # BP.dat stores one value per 1,000-request episode. Aggregate every ten
    # episodes to match the baseline's 10,000-request sampling interval.
    values = [
        sum(episode_values[start:start + 10]) / 10.0
        for start in range(0, len(episode_values) - 9, 10)
    ]
    return [10_000 * idx for idx in range(1, len(values) + 1)], values


def main():
    deep_x, deep_y = read_deep_curve()
    is_partial = not deep_x or deep_x[-1] < 5_000_000
    figure, axis = plt.subplots(figsize=(8.2, 4.8))
    deep_label = "DeepRMSA-FLX (project"
    if is_partial:
        deep_label += ", in progress"
    deep_label += ")"
    for filename, label, color in (
        (None, deep_label, "tab:blue"),
        ("sp_ff_curve.csv", "SP-FF", "tab:orange"),
        ("ksp_ff_curve.csv", "KSP-FF", "tab:red"),
    ):
        if filename is None:
            x_values, y_values = deep_x, deep_y
        else:
            x_values, y_values = read_csv_curve(filename)
        axis.plot(x_values, y_values, label=label, color=color, linewidth=1.2)

    axis.set_xlabel("Number of requests simulated")
    axis.set_ylabel("Blocking probability")
    if is_partial:
        axis.set_title("Partial Fig. 7 replot: DeepRMSA-FLX run in progress")
    else:
        axis.set_title("Fig. 7 replot: DeepRMSA-FLX, SP-FF and KSP-FF")
    axis.grid(True, alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(ROOT / "fig7_reproduction_partial.png", dpi=180)
    print("Saved fig7_reproduction_partial.png")


if __name__ == "__main__":
    main()
