use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone, Copy, PartialEq, Eq)]
pub enum Move { Left, Right }

#[derive(Serialize, Deserialize, Debug, Clone, Copy, PartialEq, Eq)]
pub struct Transition {
    pub write: u8,
    pub next_move: Move,
    pub next_state: i8, // -1 for Halt
}

pub struct Machine {
    // 6 states, 2 symbols (0 and 1)
    pub transitions: [[Option<Transition>; 2]; 6],
}

impl Machine {
    /// Parses a standard BBChallenge TNF seed (e.g., "1RB1RF_1RC---_1RD1LC_1LE1RF_1LC0LE_1RA0RA")
    pub fn from_tnf(seed: &str) -> Result<Self, &'static str> {
        let parts: Vec<&str> = seed.split('_').collect();
        if parts.len() != 6 {
            return Err("Invalid TNF seed: BB(6) requires 6 state blocks");
        }

        let mut transitions = [[None; 2]; 6];

        for (state_idx, block) in parts.iter().enumerate() {
            if block.len() != 6 {
                return Err("Invalid block length: expected 6 characters");
            }
            
            let chars: Vec<char> = block.chars().collect();
            
            // Symbol 0 transition (first 3 chars)
            transitions[state_idx][0] = Self::parse_transition(&chars[0..3]);
            // Symbol 1 transition (last 3 chars)
            transitions[state_idx][1] = Self::parse_transition(&chars[3..6]);
        }

        Ok(Machine { transitions })
    }

    fn parse_transition(chunk: &[char]) -> Option<Transition> {
        if chunk[0] == '-' {
            return None; // Halt transition
        }

        let write = if chunk[0] == '1' { 1 } else { 0 };
        let next_move = if chunk[1] == 'R' { Move::Right } else { Move::Left };
        
        let next_state = match chunk[2] {
            'A' => 0, 'B' => 1, 'C' => 2,
            'D' => 3, 'E' => 4, 'F' => 5,
            _ => -1, // Fallback for halt
        };

        if next_state == -1 {
            None
        } else {
            Some(Transition { write, next_move, next_state })
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tnf_parsing() {
        // BB6-0000 from your holdouts.json
        let seed = "1RB1RF_1RC---_1RD1LC_1LE1RF_1LC0LE_1RA0RA";
        let machine = Machine::from_tnf(seed).expect("Failed to parse");

        // Verify State A, Symbol 0 -> 1RB (Write 1, Move Right, State B)
        let t0 = machine.transitions[0][0].unwrap();
        assert_eq!(t0.write, 1);
        assert_eq!(t0.next_move, Move::Right);
        assert_eq!(t0.next_state, 1); // B is state index 1

        // Verify State B, Symbol 1 -> --- (Halt)
        let t1 = machine.transitions[1][1];
        assert!(t1.is_none());
    }
}