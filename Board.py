import numpy as np

class Board:
  
  def get_win_patterns(self, N):
    DF = (N-4)+1
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
  
  def __init__(self, N):
    self.N = N
    self.WIN_PATTERNS = self.get_win_patterns(N)
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
    
  def get_valid_actions(self):
    return [i for i in range(self.N) if self.active_pos[i]<self.N]

  def print_board(self):
    print(np.transpose(np.reshape(self.board,(self.N,self.N))))

  def visualize_win_conditions(self):
    for s in self.WIN_PATTERNS:
      board = np.array([0]*self.N*self.N)
      board[s] = 1
      print(np.transpose(np.reshape(board,(self.N,self.N))))
      print('\n')
