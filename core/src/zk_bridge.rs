use std::fs;
use crate::machine::{Machine, Move};
use num_bigint::BigUint;

pub fn generate_prover_toml(
    state_in: u8,
    left_hash_in: &str,
    right_hash_in: &str,
    state_out: u8,
    left_hash_out: &str,
    right_hash_out: &str,
    machine: &Machine,
    read_sym: u8,
    read_count: &BigUint,
    underlying_right: &str,
    write_sym: u8,
    write_count: &BigUint,
    move_dir: u8,
) {
    let mut rule_next = Vec::new();
    let mut rule_write = Vec::new();
    let mut rule_move = Vec::new();

    for s in 0..6 {
        for sym in 0..2 {
            if let Some(t) = &machine.transitions[s][sym] {
                rule_next.push(format!("\"{}\"", t.next_state));
                rule_write.push(format!("\"{}\"", t.write));
                let m = match t.next_move {
                    Move::Left => 0,
                    Move::Right => 1,
                };
                rule_move.push(format!("\"{}\"", m));
            } else {
                rule_next.push("\"0\"".to_string());
                rule_write.push("\"0\"".to_string());
                rule_move.push("\"0\"".to_string());
            }
        }
    }

    let toml = format!(
        "state_in = \"{}\"\n\
        left_hash_in = \"{}\"\n\
        right_hash_in = \"{}\"\n\
        state_out = \"{}\"\n\
        left_hash_out = \"{}\"\n\
        right_hash_out = \"{}\"\n\
        rule_next_state = [{}]\n\
        rule_write_symbol = [{}]\n\
        rule_move_dir = [{}]\n\
        underlying_right_hash = \"{}\"\n\
        move_dir = \"{}\"\n\n\
        [read_block]\n\
        symbol = \"{}\"\n\
        count = \"{}\"\n\n\
        [written_block]\n\
        symbol = \"{}\"\n\
        count = \"{}\"\n",
        state_in, left_hash_in, right_hash_in,
        state_out, left_hash_out, right_hash_out,
        rule_next.join(", "), rule_write.join(", "), rule_move.join(", "),
        underlying_right, move_dir,
        read_sym, read_count,
        write_sym, write_count
    );

    fs::write("../circuits/Prover.toml", toml).unwrap();
}