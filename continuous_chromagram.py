import librosa as la
import numpy as np
from skimage import util
import matplotlib.pyplot as plt

'''helper function that gets column indices for frequency range'''
def col_indices(array: np.ndarray, minf: float, maxf: float) -> tuple[int, int]:
    """
    Get column indices for a given frequency range from the frequency row.
    
    Args:
        array: 2D array where the 0th row contains frequencies in Hz.
        minf: Minimum frequency in Hz.
        maxf: Maximum frequency in Hz.
        
    Returns:
        A tuple (min_index, max_index) representing the indices in the array.
    """
    freqs = array[0]
    min_index = np.searchsorted(freqs, minf) - 1
    max_index = np.searchsorted(freqs, maxf)
    return int(min_index), int(max_index)

def cc_vis(filename: str, x: float = 200, W: int = 2**16, colormap: str = 'rainbow') -> None:
    """
    Visualize the octave-reduced spectrogram (continuous chromagram) of an audio file.

    Args:
        filename: Path to the audio file.
        x: Frequency 'a' for the [a, 2a) chroma octave. Defaults to 200.
        W: FFT size. Power of 2 (typically between 2**10 and 2**18).
           Smaller W = faster runtime and sharper time resolution.
           Larger W = slower runtime and sharper frequency resolution.
        colormap: Matplotlib colormap name for visualization. Defaults to 'rainbow'.
    """
    # Read audio file and get an array of its audio frames averaged to mono
    # as well as its sample rate in hz
    audio, rate = la.load(filename)

    # Determine number of frames of audio
    N = audio.shape[0]

    # Length in seconds = number of frames / frames per second
    L = N / rate

    # Window the audio data using a Hann [aka raised cosine] window
    windows = util.view_as_windows(audio, window_shape=(W,), step=int(100 * W / (2**10)))
    win = np.hanning(W + 1)[:-1]
    windows = windows * win

    # Transpose windows from rows to columns
    windows = windows.T

    # Apply the DFT to each window of audio, slicing out the positive frequencies
    spectrum = np.fft.fft(windows, axis=0)[:W // 2 + 1:-1]

    # Normalize data
    S = np.abs(spectrum)

    # Transpose array so frequency is columns and time is rows
    S = S.T

    # Get number of slices
    time_slices, freq_slices = S.shape

    # Insert helper row of frequencies (in Hz) as 0th row of array
    S = np.insert(S, 0, [(i + 1) * rate / (2 * freq_slices) for i in range(freq_slices)], 0)

    # Get indices from array
    a, b = col_indices(S, x, 2 * x)

    # Octave reduce helper row frequencies above chroma octave
    for thing in range(b + 1, len(S[0])):
        while S[0, thing] > 2 * x:
            S[0, thing] *= 0.5
            
    # Octave reduce helper row frequencies below chroma octave
    for thing in range(0, a):
        while S[0, thing] < 2 * x:
            S[0, thing] *= 2.0           

    # Octave reduce amplitudes in a copy of S
    SS = S
    for index in range(b + 1, len(S[0])):
        ind = a
        for num in range(a, b + 1):
            if SS[0, index] > SS[0, num]:
                ind += 1
            else:
                break
        if ind == a:
            SS[1:, a] += SS[1:, index]
        elif (SS[0, ind + 1] / SS[0, index]) < (SS[0, index] / SS[0, ind]):
            SS[1:, ind + 1] += SS[1:, index]
        else:
            SS[1:, ind] += SS[1:, index]

    for index in range(0, a):
        ind = a
        for num in range(a, b + 1):
            if SS[0, index] > SS[0, num]:
                ind += 1
            else:
                break
        if ind == a:
            SS[1:, a] += SS[1:, index]
        elif (SS[0, ind + 1] / SS[0, index]) > (SS[0, index] / SS[0, ind]):
            SS[1:, ind + 1] += SS[1:, index]
        else:
            SS[1:, ind] += SS[1:, index]    

    # Temporarily remove helper row and take only frequencies in chroma octave
    SS = SS[1:, a:b]

    # Convert to dB
    SS = 20 * np.log10(SS / np.max(SS))

    # Un-transpose array so frequency is rows and time is columns
    SS = SS.T

    # Paint a picture of the result
    f, ax = plt.subplots()
    ax.imshow(SS, origin='lower', cmap=colormap,
              extent=(0, L, S[0, a], S[0, b]))
    ax.axis('tight')
    ax.set_ylabel("Chroma ['Hz']")
    ax.set_xlabel('Time [s]')
    ax.set_yscale('log')
    plt.show()
