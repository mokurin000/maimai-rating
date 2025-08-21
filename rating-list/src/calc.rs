use std::ops::RangeInclusive;

use rust_decimal::{Decimal, dec};

pub fn dx_rating(difficulty_rank: Decimal, achievement: i32) -> (&'static str, u32) {
    let (rank, _, factor) = RANKS
        .into_iter()
        .rev()
        .find(|(_, threshold, _)| threshold.contains(&achievement))
        .unwrap(); // save here, due to zero threshold
    let achievement = Decimal::new(achievement as _, 4);

    // when ach > 100.5%, calculate as 100.5%
    let rating: u32 = (factor * difficulty_rank * achievement)
        .floor()
        .try_into()
        .unwrap_or_default();

    (rank, rating)
}

pub const RANKS: [(&'static str, RangeInclusive<i32>, Decimal); 23] = [
    ("D", 0..=99999, dec!(0.0)),
    ("D", 100000..=199999, dec!(0.016)),
    ("D", 200000..=299999, dec!(0.032)),
    ("D", 300000..=399999, dec!(0.048)),
    ("D", 400000..=499999, dec!(0.064)),
    ("C", 500000..=599999, dec!(0.080)),
    ("B", 600000..=699999, dec!(0.096)),
    ("BB", 700000..=749999, dec!(0.112)),
    ("BBB", 750000..=799998, dec!(0.120)),
    ("BBB*", 799999..=799999, dec!(0.128)),
    ("A", 800000..=899999, dec!(0.136)),
    ("AA", 900000..=939999, dec!(0.152)),
    ("AAA", 940000..=969998, dec!(0.168)),
    ("AAA*", 969999..=969999, dec!(0.176)),
    ("S", 970000..=979999, dec!(0.200)),
    ("S+", 980000..=989998, dec!(0.203)),
    ("S+*", 989999..=989999, dec!(0.206)),
    ("SS", 990000..=994999, dec!(0.208)),
    ("SS+", 995000..=999998, dec!(0.211)),
    ("SS+*", 999999..=999999, dec!(0.214)),
    ("SSS", 1000000..=1004998, dec!(0.216)),
    ("SSS*", 1004999..=1004999, dec!(0.222)),
    ("SSS+", 1005000..=1005000, dec!(0.224)),
];
