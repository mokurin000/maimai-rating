import polars as pl

pl.Config.set_tbl_rows(-1)


def draw_chart(csv_file: str, html_file: str, filter: str = "ABS"):
    df = (
        pl.scan_csv(
            csv_file,
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
            pl.lit(filter).str.contains(
                pl.col("rank").str.head(1),
            )
        )
        .unique(
            subset=[
                pl.col("difficulty"),
                pl.col("achievement"),
            ],
            keep="last",
        )
        .collect()
    )

    df.plot.scatter(
        x="difficulty",
        y="target_rating",
        color="rank",
        size="achievement",
    ).properties(
        width=1600,
        height=1000,
    ).save(html_file)


draw_chart("rating_table.csv", "rating.html", "ABCDS")
draw_chart("rating_table_simple.csv", "rating-simplified.html", "AS")
draw_chart("rating_table_1.csv", "rating-step1.html", "ABCDS")
draw_chart("rating_table_simple_1.csv", "rating-simplified-step1.html", "AS")
draw_chart("rating_table_2.csv", "rating-step2.html", "ABCDS")
draw_chart("rating_table_simple_2.csv", "rating-simplified-step2.html", "AS")
