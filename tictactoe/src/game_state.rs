use crate::cell_state::CellState;
use crate::player::Player;
use std::fmt::Display;

#[derive(Debug)]
pub struct GameState {
    board: [[CellState; 3]; 3],
    current_player: Player,
}

impl Display for GameState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in self.board {
            for cell in row {
                write!(f, "{}", cell)?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

impl GameState {
    pub fn new() -> Self {
        Self {
            board: [[CellState::Empty; 3]; 3],
            current_player: Player::X,
        }
    }

    pub fn current_player(&self) -> Player {
        self.current_player
    }

    pub fn print(&self) {
        print!("{}", self);
    }

    pub fn make_move(&mut self, x: usize, y: usize) -> Result<(), String> {
        if x >= self.board.len() || y >= self.board.len() {
            return Err("Out of bounds".to_string());
        }
        if self.board[x][y] != CellState::Empty {
            return Err(format!(
                "That cell was already taken by {}",
                self.board[x][y]
            ));
        }
        self.board[x][y] = match self.current_player {
            Player::X => CellState::X,
            Player::O => CellState::O,
        };
        self.current_player = match self.current_player {
            Player::X => Player::O,
            Player::O => Player::X,
        };
        Ok(())
    }

    pub fn winner(&self) -> Option<Player> {
        // Check rows
        for row in self.board {
            if row[0] != CellState::Empty && row.into_iter().all(|cell| cell == row[0]) {
                return Some(Player::from(row[0]));
            }
        }

        // Check columns
        for col in (0..3).map(|r| self.board[r]) {
            if col[0] != CellState::Empty && col.into_iter().all(|cell| cell == col[0]) {
                return Some(Player::from(col[0]));
            }
        }

        // Check diagonals
        if self.board[0][0] != CellState::Empty
            && self.board[0][0] == self.board[1][1]
            && self.board[1][1] == self.board[2][2]
        {
            return Some(Player::from(self.board[0][0]));
        }

        if self.board[0][2] != CellState::Empty
            && self.board[0][2] == self.board[1][1]
            && self.board[1][1] == self.board[2][0]
        {
            return Some(Player::from(self.board[0][0]));
        }
        None
    }
}
