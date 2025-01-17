use std::io::stdin;

#[derive(Debug)]
struct GameState {
    board: [[CellState; 3]; 3],
    current_player: Player,
}

impl GameState {
    fn print(&self) {
        for row in self.board {
            for cell in row {
                match cell {
                    CellState::Empty => print!(".\t",),
                    _ => print!("{:?}\t", cell),
                };
            }
            println!("");
        }
    }

    fn make_move(&mut self, x: usize, y: usize) -> Result<(), ()> {
        if self.board[x][y] != CellState::Empty {
            return Err(());
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

    fn winner(&self) -> Option<Player> {
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

#[derive(Debug)]
enum Player {
    X,
    O,
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

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum CellState {
    Empty,
    X,
    O,
}

fn main() {
    let board = [[CellState::Empty; 3]; 3];
    let mut game = GameState {
        board,
        current_player: Player::X,
    };
    game.print();
    loop {
        println!("Player {:?}: Enter your move!", game.current_player);
        let mut buf = String::new();
        stdin().read_line(&mut buf).unwrap();
        let player_move: Vec<&str> = buf.trim().split(",").collect();
        assert!(player_move.len() == 2);
        let x = usize::from_str_radix(player_move[0], 10).unwrap();
        let y = usize::from_str_radix(player_move[1], 10).unwrap();
        if x >= game.board.len() || y >= game.board.len() {
            println!("Nice Try!");
            continue;
        }
        match game.make_move(x, y) {
            Err(_) => {
                println!("Nice Try!");
                continue;
            }
            _ => {}
        }
        let winner = game.winner();
        if winner.is_some() {
            println!("The winner is {:?}!", winner.unwrap());
            return;
        }
        game.print();
    }
}
