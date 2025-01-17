mod cell_state;
mod game_state;
mod player;
use std::io::stdin;

use crate::game_state::GameState;

fn main() {
    let mut game = GameState::new();
    game.print();
    loop {
        println!("Player {}: Enter your move!", game.current_player());
        let mut input = String::new();
        stdin().read_line(&mut input).unwrap();
        let player_move: Vec<&str> = input.trim().split(",").collect();
        if player_move.len() != 2 {
            println!("Wrong number of coordinates!");
            continue;
        }
        let x = if let Ok(val) = player_move[0].parse::<usize>() {
            val
        } else {
            println!("Invalid coordiate");
            continue;
        };
        let y = if let Ok(val) = player_move[0].parse::<usize>() {
            val
        } else {
            println!("Invalid coordinate");
            continue;
        };
        if let Err(msg) = game.make_move(x, y) {
            println!("{}", msg);
            continue;
        }
        if let Some(winner) = game.winner() {
            println!("The winner is {winner}!");
            return;
        }
        game.print();
    }
}

#[cfg(test)]
mod tests {
    use crate::game_state::GameState;
    use crate::player::Player;
    #[test]
    fn test_main_current_player() {
        let mut game = GameState::new();
        assert!(game.current_player() == Player::X);
        let _ = game.make_move(1, 1);
        assert!(game.current_player() == Player::O);
    }

    #[test]
    fn test_main_out_of_bounds() {
        let mut game = GameState::new();
        let result = game.make_move(3, 3);
        assert_eq!(result, Err("Out of bounds".to_string()));
        assert!(result.is_err());
    }
}
