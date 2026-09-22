"""Build the fixed-marker supplier risk and exposure matrix used in the README."""

from pathlib import Path
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("MPLBACKEND", "Agg")


def main() -> None:
    table = pd.read_csv(ROOT / "results" / "supplier_decision_table.csv")
    table["observed_value_m"] = table["line_value_usd"] / 1_000_000

    colors = {
        "DIVERSIFY": "#d85b2a",
        "DEVELOP": "#1e6f6a",
        "RENEGOTIATE": "#c9952d",
        "PROTECT": "#80909e",
    }
    label_offsets = {
        "Supplier 07": (7, -8),
        "Supplier 09": (7, 12),
        "Supplier 14": (7, -10),
        "Supplier 22": (7, -8),
        "Supplier 24": (7, 12),
    }

    fig, ax = plt.subplots(figsize=(11, 6.5), facecolor="white")
    for action, group in table.groupby("action", sort=False):
        ax.scatter(
            group["observable_risk_score"],
            group["observed_value_m"],
            s=135,
            color=colors[action],
            edgecolor="white",
            linewidth=1.4,
            label=action.title(),
            zorder=3,
        )

    for _, row in table.iterrows():
        dx, dy = label_offsets.get(row["supplier_alias"], (7, 7))
        ax.annotate(
            row["supplier_alias"],
            (row["observable_risk_score"], row["observed_value_m"]),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=9,
            color="#23313b",
        )

    ax.set_xlim(0, 82)
    ax.set_xlabel("Observable risk score (0–100)", fontsize=11)
    ax.set_ylabel("Observed line-item value (USD, millions)", fontsize=11)
    fig.suptitle("Where exposure and risk intersect", x=0.125, y=0.98, ha="left", fontsize=15, weight="bold")
    fig.text(0.125, 0.935, "Each point represents one anonymized supplier.", color="#5b6770", fontsize=9.5)
    ax.grid(axis="y", color="#dce3e7", linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(frameon=False, title="Review path", ncols=4, loc="upper left", bbox_to_anchor=(0, -0.15))
    fig.subplots_adjust(left=0.10, right=0.98, top=0.84, bottom=0.20)
    fig.savefig(ROOT / "visuals" / "supplier_exposure_matrix.png", dpi=180, bbox_inches="tight")
    print("Wrote visuals/supplier_exposure_matrix.png")


if __name__ == "__main__":
    main()
