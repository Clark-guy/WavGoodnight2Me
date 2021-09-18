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
import sys

def plotWav(data):
    plt.figure()
    plt.plot(data)
    plt.xlabel("index")
    plt.ylabel("Amplitude")
    plt.title("waveform of audio")
    plt.show()

def matchArray(data1, data2, fillType):
    pass

def genSinWave(playSeconds):
    Fs = 44100
    out = np.empty(int(Fs*playSeconds))
    for x in range(int(Fs*playSeconds)):
        out[x] = math.sin(x/20)
    return out

def genNoise(playSeconds):
    Fs = 44100
    out = np.empty(int(Fs*playSeconds))
    for x in range(int(Fs*playSeconds)):
        out[x] = random.randrange(-1, 2)
    return out

def genBlank(playSeconds):
    Fs = 44100
    out = np.empty(int(Fs*playSeconds))
    for x in range(int(Fs*playSeconds)):
        out[x] = 0 
    return out

def playAudio(filename):
    print("playing audio")
    p = multiprocessing.Process(target=playsound, args=(filename,))
    p.start()
    input("press enter to stop playback")
    p.terminate()



def stringToMorse(inString): #takes input string, converts to array of chars. for each char, adds morse code and then converts to beeps
    #first make dict from file
    f = open("morse.txt", "r")
    morseDict = {}
    for line in f:
        morseDict[line[0]] = line[1:-1]
    outStr = ""
    for ch in inString:
        outStr = outStr + morseDict[ch] + " "
    print(outStr)
    return outStr   


def morseStringToAudio(inString):   #takes input string in morse code, creates audio file of morse code
    out = np.empty([])
    unitLen = .05
    for ch in inString:
        if ch == ".":
            out = np.concatenate((out, genSinWave(unitLen*1)), axis=None)
            out = np.concatenate((out, genBlank(unitLen*1)), axis=None)
        elif ch == "-":
            out = np.concatenate((out, genSinWave(unitLen*3)), axis=None)
            out = np.concatenate((out, genBlank(unitLen*1)), axis=None)
        elif ch == " ":
            out = np.concatenate((out, genBlank(unitLen*2)), axis=None)
    return out
        

def readWav(filename):
    Fs, data = read(filename)
    data = data[:,0]
    #print(data.ndim)    #  data is a one dimensional
    #print(type(data))   #  ndim array from numpy
    print("sampling freq: " , Fs)
    print("length of data: ", len(data))
    print("divided by freq (seconds of audio): ", len(data)/Fs)

def mixAudio(data1, data2, amtD1, amtD2):   #takes 2 np arrays and 2 values 
    for x in range(len(data1)):
        data1[x] = amtD1*data1[x]
    for x in range(len(data2)):
        data2[x] = amtD2*data2[x]
    # check if arrays are same length, if not, broadcast and then .add(a,b)
    len1 = len(data1)
    len2 = len(data2)
    if len1 !=len2:
        if len1<len2:
            print(len(data1),len(data2))
            data1 = np.concatenate((data1, np.zeros(len2-len1)), axis=None)
        else:
            # TODO fix it so this actually pads 
            # data 1 is longer than data 2
            print(len(data1),len(data2))
            data2 = np.concatenate((data2, np.zeros(len1-len2)), axis=None)

    print(len(data1), len(data2))
    output = data1+data2
    return output

if __name__ == "__main__":
    #default string is SOS
    if len(sys.argv) == 1:
        englishStr = "SOS"
    else:
        englishStr = sys.argv[1]
    englishStr = englishStr.upper()

    #frequency sample rate is 44100
    Fs = 44100
    morseStr = stringToMorse(englishStr)      # generates data for moString in morse code (returns string of morse code)
    morse = morseStringToAudio(morseStr)    # generates waveform from morse code string
    # mix morse with noise generated of same length
    noise = genNoise(len(morse)/Fs)
    out = mixAudio(noise, morse, .1, .9)
    write("out.wav", Fs, out)
    playAudio("out.wav")
    #out = np.empty([])
    #for x in range(5):
    #    out = np.concatenate((out, genSinWave(1)), axis=None)
    #    out = np.concatenate((out, genNoise(1)), axis=None)
    #    out = np.concatenate((out, genBlank(1)), axis=None)
    #plotWav(out)
    #write("out.wav", Fs, out)
    #playAudio("out.wav")
