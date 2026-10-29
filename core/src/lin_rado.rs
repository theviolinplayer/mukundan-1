use std::collections::HashMap;

#[derive(Clone, Debug, PartialEq)]
pub struct MachineSnapshot {
    pub step: u64,
    pub state: u64,
    pub head_position: i64,
    pub active_tape: Vec<u8>, 
    pub tape_offset: i64,
}

pub struct LinRadoDetector {
    checkpoints: Vec<MachineSnapshot>,
    next_checkpoint: u64,
}

impl LinRadoDetector {
    pub fn new() -> Self {
        Self {
            checkpoints: Vec::with_capacity(64),
            next_checkpoint: 2,
        }
    }


    pub fn ingest_and_check(
        &mut self, 
        step: u64, 
        state: u64, 
        head: i64, 
        active_tape: Vec<u8>, 
        tape_offset: i64
    ) -> bool {
        
        let current_snapshot = MachineSnapshot {
            step,
            state,
            head_position: head,
            active_tape,
            tape_offset,
        };

        for checkpoint in self.checkpoints.iter().rev() {
            if self.is_recurring(checkpoint, &current_snapshot) {
                return true;
            }
        }

        if step >= self.next_checkpoint {
            self.checkpoints.push(current_snapshot);
            self.next_checkpoint *= 2; 
        }

        false
    }

    fn is_recurring(&self, past: &MachineSnapshot, current: &MachineSnapshot) -> bool {

        if past.state != current.state {
            return false;
        }

        if past.active_tape != current.active_tape {
            return false;
        }

        let past_relative_head = past.head_position - past.tape_offset;
        let current_relative_head = current.head_position - current.tape_offset;
        
        if past_relative_head != current_relative_head {
            return false;
        }

        let absolute_shift = current.head_position - past.head_position;
        if absolute_shift == 0 {
            return true; 
        }

        true
    }
}