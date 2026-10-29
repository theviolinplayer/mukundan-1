mod memory;

struct TapeState {
    state: Field,
    head_symbol: Field,
    left_tape_hash: Field,
    right_tape_hash: Field,
    steps_accumulated: Field,
}



fn main(
    current_state: pub TapeState, 
    next_state: pub TapeState,
    transition_write: Field,
    transition_next_move: Field, 
    transition_next_state: Field,
    tnf_merkle_root: pub Field,
    tnf_merkle_path: [Field; 4],
    compressed_block_count: Field,
    prev_left_tape_preimage: [Field; 2],
    prev_right_tape_preimage: [Field; 2]
) {
    let leaf_hash = std::hash::poseidon::bn254::hash_5([
        current_state.state, 
        current_state.head_symbol, 
        transition_write, 
        transition_next_move, 
        transition_next_state
    ]);

    let mut current_hash = leaf_hash;
    let mut current_index = current_state.state as u32 * 2 + current_state.head_symbol as u32;
    for i in 0..4 {
        let is_right = current_index & 1;
        if is_right == 1 {
            current_hash = std::hash::poseidon::bn254::hash_2([tnf_merkle_path[i], current_hash]);
        } else {
            current_hash = std::hash::poseidon::bn254::hash_2([current_hash, tnf_merkle_path[i]]);
        }
        current_index >>= 1;
    }
    assert(current_hash == tnf_merkle_root);
    
    assert(next_state.steps_accumulated == current_state.steps_accumulated + compressed_block_count);
    let is_state_change = current_state.state != transition_next_state;
    if is_state_change {
        assert(compressed_block_count == 1);
    }

    if transition_next_move == 1 {
        memory::check_tape_push(
            transition_write,
            compressed_block_count,
            current_state.left_tape_hash,
            next_state.left_tape_hash
        );
        
        memory::check_tape_pop(
            current_state.head_symbol,
            compressed_block_count,
            next_state.right_tape_hash,
            current_state.right_tape_hash
        );

        assert(prev_right_tape_preimage[0] == current_state.head_symbol);
        assert(prev_right_tape_preimage[1] == compressed_block_count);
    } else {
        memory::check_tape_push(
            transition_write,
            compressed_block_count,
            current_state.right_tape_hash,
            next_state.right_tape_hash
        );

        memory::check_tape_pop(
            current_state.head_symbol,
            compressed_block_count,
            next_state.left_tape_hash,
            current_state.left_tape_hash
        );

        assert(prev_left_tape_preimage[0] == current_state.head_symbol);
        assert(prev_left_tape_preimage[1] == compressed_block_count);
    }
    
    assert(next_state.state == transition_next_state);
}