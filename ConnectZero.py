import numpy as np
import random

N=7 # number of rows and columns
DF=4 # degrees of freedom in positioning streaks
EPS=0.01 # exploration probability

def get_valid_states(valid_actions, next_states):
  return [next_states[i] for i in valid_actions]

def get_state_values(values, valid_states):
  return [0 if i == -1 else values[i][VALUE_IDX] for i in valid_states]

def get_uniform_action(k):
  return random.randrange(start=0, stop=k)

def get_extreme_index(state_values, player_one):
  candidates = []
  if player_one:
    candidates = np.argwhere(state_values == np.max(state_values))
  else:
    candidates = np.argwhere(state_values == np.min(state_values))
  r = get_uniform_action(len(candidates))
  return np.squeeze(candidates[r])
  
def select_eps_greedy(values, valid_actions, next_states, player_one):
  if random.random() < EPS:
    k = len(valid_actions)
    return valid_actions[get_uniform_action(k)]
  else:
    valid_states = get_valid_states(valid_actions, next_states)
    state_values = get_state_values(values, valid_states)
    return valid_actions[get_extreme_index(state_values, player_one)]

def play_game(board, active_pos, idxs, values, children):

  visit_idxs = []
  player_one = True
  p_idx = 0
  while(check_win(board, WIN_PATTERNS)==0):

    # subset to permissible moves
    valid_actions = get_valid_actions(active_pos)

    # select action and update board
    next_states = children[p_idx]

    action = select_eps_greedy(values, valid_actions, next_states, player_one)
    place(action, board, player_one)

    # add state to game tree if not already there
    add_state(idxs, values,  children, board, p_idx)

    # switch to next player and update index of board state
    player_one = not player_one
    p_idx = idxs[board.tobytes()]
    visit_idxs.append(p_idx)

    print_board(board)

  return (check_win(board, WIN_PATTERNS), visit_idxs)

  if __name__ == "__main__":
    NSIM = 10
    idxs, values, children = init_game_tree()
    for i in range(NSIM):

      board, active_pos = init_board()

      w, visit_idxs = play_game(board, active_pos, idxs, values, children)
      update_values_mc(values, visit_idxs, w, 0.95)
      print("game completed in " + str(len(visit_idxs)) + " moves")
      print(w)
      print(values)
