import librosa as la
import numpy as np
from skimage import util
import matplotlib.pyplot as plt

'''helper function that gets column indices for frequency range'''
def col_indices(array, minf, maxf):
    j = 0
    while j<1:
        for q in range(len(array[0])):
            if array[0,q] > minf:
                min_index = q-1
                j += 1
                break
    j = 0
    while j<1:
        for q in range(len(array[0])):
            if array[0,q] > maxf:
                max_index = q
                j += 1
                break
    return (min_index, max_index)

def cc_vis(filename, x=200, W=2**16, colormap='rainbow'):
## x is frequency a for [a, 2a) chroma octave
## W is FFT size: power of 2 (minimum 2**10, maximum 2**18)
## smaller W = faster runtime and sharper time resolution
## larger W = slower runtime and sharper frequency resolution
## see https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html for colormap options

    #read audio file and get an array of its audio frames averaged to mono
    #as well as its sample rate in hz
    audio, rate = la.load(filename)

    #determine number of frames of audio
    N = audio.shape[0]

    #length in seconds = number of frames / frames per second
    L = N / rate

    #window the audio data using a Hann [aka raised cosine] window
    windows = util.view_as_windows(audio, window_shape=(W,), step=int(100 * W/(2**10)))
    win = np.hanning(W + 1)[:-1]
    windows = windows * win

    #transpose windows from rows to columns
    windows = windows.T

    #apply the DFT to each window of audio, slicing out the positive frequencies
    spectrum = np.fft.fft(windows, axis=0)[:W // 2 + 1:-1]

    #normalize data
    S = np.abs(spectrum)

    #tranpose array so frequency is columns and time is rows
    S = S.T

    #get number of slices
    time_slices, freq_slices = S.shape

    #insert helper row of frequencies (in Hz) as 0th row of array
    S = np.insert(S, 0, [(i+1)*rate/(2*freq_slices) for i in range(freq_slices)], 0)

    #get indices from array
    a,b = col_indices(S, x, 2*x)

    #octave reduce helper row frequencies above chroma octave
    for thing in range(b+1, len(S[0])):
        while S[0,thing] > 2*x:
            S[0,thing] *= 0.5
            
    #octave reduce helper row frequencies below chroma octave
    for thing in range(0, a):
        while S[0,thing] < 2*x:
            S[0,thing] *= 2.0           

    #octave reduce amplitudes in a copy of S
    SS = S
    for index in range(b+1, len(S[0])):
        ind = a
        for num in range(a,b+1):
            if SS[0,index] > SS[0, num]:
                ind +=1
            else:
                break
        if ind == a:
            SS[1:,a] += SS[1:,index]
        elif (SS[0,ind+1]/SS[0, index]) < (SS[0, index]/SS[0,ind]):
            SS[1:,ind+1] += SS[1:,index]
        else:
            SS[1:,ind] += SS[1:,index]
    for index in range(0, a):
        ind = a
        for num in range(a,b+1):
            if SS[0,index] > SS[0, num]:
                ind +=1
            else:
                break
        if ind == a:
            SS[1:,a] += SS[1:,index]
        elif (SS[0,ind+1]/SS[0, index]) > (SS[0, index]/SS[0,ind]):
            SS[1:,ind+1] += SS[1:,index]
        else:
            SS[1:,ind] += SS[1:,index]    

    #temporarily remove helper row and take only frequencies in chroma octave
    SS = SS[1:,a:b]

    #convert to dB
    SS = 20 * np.log10(SS / np.max(SS))

    #un-tranpose array so frequency is rows and time is columns
    SS = SS.T

    #paint a picture of the result
    f, ax = plt.subplots()
    ax.imshow(SS, origin='lower', cmap=colormap,
          extent=(0, L, S[0,a], S[0,b]))
    ax.axis('tight')
    ax.set_ylabel('Chroma [\'Hz\']')
    ax.set_xlabel('Time [s]')
    ax.set_yscale('log')
    plt.show()
