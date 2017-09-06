
def InitGame(model):
  '''
      Feature      | No. of planes | Description
      Stone colour | 3             | Player stone / opponent stone / empty
      Ones         | 1             | A constant plane filled with 1
      Turns since  | 8             | How many turns since a move was played
      Player color | 1             | Whether current player is black
  '''
  ZERO = model.ConstantFill([], 'ZERO', shape=[1,1,19,19], value=0) # constant
  ONE = model.ConstantFill([], 'ONE', shape=[1,1,19,19], value=1) # constant
  #data, _dim = model.Concat([ZERO,ZERO,ONE,ZERO,ZERO,ZERO,ZERO,ZERO,ZERO,ZERO,ZERO,ZERO], ['data','_dim'], axis=1) #12 features
  data, _dim = model.Concat([ZERO,ZERO,ONE,ZERO,ZERO,ZERO,ZERO,ZERO,ZERO,ZERO,ZERO,ZERO,ONE], ['data','_dim'], axis=1) #13 features, BLACK=+1
  return data
  
def AddGamePlay(model, data, predict):
  ''' AddGamePlay
      It does not consider symmetric, all games are treated independantly.
      Input: data with shape (N, C, H, W)
             predict with shape (N, C, H, W)
      Output: data with shape (N, C, H, W)
  '''
  BOARD_SIZE = model.ConstantFill([], 'board_size', shape=[1,], value=361) # constant
  SPLIT_SIZE = model.GivenTensorIntFill([], 'split_size', shape=[8,], values=np.array([1,1,1,1,6,1,1,1])) # constant
  
  _topk, topk_indices = model.TopK(predict, ['_topk', 'topk_indices'], k=1)
  label, _old_shape = model.Reshape(['topk_indices'], ['label', '_old_shape'], shape=(N,))
  
  onehot = model.OneHot([label, BOARD_SIZE], 'onehot')
  onehot, _ = model.Reshape(['onehot'], ['onehot', '_'], shape=(N,1,19,19))
  
  layer0, layer1, layer2, layer3, \
  layer4to9, layer10, layer11, layer48 = model.Split([data, SPLIT_SIZE], \
                                                     ['layer0', 'layer1', 'layer2','layer3', \
                                                      'layer4to9', 'layer10', 'layer11','layer48'], \
                                                     axis=1)
  ###
  layer0n = layer1 # player of this turn = opponent of last turn
  layer1n = model.Add([layer0, onehot], 'layer1n') # opponent of this turn = player of last turn
  layer2n = model.Sub([layer2, onehot], 'layer2n') # empty. need to calculate taken
  layer3n = layer3 # all ONE
  #
  layer4n = onehot # 1 turns since last move
  layer5to10n = layer4to9
  layer11n = model.Add([layer10, layer11], 'layer11n')
  #
  layer48n = model.Negative(layer48)
  ###
  data = model.Concat([layer0n, layer1n, layer2n, layer3n, \
                       layer4n, layer5to10n, layer11n, layer48n], ['data','_dim'], axis=1)
  
  return data

def Symmetric(model, predict)
  ''' Symmetric is optional
      Input: predict with shape (N*8, C, H, W)
      Output: symm_predict with shape (N*8, C, H, W)
  '''
  # Unify
  symm0, symm1, ... symm7 = model.Segment(predict)
  symm0u = symm0
  symm1u = model.Flip(symm1, axes(3))
  symm2u = model.Flip(symm2, axes=(2))
  symm3u = model.Flip(symm3, axes=(2,3))
  symm4u = model.Transpose(symm4, axes=(0,1,3,2))
  symm5u = model.Flip(symm5, axes=(3))
  symm6u = model.Flip(symm6, axes=(2))
  symm7u = model.Flip(symm7, axes=(2,3))
  # Average
  unify_predict = model.avg(symm0r, symm1r, ... symm7r)
  # Diversify
  symm0d = model.Reshape(unify_predict, Nx1x19x19)
  symm1d = model.Flip(symm0d, axes=(3))
  symm2d = model.Flip(symm0d, axes=(2))
  symm3d = model.Flip(symm0d, axes=(2,3))
  symm4d = model.Transpose(symm0d, axes=(0,1,3,2))
  symm5d = model.Flip(symm4d, axes=(3))
  symm6d = model.Flip(symm4d, axes=(2))
  symm7d = model.Flip(symm4d, axes=(2,3))
  # shape(symm_predict) = [N*8,C,H,W]
  symm_predict = model.concatenate(symm0, ... symm7)
  return symm_predict
