#![feature(new_range_api)]

use std::range::RangeInclusive;

use rust_decimal::Decimal;

use calc::dx_rating;

use crate::calc::{RANKS, RANKS_SIMPLE};
mod calc;

pub fn get_rating(target_rating: u32, simple: bool) -> Vec<(&'static str, Decimal, i32)> {
    let mut results = Vec::new();
    let mut last_difficulty = None;
    for (rank, current_ach, _) in if simple {
        RANKS_SIMPLE.as_ref()
    } else {
        RANKS.as_ref()
    } {
        let current_ach: RangeInclusive<i32> = current_ach.clone().into();

        for difficulty_rank in (10..=150).map(|num| Decimal::new(num, 1)) {
            let (_, rating) = dx_rating(difficulty_rank, current_ach.end);
            if rating < target_rating {
                continue;
            }

            if last_difficulty == Some(difficulty_rank) {
                break;
            }

            let minimum_ach = current_ach
                .into_iter()
                .find(|achievement| dx_rating(difficulty_rank, *achievement).1 >= target_rating)
                .unwrap();
            results.push((*rank, difficulty_rank, minimum_ach));
            last_difficulty = Some(difficulty_rank);
            break;
        }
    }

    results
}
