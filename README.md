# C2TutorialsGo
This is a tutorial written for Caffe2 which mocks google AlphaGo.

## Preprocess
The preprocess program relies on [RocAlphaGo](https://github.com/Rochester-NRT/RocAlphaGo) project for Go rules and feature plane generation.  
The preprocess takes around 500 CPU hours in python implementation for complete KGS data set. By 2017-09-10, the program switched to `Cython` implementation of RocAlphaGo, it is estimated to take 50 CPU hours for preprocess complete KGS data set.

## Supervised Learning - Policy Network
According to [DeepMind](http://www.nature.com/nature/journal/v529/n7587/full/nature16961.html?foxtrotcallback=true), AlphaGo (conv=13 filters=192) can achieve 55.4% test accuracy after 20 epochs training. Test set is the first 1 million steps. i.e. KGS2004. The speed of each prediction is 4.8ms (on Kepler GPU).  
This program (conv=13 filters=192) achieves 52.75% test accuracy by 4 epochs so far. Test set is the latest 300K steps. i.e. KGS201705-201706. It also achieved speed of around 4.5ms for each single prediction (on Maxwell GPU). Therefore each epochs takes ~40 GPU hours. Running on GPU mode is around 100x faster than CPU mode.
> Intel Broadwell CPU can provide around 30 GFlops compute power per core.  
> Nvidia Kepler K40 and Maxwell GTX980m GPU can provide around 3 TFlops compute power.  

## Reinforced Learning - Policy Network
The program is runnable but still under evaluation. It also relies on RocAlphaGo project for Go rules by now.  
A new program is under construction to implement first 12 features in GPU mode to replace RocAlphaGo. It is believed to be at least 10x faster than RocAlphaGo(python implementation).
> The AI player trained 1 epochs(48% test accuracy) wins over the one trained 0.2 epochs(39% test accuracy) by 14:2  
> The AI player trained 4 epochs(52.75% test accuracy) wins over the one trained 1 epochs by 13:3  
> More result tbd.  

## Supervised Learning - Value Network
tbd. Depends on Reinforced Learning to generate 30 millions games. And pick 1 state of each game.

## Supervised Learning - Fast Rollout
tbd. AlphaGo achieved 24.2% of accuracy and 2us of speed.

## MTCS
tbd. Depends on Fast Rollout.
