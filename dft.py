import numpy as py
import matplotlib.pyplot as plot
import math as math
from wav import WavReader


wav = WavReader('test-data/flute4.wav')
wav.show()

wav.showDFT()
