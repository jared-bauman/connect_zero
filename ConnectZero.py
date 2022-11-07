import numpy as np
import random

N=7 # number of rows and columns
DF=4 # degrees of freedom in positioning streaks
EPS=0.01 # exploration probability

def get_win_slices():
  s0 = np.array([0, 1, 2, 3]) # vertical
  s1 = np.array([0, N, 2*N, 3*N]) # horizontal
  s2 = np.array([0, N+1, 2*N+2, 3*N+3]) # positive slope
  s3 = np.array([3, N+2, 2*N+1, 3*N]) # negative slope

  slices = []
  # add vertical slices
  for i in range(DF):
    for j in range(N):
      slices.append(s0 + i + N*j)

  # add horizontal slices
  for i in range(N):
    for j in range(DF):
      slices.append(s1 + i + N*j)

  # add upward slopes
  for i in range(DF):
    for j in range(DF):
      slices.append(s2 + i + N*j)

  # add downward slopes
  for i in range(DF):
    for j in range(DF):
      slices.append(s3 + i + N*j)

  return slices

WIN_PATTERNS = get_win_slices()

def get_valid_actions(active_pos):
   return [i for i in range(N) if active_pos[i]<N]

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

