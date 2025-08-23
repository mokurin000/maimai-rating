use std::fs::OpenOptions;
use std::io::{BufWriter, Write};

use rating_list::get_rating;

fn main() -> std::io::Result<()> {
    write_file((10..=330).step_by(10), false, "rating_table.csv")?;
    write_file((10..=330).step_by(10), true, "rating_table_simple.csv")?;
    write_file((2..=330).step_by(2), true, "rating_table_simple_2.csv")?;
    Ok(())
}

fn write_file(
    ratings: impl IntoIterator<Item = u32>,
    simple: bool,
    filename: &str,
) -> std::io::Result<()> {
    let file = OpenOptions::new().write(true).create(true).open(filename)?;
    let mut file = BufWriter::new(file);
    writeln!(&mut file, "target_rating,rank,achievement,difficulty")?;
    for target_rating in ratings {
        let pairs = get_rating(target_rating, simple);
        for (rank, difficulty, achievement) in pairs {
            writeln!(
                &mut file,
                "{target_rating},{rank},{achievement},{difficulty}",
            )?;
        }
    }

    Ok(())
}
