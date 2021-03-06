

import sys
import os
import numpy as np

import struct
import soundfile as sf
from soundfile import SoundFile
import sounddevice as sd
#from matplotlib import pyplot as plt
import os.path
import pynput
import json

NEXT_SEG = 'n'
LAST_SEG = 'l'
QUIT = 'q'
_audioArray = []
_sample_rate = 0
_channels = 0
_frames_per_sample_span_in_second = 0


def _readSettingFile():
    paraDict = {}
    with open("setting.config","r") as f:
        lines = f.readlines()
        for line in lines:
            paras = line.split(':')
            paraDict.update({paras[0]:paras[1].replace('\n','')})
    #print(paraDict)
    return paraDict

        

def _loadFile(fileName):
    sf = SoundFile(fileName)
    signal = sf.read()
    channels = sf.channels
    sample_rate = sf.samplerate
    sf.close()
    return signal, channels, sample_rate

def _loadLogFile(filename):
    jsondata = None
    with open(filename,'r') as fr:
        jsondata = json.load(fr)
    return jsondata

def playAudioArray(audioArray,sample_rate):
    sd.play(audioArray, sample_rate)
    status = sd.wait()
    print("sound device status is ",status)


def MainEntry():
    #read config file
    configs = _readSettingFile()
    #assemble full path
    fullfilepath = os.path.join("",configs["PREPATH"],configs["FILE_NAME"])
    fulllogfilepath = "log/reslog_1558590355.txt"
    _segDuration = int(configs["SEGMENT_DURATION"])
    print("Starting to play the audio file:{}".format(_segDuration))
    _audioArray, _channels, _sample_rate = _loadFile(fullfilepath)
    _frames_per_sample_span_in_second = _sample_rate * _segDuration
    endPoint = int(len(_audioArray) / _frames_per_sample_span_in_second)
    print("Audio File Info")
    print("Sample Rate:",_sample_rate)
    print("Channels:",_channels)
    print("Frames per {} Second:{}".format(_segDuration,_frames_per_sample_span_in_second))
    print("Total Segments:",endPoint)
    _startIdx = 0
    _endIdx = 1
    #start second is 5th second
    while True:
        userInput = input()
        if userInput == 'q' or userInput == 'Q':
                break
        #print("Current key input is: {}".format(userInput))
        if userInput == NEXT_SEG:
            if _endIdx == endPoint:
                print("The audio has reached the end.")
            else:
                _startIdx += 1
                _endIdx += 1
        elif userInput == LAST_SEG :
            if _startIdx == 0 :
                print("The audio has rewinded to the start.")
            else:
                _startIdx -= 1
                _endIdx -= 1
        startFrame = _startIdx*_frames_per_sample_span_in_second
        endFrame = _endIdx*_frames_per_sample_span_in_second
        signals = (_audioArray[startFrame:endFrame])[:,0]
        print("current startIdx:{}, endIdx:{}".format(_startIdx,_endIdx))
        print("current startSec:{}, endSec:{}".format(_startIdx*_segDuration,_endIdx*_segDuration))
        print("current startFrame:{}, endFrame:{}".format(startFrame,endFrame))
        playAudioArray(signals,_sample_rate)

    print("Exit the program.")

    





if __name__ == "__main__":
    #read config file
    MainEntry()
