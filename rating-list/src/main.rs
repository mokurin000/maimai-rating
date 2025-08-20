use rating_list::get_rating;

fn main() {
    println!("target_rating,rank,achievement,difficulty");
    for target_total_rating in 1..=33 {
        let target_rating = target_total_rating * 10;
        let pairs = get_rating(target_rating);
        for (rank, difficulty, achievement) in pairs {
            println!("{target_rating},{rank},{achievement},{difficulty}",);
        }
    }
}
