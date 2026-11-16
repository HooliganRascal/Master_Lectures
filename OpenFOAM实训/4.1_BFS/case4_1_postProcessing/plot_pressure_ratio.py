#!/usr/bin/env python3

import csv
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "case4_1_matplotlib"))

import matplotlib.pyplot as plt


SERIES = (
    ("sonicFoam", "sonicFoam (laminar)", "#0072B2", "o"),
    ("rhoCentralFoam", "rhoCentralFoam (k-epsilon)", "#D55E00", "s"),
    ("rhoPimpleFoam", "rhoPimpleFoam (k-epsilon)", "#009E73", "^"),
)


def read_series(path):
    with path.open(newline="", encoding="ascii") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise RuntimeError("No pressure samples were found in {}".format(path))
    x_inches = [float(row["x_in"]) for row in rows]
    pressure_ratio = [float(row["p_over_p_infinity"]) for row in rows]
    time_s = float(rows[0]["time_s"])
    sample_y = float(rows[0]["y_m"])
    return x_inches, pressure_ratio, time_s, sample_y


def main():
    post_dir = Path(__file__).resolve().parent
    figure, axis = plt.subplots(figsize=(8.2, 4.9), constrained_layout=True)

    times = []
    sample_locations = []
    for file_stem, label, color, marker in SERIES:
        input_path = post_dir / "pressure_ratio_{}.csv".format(file_stem)
        x_inches, pressure_ratio, time_s, sample_y = read_series(input_path)
        times.append(time_s)
        sample_locations.append(sample_y)
        axis.plot(
            x_inches,
            pressure_ratio,
            color=color,
            linewidth=1.7,
            marker=marker,
            markersize=3.5,
            markevery=5,
            label=label,
        )

    if max(times) - min(times) > 1.0e-12:
        raise RuntimeError("The three cases were sampled at different physical times")
    if max(sample_locations) - min(sample_locations) > 1.0e-12:
        raise RuntimeError("The three cases were sampled on different lower cell rows")

    axis.axhline(1.0, color="#666666", linewidth=1.0, linestyle="--", label=r"$p/p_{\infty}=1$")
    axis.set_xlim(0.0, 12.0)
    axis.set_xlabel(r"Distance downstream of step, $x$ (in)")
    axis.set_ylabel(r"Pressure ratio, $p/p_{\infty}$")
    axis.set_title("Case 4.1 pressure along the step extension at $t=3.5$ ms")
    axis.grid(True, color="#D9D9D9", linewidth=0.7)
    axis.set_axisbelow(True)
    axis.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="none", ncol=2, fontsize=8.5)
    axis.text(
        0.015,
        0.98,
        r"$p_{\infty}=15.35$ kPa; lower cell row immediately below $y=0$",
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        color="#4D4D4D",
    )

    output_path = post_dir / "pressure_ratio_comparison.png"
    figure.savefig(output_path, dpi=300, facecolor="white")
    plt.close(figure)
    print("Wrote {}".format(output_path))


if __name__ == "__main__":
    main()
