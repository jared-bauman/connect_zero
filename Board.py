import numpy as np

class Board:
  def __init__(self, N, WIN_PATTERNS):
    self.N = N
    self.WIN_PATTERNS = WIN_PATTERNS
    self.board = np.array([0]*N*N) # board representation
    self.active_pos = np.array([0]*N) # column position counter

  def check_win(self):
    for s in self.WIN_PATTERNS:
      t = np.sum(self.board[s])
      if t==4:
        return 1
      elif t==-4:
        return -1
    return 0

  def place(self, x, player_one):
    assert 0<=x<self.N
    y = self.active_pos[x]
    assert 0<=y<self.N
    self.board[(self.N-1)-y+x*self.N] = (1 if player_one else -1)
    self.active_pos[x] += 1

  def print_board(self):
    print(np.transpose(np.reshape(self.board,(self.N,self.N))))
