# continuous-chromagram
Octave-reduced spectrogram visualizer.

As described in: Lenchitz, Jordan, and Anthony Coniglio. Continuous Chromagrams and Pseudometric Spaces of Sound Spectra. In: Montiel, M., Agustín-Aquino, O.A., Gómez, F., Kastine, J., Lluis-Puebla, E., Milam, B. (eds) Mathematics and Computation in Music. MCM 2022. Lecture Notes in Computer Science, vol 13267. Springer, Cham. https://doi.org/10.1007/978-3-031-07015-0_25 (Preprint available <a href="https://github.com/jordan-lenchitz/continuous-chromagram/blob/9a081ebf1b613c15d870e381b41ec78acc63ee7a/Continuous%20Chromagrams%20and%20Pseudometric%20Spaces%20of%20Sound%20Spectra.pdf">in this repository</a>.)


Necessary modules: librosa, numpy, skimage, matplotlib

Syntax: cc_vis(filename, x=200, W=2**16, colormap='rainbow')

x is frequency a for [a, 2a) chroma octave

W is FFT size: power of 2 (minimum 2^10, maximum 2^18); smaller = faster runtime and sharper time resolution, larger = slower runtime and sharper frequency resolution

colormap is for visualization; https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html for options

Example: visualize the octave-reduced spectrogram of 'my_sound.wav' in the chroma octave [300, 600) 'Hz' with a 1024-point FFT and the colormap plasma
>cc_vis('my_sound.wav', 300, 2**10, 'plasma')
