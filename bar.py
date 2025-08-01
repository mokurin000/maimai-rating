import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
import pandas as pd

# Set Decimal precision
getcontext().prec = 28

# Constants
SSS_PLUS_THRESHOLD = Decimal("100.5")
SSS_PLUS_FACTOR = Decimal("0.224")
SSS_THRESHOLD = Decimal("100.0")
SSS_FACTOR = Decimal("0.216")
SS_PLUS_THRESHOLD = Decimal("99.5")
SS_PLUS_FACTOR = Decimal("0.211")
SS_THRESHOLD = Decimal("99.0")
SS_FACTOR = Decimal("0.208")
S_PLUS_THRESHOLD = Decimal("98.0")
S_PLUS_FACTOR = Decimal("0.203")
S_THRESHOLD = Decimal("97.0")
S_FACTOR = Decimal("0.2")
AAA_THRESHOLD = Decimal("94.0")
AAA_FACTOR = Decimal("0.168")
AA_THRESHOLD = Decimal("90.0")
AA_FACTOR = Decimal("0.152")
A_THRESHOLD = Decimal("80.0")
A_FACTOR = Decimal("0.136")


def dx_rating(difficulty: Decimal, achievement: int) -> int:
    ach = Decimal(achievement) / Decimal("10000")
    if ach >= Decimal("101.0") or ach < A_THRESHOLD:
        return 0
    if ach >= SSS_PLUS_THRESHOLD:
        factor = SSS_PLUS_FACTOR
    elif ach >= SSS_THRESHOLD:
        factor = SSS_FACTOR
    elif ach >= SS_PLUS_THRESHOLD:
        factor = SS_PLUS_FACTOR
    elif ach >= SS_THRESHOLD:
        factor = SS_FACTOR
    elif ach >= S_PLUS_THRESHOLD:
        factor = S_PLUS_FACTOR
    elif ach >= S_THRESHOLD:
        factor = S_FACTOR
    elif ach >= AAA_THRESHOLD:
        factor = AAA_FACTOR
    elif ach >= AA_THRESHOLD:
        factor = AA_FACTOR
    elif ach >= A_THRESHOLD:
        factor = A_FACTOR
    else:
        return 0
    result = (factor * difficulty * ach).quantize(Decimal("1."), rounding="ROUND_FLOOR")
    return int(result)


# Define ranks
ranks = [
    {"name": "SSS+", "min_ach": 1005000, "max_ach": 1009999},
    {"name": "SSS", "min_ach": 1000000, "max_ach": 1004999},
    {"name": "SS+", "min_ach": 995000, "max_ach": 999999},
    {"name": "SS", "min_ach": 990000, "max_ach": 994999},
    {"name": "S+", "min_ach": 980000, "max_ach": 989999},
    {"name": "S", "min_ach": 970000, "max_ach": 979999},
    {"name": "AAA", "min_ach": 940000, "max_ach": 969999},
    {"name": "AA", "min_ach": 900000, "max_ach": 939999},
    {"name": "A", "min_ach": 800000, "max_ach": 899999},
]

# Generate difficulty levels
difficulties_dec = [Decimal(f"{8 + i // 10}.{i % 10}") for i in range(71)]

# Prepare data for seaborn
data = []
for diff in difficulties_dec:
    for rank in ranks:
        min_rating = dx_rating(diff, rank["min_ach"])
        max_rating = dx_rating(diff, rank["max_ach"])
        mid = (min_rating + max_rating) / 2
        data.append(
            {
                "Difficulty": str(diff),
                "Rank": rank["name"],
                "Rating": min_rating,
                "Type": "Min",
            }
        )
        data.append(
            {
                "Difficulty": str(diff),
                "Rank": rank["name"],
                "Rating": max_rating,
                "Type": "Max",
            }
        )
        data.append(
            {
                "Difficulty": str(diff),
                "Rank": rank["name"],
                "Rating": mid,
                "Type": "Mid",
            }
        )

# Convert to DataFrame
df = pd.DataFrame(data)
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
difficulties= df_grouped["Difficulty"].unique()
x_pos = range(len(difficulties))

# Plot bars for each rank at each difficulty
for rank in df_grouped["Rank"].unique():
    rank_data = df_grouped[df_grouped["Rank"] == rank]
    min_ratings = rank_data["Min"]
    max_ratings = rank_data["Max"]
    heights = max_ratings - min_ratings
    ax.bar(x_pos, heights, bottom=min_ratings, label=rank, alpha=0.5, width=0.8)

# Customize plot
ax.set_xticks(x_pos[::5])  # Show every 5th tick for readability
ax.set_xticklabels(difficulties[::5], rotation=45)
ax.set_xlabel("Difficulty")
ax.set_ylabel("DX Rating")
ax.set_title("DX Ratings by Difficulty and Rank")
ax.legend(title="Rank")

for rating in [15000, 14000, 13000, 12000, 11000, 10000]:
    ax.axhline(rating // 50, color="gray", linestyle="--", alpha=0.3)

for diff in difficulties_dec:
    if (diff * 2).as_integer_ratio()[1] == 1:
        d = int((diff - 8) / Decimal("0.5") * 5)
        ax.axvline(x=d, color="gray", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()
