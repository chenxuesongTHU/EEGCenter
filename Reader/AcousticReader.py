#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   AcousticReader  
@Time        :   2021/12/10 3:28 下午
@Author      :   Xuesong Chen
@Description :   
"""
import IPython.display as ipd
import librosa
from pathlib import Path
import librosa.display
import matplotlib.pyplot as plt
import matplotlib; # matplotlib.use('TkAgg')
import soundfile as sf

class AcousticReader():
    def __init__(self, file_path, sfreq=100):
        acoustic, org_sfreq = librosa.load(Path(file_path), sr=None)
        self.acoustic = librosa.resample(acoustic, org_sfreq, sfreq)

        # librosa.display.waveplot(self.acoustic, sr=self.sfreq)
        # plt.show()
        # print()


if __name__ == '__main__':
    file_path = '../data/acoustics/A1.wav'
    # acoustic = AcousticReader('../data/acoustics/A1.wav')
    # ipd.Audio(acoustic.acoustic, acoustic.sfreq)
    # acoustic.acoustic.write('tmp.wav', acoustic.sfreq)
    acoustic, org_sfreq = librosa.load(Path(file_path), sr=None)
    new_sfreq = int(org_sfreq/100)
    acoustic = librosa.resample(acoustic, org_sfreq, new_sfreq)
    sf.write('tmp.wav', acoustic, new_sfreq)
    # sf.write('tmp.wav', acoustic.acoustic, acoustic.sfreq, 'PCM_24')


