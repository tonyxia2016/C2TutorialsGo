# C2TutorialsGo
This is a tutorial written for Caffe2 which mocks google AlphaGo.

## Preprocess
  The Go game dataset are usually stored in [SGF](http://www.red-bean.com/sgf/go.html) file format. We need to transform SGF file into Caffe2 Tensor which are 48 feature planes of 19x19 size, according to [DeepMind](http://www.nature.com/nature/journal/v529/n7587/full/nature16961.html?foxtrotcallback=true).  
    The preprocess program relies on `Cython` implementation of [RocAlphaGo](https://github.com/Rochester-NRT/RocAlphaGo) project for Go rules and feature plane generation. It is estimated to take 60 CPU hours for preprocess complete KGS data set.

## Supervised Learning - Policy Network
  According to [DeepMind](http://www.nature.com/nature/journal/v529/n7587/full/nature16961.html?foxtrotcallback=true), AlphaGo (conv=13 filters=192) can achieve 55.4% test accuracy after 20 epochs training. Test set is the first 1 million steps. i.e. KGS2004. The speed of each prediction is 4.8ms (on Kepler GPU).  
  This program (conv=13 filters=192) achieves 52.75% test accuracy by 4 epochs and 54% by 7 epochs so far. Test set is the latest 300K steps. i.e. KGS201705-201706. It also achieved speed of around 4.5ms for each single prediction (on Maxwell GPU). Therefore each epochs takes ~40 GPU hours. Running on GPU mode is around 100x faster than CPU mode.
> Intel Broadwell CPU can provide around 30 GFlops compute power per core.  
> Nvidia Kepler K40 and Maxwell GTX980m GPU can provide around 3 TFlops compute power.  

## Reinforced Learning - Policy Network
  The program is runnable but still under evaluation. It also relies on RocAlphaGo project for Go rules by now. A new program is under construction to implement first 12 features in GPU mode to replace RocAlphaGo. It is believed to be at least 10x faster than RocAlphaGo(python implementation).
> The AI player trained 1 epochs(48% test accuracy) wins over the one trained 0.2 epochs(39% test accuracy) by 14:2  
> The AI player trained 4 epochs(52.75% test accuracy) wins over the one trained 1 epochs by 13:3  
> More result tbd.  

## Supervised Learning - Value Network
tbd. Depends on Reinforced Learning to generate 30 millions games. And pick 1 state of each game.

## Supervised Learning - Fast Rollout
tbd. AlphaGo achieved 24.2% of accuracy and 2us of speed.

## MTCS
tbd. Depends on Fast Rollout.
