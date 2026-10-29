use ark_bn254::Fr;
use crate::hash::{poseidon_hash_2, poseidon_hash_5};
use crate::machine::{Machine, Move};

pub struct TnfTree {
    pub leaves: [Fr; 16],
    pub tree: [[Fr; 16]; 5], // Level 0 is leaves, Level 4 is root
}

impl TnfTree {
    pub fn new(machine: &Machine) -> Self {
        let mut leaves = [Fr::from(0u32); 16];
        for s in 0..6 {
            for sym in 0..2 {
                let idx = s * 2 + sym;
                if let Some(t) = &machine.transitions[s as usize][sym as usize] {
                    let st = Fr::from(s as u32);
                    let rd = Fr::from(sym as u32);
                    let wr = Fr::from(t.write as u32);
                    let mv = match t.next_move { Move::Left => Fr::from(0u32), Move::Right => Fr::from(1u32) };
                    let nx = Fr::from(if t.next_state < 0 { 0 } else { t.next_state as u32 });
                    leaves[idx as usize] = poseidon_hash_5(st, rd, wr, mv, nx);
                }
            }
        }
        
        let mut tree = [[Fr::from(0u32); 16]; 5];
        tree[0] = leaves;
        
        for level in 1..=4 {
            let num_nodes = 16 >> level;
            for i in 0..num_nodes {
                let left = tree[level - 1][i * 2];
                let right = tree[level - 1][i * 2 + 1];
                tree[level][i] = poseidon_hash_2(left, right);
            }
        }
        
        Self { leaves, tree }
    }
    
    pub fn root(&self) -> Fr {
        self.tree[4][0]
    }
    
    pub fn get_path(&self, state: usize, symbol: usize) -> [Fr; 4] {
        let mut idx = state * 2 + symbol;
        let mut path = [Fr::from(0u32); 4];
        
        for level in 0..4 {
            let sibling_idx = idx ^ 1;
            path[level] = self.tree[level][sibling_idx];
            idx >>= 1;
        }
        path
    }
}
