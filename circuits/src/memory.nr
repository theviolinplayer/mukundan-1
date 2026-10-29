// Memory argument helpers for tape multiset checks
// The tape hashes are accumulated using Pedersen hashes, which acts as a succinct memory checking argument.

pub fn check_tape_push(
    symbol: Field,
    count: Field,
    prev_hash: Field,
    expected_hash: Field
) {
    let computed_hash = std::hash::poseidon::bn254::hash_3([symbol, count, prev_hash]);
    assert(computed_hash == expected_hash);
}

pub fn check_tape_pop(
    symbol: Field,
    count: Field,
    next_hash: Field,
    expected_hash: Field
) {
    if expected_hash == 0 {
        assert(symbol == 0);
        assert(next_hash == 0);
    } else {
        let computed_hash = std::hash::poseidon::bn254::hash_3([symbol, count, next_hash]);
        assert(computed_hash == expected_hash);
    }
}
