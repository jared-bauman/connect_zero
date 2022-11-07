class GameTree:
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
      self.idxs[c] = len(idxs)
      self.children.append(np.array([-1]*N))
      self.values.append(np.array([0.,0]))

  def update_values_mc(self, visit_idxs, w, gamma=1.0):
    decay = 1.0
    visit_idxs.reverse()
    for i in visit_idxs:
      c = self.values[i][COUNT_IDX]
      self.values[i][VALUE_IDX] = (
          (self.values[i][VALUE_IDX] * c + w * decay) / (c + 1)
      )
      self.values[i][COUNT_IDX] += 1
      decay *= gamma
