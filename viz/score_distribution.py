import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── theme ────────────────────────────────────────────────────────────────────
BG      = "#222129"
ACCENT  = "#ffa86a"
FG      = "#ffffff"
MUTED   = "#ffffff26"   # 15% white — subtle gridlines
FONT    = "monospace"

# ── data ─────────────────────────────────────────────────────────────────────
buckets, counts = [], []
with open(ROOT / "data/score_distribution.csv") as f:
    for row in csv.DictReader(f):
        buckets.append(row["score_bucket"])
        counts.append(int(row["story_count"]))

total = sum(counts)
pcts  = [c / total * 100 for c in counts]

# ── plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

bars = ax.bar(buckets, counts, color=ACCENT, width=0.6, zorder=2)

# percentage labels above each bar
for bar, pct in zip(bars, pcts):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 18_000,
        f"{pct:.1f}%",
        ha="center", va="bottom",
        color=FG, fontsize=8, fontfamily=FONT,
    )

# dashed horizontal gridlines — matches site's dashed table borders
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x/1_000_000:.1f}M" if x >= 1_000_000 else f"{int(x/1_000)}K"))
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(axis="y", color=MUTED, linestyle="--", linewidth=0.7, zorder=1)
ax.set_axisbelow(True)

# spines
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(colors=FG, labelsize=9, length=0)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontfamily(FONT)

ax.set_xlabel("score", color=FG, fontfamily=FONT, fontsize=10, labelpad=10)
ax.set_ylabel("stories", color=FG, fontfamily=FONT, fontsize=10, labelpad=10)
ax.set_title("HN story score distribution", color=FG, fontfamily=FONT, fontsize=13, pad=16)

plt.tight_layout()
out = ROOT / "viz/score_distribution.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"saved → {out}")
