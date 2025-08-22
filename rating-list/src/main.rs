use std::fs::OpenOptions;
use std::io::Write;

use rating_list::get_rating;

fn main() -> std::io::Result<()> {
    write_file(false, "rating_table.csv")?;
    write_file(true, "rating_table_simple.csv")?;
    Ok(())
}

fn write_file(simple: bool, filename: &str) -> std::io::Result<()> {
    let mut file = OpenOptions::new().write(true).create(true).open(filename)?;
    writeln!(&mut file, "target_rating,rank,achievement,difficulty")?;
    for target_total_rating in 1..=33 {
        let target_rating = target_total_rating * 10;
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
