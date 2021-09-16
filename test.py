import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
#from IPython.display import Audio
from numpy.fft import fft, ifft
#%matplotlib inline
import random
import copy
import multiprocessing
from playsound import playsound
import math


def plotWav(data):
    plt.figure()
    plt.plot(data)
    plt.xlabel("index")
    plt.ylabel("Amplitude")
    plt.title("waveform of audio")
    plt.show()


def genSinWave(playSeconds):
    Fs = 44100
    out = np.empty(Fs*playSeconds)
    for x in range(Fs*playSeconds):
        out[x] = math.sin(x/20)
    return out

def genNoise(playSeconds):
    Fs = 44100
    out = np.empty(Fs*playSeconds)
    for x in range(Fs*playSeconds):
        noise[x] = random.randrange(-2000000000, 2000000000)
    return out

def genBlank(playSeconds):
    Fs = 44100
    out = np.empty(Fs*playSeconds)
    for x in range(Fs*playSeconds):
        noise[x] = 0 
    return out

def playAudio(filename):
    print("playing audio")
    p = multiprocessing.Process(target=playsound, args=(filename,))
    p.start()
    input()
    p.terminate()


def beep(length): #returns a small length array for use to add to another array
    pass

def stringToMorse(inString): #takes input string, converts to array of chars. for each char, adds morse code and then converts to beeps
    pass


if __name__ == "__main__":
    # initialize data, read out sampling frequency
    Fs, data = read("ez.wav")
    data = data[:,0]
    #print(data.ndim)    #  data is a one dimensional
    #print(type(data))   #  ndim array from numpy
    print("sampling freq: " , Fs)
    print("length of data: ", len(data))
    print("divided by freq (seconds of audio): ", len(data)/Fs)
    out = genSinWave(10)
    write("out.wav", Fs, out)
    # make noise
    noise = copy.deepcopy(data)
    for x in range(len(noise)):
        noise[x] = random.randrange(-2000000000, 2000000000)
    #plotWav(data)
    write("noise.wav", Fs, noise)
    playAudio("noise.wav")
