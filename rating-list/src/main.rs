use std::fs::OpenOptions;
use std::io::{BufWriter, Write};

use rating_list::get_rating;
use rayon::iter::IntoParallelIterator;
use rayon::iter::ParallelIterator;

fn main() -> std::io::Result<()> {
    write_file((10..=330).step_by(10), false, "../rating_table.csv")?;
    write_file((10..=330).step_by(10), true, "../rating_table_simple.csv")?;

    write_file((2..=330).step_by(2), false, "../rating_table_2.csv")?;
    write_file((2..=330).step_by(2), true, "../rating_table_simple_2.csv")?;

    write_file(1..=330, false, "../rating_table_1.csv")?;
    write_file(1..=330, true, "../rating_table_simple_1.csv")?;
    Ok(())
}

fn write_file(
    ratings: impl Iterator<Item = u32>,
    simple: bool,
    filename: &str,
) -> std::io::Result<()> {
    let file = OpenOptions::new().write(true).create(true).open(filename)?;
    let mut file = BufWriter::new(file);
    writeln!(&mut file, "target_rating,rank,achievement,difficulty")?;
    file.write(
        ratings
            .collect::<Vec<u32>>()
            .into_par_iter()
            .map(|rating| {
                let pairs = get_rating(rating as _, simple);
                pairs
                    .into_par_iter()
                    .map(|(rank, difficulty, achievement)| {
                        format!("{rating},{rank},{achievement},{difficulty}\n")
                    })
                    .collect::<String>()
            })
            .collect::<String>()
            .as_bytes(),
    )?;

    Ok(())
}
