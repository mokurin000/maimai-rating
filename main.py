import seaborn as sns
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
import pandas as pd

# Set Decimal precision
getcontext().prec = 28

# Constants (same as above)
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
difficulties = [Decimal(str(round(8.0 + i * 0.1, 1))) for i in range(71)]

# Prepare data for seaborn
data = []
for diff in difficulties:
    for rank in ranks:
        min_rating = dx_rating(diff, rank["min_ach"])
        max_rating = dx_rating(diff, rank["max_ach"])
        mid = (min_rating + max_rating) / 2
        # Add data points for boxplot
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

# Plot using seaborn
plt.figure(figsize=(15, 8))
sns.boxplot(
    x="Difficulty",
    y="Rating",
    hue="Rank",
    data=df[df["Type"].isin(["Min", "Max"])],
    dodge=False,  # Disable dodging to place all ranks on the same vertical line
)
plt.title("DX Rating Distribution by Difficulty and Rank")
plt.xlabel("Difficulty")
plt.ylabel("DX Rating")
plt.xticks(
    rotation=45,
    ticks=range(0, len(difficulties), 5),
    labels=[str(diff) for diff in difficulties[::5]],
)
plt.legend(title="Rank")
plt.tight_layout()
plt.show()
