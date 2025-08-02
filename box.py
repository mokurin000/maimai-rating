from decimal import Decimal

import seaborn as sns
import matplotlib.pyplot as plt

from common import df, difficulties

# Create figure with extra space on the right
plt.figure(figsize=(16, 8))
ax = sns.boxplot(
    x="Difficulty",
    y="Rating",
    hue="Rank",
    data=df[df["Type"].isin(["Min", "Max"])],
    dodge=False,  # Disable dodging to place all ranks on the same vertical line
)

# Add horizontal reference lines
rating_lines = [
    {"y": 200, "label": "w0"},
    {"y": 220, "label": "w1"},
    {"y": 240, "label": "w2"},
    {"y": 260, "label": "w3"},
    {"y": 280, "label": "w4"},
    {"y": 300, "label": "w5"},
    {"y": 320, "label": "w6"},
]
for line in rating_lines:
    ax.axhline(y=line["y"], color="gray", linestyle="--", alpha=0.3)
    # Place label outside the plot on the right
    ax.text(
        1.02,  # x position in axes fraction (just outside the plot)
        line["y"],
        line["label"],
        transform=ax.get_yaxis_transform(),  # Use y-axis data coordinates
        ha="left",  # Align left to avoid overlap with plot
        va="center",  # Center vertically with the line
        fontsize=10,
    )

for diff in difficulties:
    if (diff * 2).as_integer_ratio()[1] == 1:
        d = int((diff - 9) / Decimal("0.5") * 5)
        ax.axvline(x=d, color="gray", linestyle="--", alpha=0.3)


plt.title("DX Rating Distribution by Difficulty and Rank")
plt.xlabel("Difficulty")
plt.ylabel("DX Rating")
plt.xticks(
    rotation=45,
    ticks=range(0, len(difficulties), 5),
    labels=[str(diff) for diff in difficulties[::5]],
)
plt.legend(title="Rank", loc="upper left")
# Adjust layout to ensure labels are visible
plt.subplots_adjust(right=0.90)  # Leave space on the right for labels
plt.show()
