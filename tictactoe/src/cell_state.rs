use std::fmt::Display;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CellState {
    Empty,
    X,
    O,
}

impl Display for CellState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            CellState::Empty => write!(f, ".\t",),
            CellState::O => write!(f, "O\t",),
            CellState::X => write!(f, "X\t",),
        }
    }
}
