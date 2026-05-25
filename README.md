# continuous chromagram
octave-reduced spectrogram visualizer as described in [`doi.org/10.1007/978-3-031-07015-0_25`](https://doi.org/10.1007/978-3-031-07015-0_25) 

please read <a href="https://github.com/jordan-lenchitz/continuous-chromagram/blob/main/preprint.pdf">full-color pdf preprint and feel free to email</a>

# howto
`pip install librosa numpy skimage matplotlib` if you must then `cc_vis(filename, x=200, W=2**16, colormap='rainbow')`

`filename` doth be your file of a type supported by `librosa`, `x :=` frequency `a` for the `[a, 2a)` chroma octave, `W` is your power of 2 between `2^10` and `2^18` where smaller means faster runtime with sharper time resolution and larger means slower runtime with sharper frequency resolution, and then colormap is for visualization see their [docs](https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html) for all the fun options

# example 
visualize the octave-reduced spectrogram of `'my_sound.wav'` in the chroma octave `[300, 600)` 'Hz' with a 1024-point FFT and the colormap `plasma`

`cc_vis('my_sound.wav', 300, 2**10, 'plasma')`
