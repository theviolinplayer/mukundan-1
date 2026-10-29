// core/src/smt.rs
// MUKUNDAN 1: Sparse Merkle Tree for BB(6) Tape Arithmetization
// Optimized for WebAssembly Heap Limits and Noir ZK Compatibility

use rustc_hash::FxHashMap;
use serde::{Serialize, Deserialize};
use crate::hash::{poseidon_hash_2, fr_from_u8_array, u8_array_from_fr};

pub type FieldElement = [u8; 32];

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct MerkleInclusionProof {
    pub symbol: u8,
    pub index: u64,
    pub siblings: Vec<FieldElement>, // Will always be length 64 for this SMT
}

pub struct TapeMerkleTree {
    pub depth: usize,
    // Maps (level, index) -> Poseidon Hash. Uses FxHashMap to save CPU cycles in the browser.
    nodes: FxHashMap<(usize, u64), FieldElement>,
    // Precomputed hashes of empty subtrees (level 0 to 64)
    zero_hashes: Vec<FieldElement>,
    // Fast-access state of the actual tape symbols (to avoid inverse-hashing leaves)
    tape_memory: FxHashMap<u64, u8>,
}

impl TapeMerkleTree {
    /// Initializes a Sparse Merkle Tree of depth 64 (Max cells: 2^64)
    pub fn new() -> Self {
        let depth = 64;
        let mut zero_hashes = Vec::with_capacity(depth + 1);
        
        // Level 0 Zero Hash (Leaf representing tape symbol '0')
        // In Noir, a '0' is usually a 32-byte array of zeroes.
        let mut current_zero = [0u8; 32];
        zero_hashes.push(current_zero);

        // Precompute the Zero Hashes for all levels up to the root
        for _ in 1..=depth {
            current_zero = Self::poseidon_hash(&current_zero, &current_zero);
            zero_hashes.push(current_zero);
        }

        TapeMerkleTree {
            depth,
            nodes: FxHashMap::default(),
            zero_hashes,
            tape_memory: FxHashMap::default(),
        }
    }

    /// Reads a symbol from the tape and generates the cryptographic ZK-witness
    pub fn read_and_prove(&self, index: u64) -> MerkleInclusionProof {
        let symbol = *self.tape_memory.get(&index).unwrap_or(&0);
        let mut siblings = Vec::with_capacity(self.depth);
        let mut curr_index = index;

        // Traverse from leaf (level 0) to root (level 64)
        for level in 0..self.depth {
            // Bitwise XOR with 1 flips the least significant bit, yielding the sibling index
            let sibling_index = curr_index ^ 1;
            
            let sibling_hash = self.nodes
                .get(&(level, sibling_index))
                .copied()
                .unwrap_or(self.zero_hashes[level]);
                
            siblings.push(sibling_hash);
            
            // Move up to the parent node
            curr_index >>= 1;
        }

        MerkleInclusionProof {
            symbol,
            index,
            siblings,
        }
    }

    /// Writes a symbol, recalculates the modified branch, and returns the new Root Hash
    pub fn write_symbol(&mut self, index: u64, symbol: u8) -> FieldElement {
        // Update raw memory
        self.tape_memory.insert(index, symbol);

        // Define the new leaf hash (padding the u8 to a 32-byte Field Element)
        let mut current_hash = [0u8; 32];
        current_hash[31] = symbol; // Big-endian representation for Noir compatibility
        
        let mut curr_index = index;

        // Traverse up, recalculating hashes
        for level in 0..self.depth {
            // Store the current node
            self.nodes.insert((level, curr_index), current_hash);

            let sibling_index = curr_index ^ 1;
            let sibling_hash = self.nodes
                .get(&(level, sibling_index))
                .copied()
                .unwrap_or(self.zero_hashes[level]);

            // ORIENTATION LOCK: 
            // If curr_index is even (curr_index & 1 == 0), it is the Left child.
            // If curr_index is odd, it is the Right child.
            // Poseidon is permutation-sensitive. This order is non-negotiable.
            if curr_index & 1 == 0 {
                current_hash = Self::poseidon_hash(&current_hash, &sibling_hash);
            } else {
                current_hash = Self::poseidon_hash(&sibling_hash, &current_hash);
            }

            curr_index >>= 1;
        }

        // Store and return the final Root Hash (Level 64, Index 0)
        self.nodes.insert((self.depth, 0), current_hash);
        current_hash
    }

    /// Fetches the current root hash of the entire tape
    pub fn root(&self) -> FieldElement {
        self.nodes.get(&(self.depth, 0)).copied().unwrap_or(self.zero_hashes[self.depth])
    }

    /// SNARK-friendly Hash Function Binding
    fn poseidon_hash(left: &FieldElement, right: &FieldElement) -> FieldElement {
        let left_fr = fr_from_u8_array(left);
        let right_fr = fr_from_u8_array(right);
        let result = poseidon_hash_2(left_fr, right_fr);
        u8_array_from_fr(result)
    }
}