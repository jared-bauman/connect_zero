import numpy as np
import random

class GameTree:
  VALUE_IDX = 0
  COUNT_IDX = 1
  
  def __init__(self, N):
    # board index lookup
    self.idxs = {}
    # 1st pos: val of board position, 2nd: visit count
    self.values = []
    # map to children indices
    self.children = []

  def add_state(self, board, p_idx):
    # add state to game tree if not already there
    c = board.tobytes()
    if c not in self.idxs:
      self.idxs[c] = len(self.idxs)
      self.children.append(np.array([-1]*N))
      self.values.append(np.array([0.,0]))
      
  def get_valid_states(valid_actions, p_idx):
    assert p_idx in self.children
    next_states = self.children[p_idx]
    return [next_states[i] for i in valid_actions]

  def get_state_values(valid_actions, p_idx):
    valid_states = self.get_valid_states(valid_actions, p_idx)
    return [0 if i == -1 else self.values[i][GameTree.VALUE_IDX] for i in valid_states]

  def update_values_mc(self, visit_idxs, w, gamma=1.0):
    decay = 1.0
    visit_idxs.reverse()
    for i in visit_idxs:
      c = self.values[i][GameTree.COUNT_IDX]
      self.values[i][GameTree.VALUE_IDX] = (
          (self.values[i][GameTree.VALUE_IDX] * c + w * decay) / (c + 1)
      )
      self.values[i][GameTree.COUNT_IDX] += 1
      decay *= gamma
      
  def update_values_td0(self, visit_idxs, w, alpha=0.05, gamma=1.0):
    visit_idxs.reverse()
    
    # update the game end state value
    s_prime = visit_ids[-1]
    self.values[s_prime][GameTree.VALUE_IDX] = w
    self.values[s_prime][GameTree.COUNT_IDX] += 1
    
    # update all other values with bootstrap
    for i in range(len(visit_idxs)-1):
      s = visit_idxs[i]
      self.values[s][GameTree.VALUE_IDX] += alpha * (
          gamma*self.values[s_prime][GameTree.VALUE_IDX] - self.values[s][GameTree.VALUE_IDX]
      )
      self.values[s][GameTree.COUNT_IDX] += 1
      s_prime = s
