"""

Pair programming workshop on 2025-01-07

With Jakub Sygnowski
"""

from collections import defaultdict
import enum
import random
from dataclasses import dataclass

Code = list[int]


class Result(enum.Enum):
  NO_MATCH = enum.auto()
  PARTIAL = enum.auto()
  MATCH = enum.auto()


NUM_ITEMS = 3
NUM_COLORS = 5
MAX_TURNS = 12


@dataclass
class State:
  code: Code
  # past_guesses: list[Code]


def generate_code() -> State:
  code = [0, 0, 0, 0]
  for i in range(NUM_ITEMS):
    code[i] = random.randint(0, NUM_COLORS - 1)
  return State(code)


def get_matches(code: Code, guess: Code) -> list[Result]:
  matches = []
  partial_matches = []
  no_matches = []
  to_check = defaultdict(int)

  for i, guess_peg in enumerate(guess):
    if guess_peg == code[i]:
      matches.append(i)
    else:
      to_check[guess_peg] += 1

  for i, code_peg in enumerate(code):
    if i in matches:
      continue
    if to_check[code_peg] > 0:
      to_check[code_peg] -= 1
      partial_matches.append(i)
    else:
      no_matches.append(i)
  x = [
      *[Result.MATCH] * len(matches),
      *[Result.NO_MATCH] * len(no_matches),
      *[Result.PARTIAL] * len(partial_matches),
  ]
  return x


state = State(code=Code([0, 1, 1, 1]))
guess = Code([2, 0, 0, 7])

assert get_matches(state.code, guess) == [
    Result.NO_MATCH, Result.NO_MATCH, Result.NO_MATCH, Result.PARTIAL
]

# mode = input("(H)uman or (C)omputer\n")
mode = "C"
if mode == "H":
  state = generate_code()
  turn_counter = 0
  while (turn_counter < MAX_TURNS):
    print(
        f"Turn {turn_counter} - Enter your guess, in the format of eg. 0,5,1,3. "
    )
    user_input = Code([int(i) for i in input().split(",")])
    assert len(user_input) == 4
    for i in user_input:
      assert 0 <= i < NUM_COLORS
    matches = get_matches(state.code, user_input)
    print(", ".join(m.name for m in matches))
    if set(matches) == set([Result.MATCH]):
      print("You win!")
      exit(0)
    else:
      turn_counter += 1


def all_possible_codes(length=1):
  if length == 0:
    return
  if length == 1:
    for i in range(NUM_COLORS):
      yield [i]
    return
  for code in all_possible_codes(length - 1):
    for i in range(NUM_COLORS):
      yield [i] + code


all_codes = list(all_possible_codes(NUM_ITEMS))

# print(len(list(all_possible_codes(2))))


def all_matching_codes(guesses, answers):
  matching_codes = []
  for code in all_codes:
    for guess, answer in zip(guesses, answers):
      would_be_answer = get_matches(code, guess)
      if would_be_answer != answer:
        break
    else:
      matching_codes.append(code)
  return matching_codes


def search(guesses, answers, best=9999):
  matching_codes = all_matching_codes(guesses, answers)
  if len(guesses) > 6 or len(guesses) == 1:
    print(f"Searching... {guesses=}, {answers=} {best=}")
  if len(guesses) >= best:
    return best + 1, None
  if len(matching_codes) == 1:
    return len(guesses), None

  min_remaining_rounds = best
  optimal_guess = None
  for guess in all_codes:
    if guess in guesses or (not guesses and
                            (guess[0] > 0 or guess[1] > 1 or guess[2] > 2)):
      continue
    max_plays = -1
    possible_answers = set()
    for code in matching_codes:
      answer = get_matches(code, guess)
      new_matching_codes = all_matching_codes(guesses + [guess],
                                              answers + [answer])
      if len(new_matching_codes) < len(matching_codes):
        possible_answers.add(tuple(answer))

    guesses.append(guess)
    for answer in possible_answers:
      answers.append(list(answer))
      remaining_rounds = search(guesses, answers, min_remaining_rounds)[0]
      # if remaining_rounds == 0 and len(guesses) == 1:
      #   print(
      #       f"Got an immediate answer of {remaining_rounds=} with {code=} and {guess=}"
      #   )

      #   breakpoint()
      if remaining_rounds > max_plays:
        max_plays = remaining_rounds
      answers.pop()
      # if len(guesses) == 1:
      #   print(f"{code=}, {optimal_guesses=}, {max_plays=}")
    guesses.pop()
    if max_plays < min_remaining_rounds and max_plays >= 0:
      optimal_guess = guess
      min_remaining_rounds = max_plays

  # print(f"for {guesses=}, {answers=} we got {min_remaining_rounds=}")

  return min_remaining_rounds, optimal_guess


print(search([], []))

#   all_possible_guesses = fn(codes, answers)
#   for potential_guesses in all_possible_guesses:
