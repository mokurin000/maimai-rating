from decimal import Decimal

import matplotlib.pyplot as plt

from common import df, difficulties

df["Difficulty"] = df["Difficulty"].astype(float)

# Assuming df is your original DataFrame with "Difficulty", "Rank", "Type", and "Rating"
# Group data to get min and max ratings for each Difficulty and Rank
df_grouped = (
    df.groupby(["Difficulty", "Rank"]).agg({"Rating": ["min", "max"]}).reset_index()
)
df_grouped.columns = ["Difficulty", "Rank", "Min", "Max"]

# Create figure and axes
fig, ax = plt.subplots(figsize=(16, 8))

# Get unique difficulties and assign x-positions
difficulties_uniq = df_grouped["Difficulty"].unique()
x_pos = range(len(difficulties_uniq))

# Plot bars for each rank at each difficulty
for rank in df_grouped["Rank"].unique():
    rank_data = df_grouped[df_grouped["Rank"] == rank]
    min_ratings = rank_data["Min"]
    max_ratings = rank_data["Max"]
    heights = max_ratings - min_ratings
    ax.bar(x_pos, heights, bottom=min_ratings, label=rank, alpha=0.5, width=0.8)

# Customize plot
ax.set_xticks(x_pos[::5])  # Show every 5th tick for readability
ax.set_xticklabels(difficulties_uniq[::5], rotation=45)
ax.set_xlabel("Difficulty")
ax.set_ylabel("DX Rating")
ax.set_title("DX Ratings by Difficulty and Rank")
ax.legend(title="Rank")

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

plt.tight_layout()
plt.show()
