import polars as pl

pl.Config.set_tbl_rows(-1)

df = (
    pl.scan_csv(
        "rating_table.csv",
        schema={
            "target_rating": pl.Int32,
            "rank": pl.String,
            "achievement": pl.Int32,
            "difficulty": pl.String,
        },
    )
    .with_columns(
        pl.col("difficulty").cast(pl.Float64),
    )
    .filter(
        pl.lit("ABS").str.contains(
            pl.col("rank").str.head(1),
        )
    )
)

df.collect().plot.scatter(
    x="difficulty",
    y="target_rating",
    color="rank",
    size="achievement",
).properties(
    width=1600,
    height=1000,
).save("rating.html")

df.filter(pl.col("rank").str.contains(r"\*").not_()).collect().plot.scatter(
    x="difficulty",
    y="target_rating",
    color="rank",
    size="achievement",
).properties(
    width=1600,
    height=1000,
).save("rating-simplified.html")
