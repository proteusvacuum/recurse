use std::fmt::Display;

use crate::cell_state::CellState;

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum Player {
    X,
    O,
}

impl Display for Player {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Player::O => write!(f, "O",),
            Player::X => write!(f, "X",),
        }
    }
}

impl From<CellState> for Player {
    fn from(cellstate: CellState) -> Self {
        match cellstate {
            CellState::X => Self::X,
            CellState::O => Self::O,
            CellState::Empty => panic!(),
        }
    }
}
