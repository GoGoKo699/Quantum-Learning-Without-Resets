#!/usr/bin/env python3
"""Reproduce Fig. 2(a): proved envelopes, not a fitted optimal-signal curve.

Run from any directory. Output defaults to signal_bounds.pdf beside this generator.
The only inputs are the two universal bounds in science/protocols.md (A1).
"""
from pathlib import Path
import argparse
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, LogFormatterMathtext


def main():
    default = Path(__file__).resolve().parent / "signal_bounds.pdf"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=default)
    args = parser.parse_args()
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.linewidth": 0.7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.facecolor": "white",
    })
    navy, teal = "#163754", "#217E82"
    # Include both analytical breakpoints exactly, avoiding interpolation artifacts.
    z = np.unique(np.r_[np.logspace(-4, 3, 1201), 1.0, 2.0])
    lower = np.minimum(1.0, z) / 128.0
    upper = np.minimum(1.0, z / 2.0)
    assert np.all(lower <= upper)
    assert lower[np.flatnonzero(z == 1.0)[0]] == 1.0 / 128.0
    assert upper[np.flatnonzero(z == 2.0)[0]] == 1.0

    fig, ax = plt.subplots(figsize=(6.9, 2.8))
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.215, top=0.89)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.fill_between(z, lower, upper, color=teal, alpha=0.15, linewidth=0)
    ax.plot(z, upper, color=navy, lw=1.65, label=r"Converse $U(z)=\min\{1,z/2\}$")
    ax.plot(z, lower, color=teal, lw=1.65, ls=(0, (4, 2.5)),
            label=r"Finite protocols $L(z)=\min\{1,z\}/128$")
    ax.axvline(1.0, color="0.5", lw=0.8, ls=(0, (1.5, 2.5)), zorder=0)
    ax.set_xlim(1e-4, 1e3)
    ax.set_ylim(4e-7, 1.9)
    ax.set_xticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_locator(LogLocator(base=10, numticks=8))
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.minorticks_off()
    ax.grid(axis="y", color="0.9", linewidth=0.45)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel(r"Rescaled retention $z=\lambda/[M(1-\lambda)]$", labelpad=3)
    ax.set_ylabel(r"One-clean-qubit signal $\Delta_1$", labelpad=4)
    ax.set_title(r"(a) Proved envelopes for $0<\lambda<1$", loc="left", fontsize=11, pad=8)
    ax.legend(loc="upper left", bbox_to_anchor=(0.015, 1.015), frameon=False,
              fontsize=9, handlelength=2.5, labelspacing=0.4)
    ax.text(12, 0.075, "Rigorous interval\nfor the optimum", color=navy,
            fontsize=10, ha="left", va="center")
    ax.annotate(r"Near-conservation crossover" + "\n" + r"$1-\lambda\asymp M^{-1}$",
                xy=(1, 0.0025), xycoords="data", xytext=(0.51, 0.16),
                textcoords="axes fraction", fontsize=9, ha="center", va="bottom",
                arrowprops=dict(arrowstyle="-", color="0.4", lw=0.7))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, metadata={
        "Title": "Rigorous one-clean-qubit signal envelopes",
        "Author": "",
        "Subject": "Analytic upper and lower bounds; no simulated or fitted optimum",
        "CreationDate": None,
        "ModDate": None,
    })
    plt.close(fig)
    print(args.output)


if __name__ == "__main__":
    main()
