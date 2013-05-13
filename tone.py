import wave, random, math, numpy

noise_output = wave.open('tone.wav', 'w')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

# num of seconds
duration = 4

# Hz per second
samplerate = 44100

# total number of samples
samples = duration * samplerate

# pulse per second
frequency = 90 # Hz

"""
The time of one sample is the inverse of the sample rate, and the period is the inverse of the frequency, so the number of samples is also the sample rate divided by the frequency.
"""
period = samplerate / float(frequency) # in sample points

"""
This is the phase increment.
"""
omega = numpy.pi * .2 / period

"""
Creates the x-axis set with 'period' number of items.  numpy.arange(int(period), dtype = numpy.float) produces {0..146}, but since each value is a factor of omega, the transformed set is in the range {0..0.627}.
"""
xaxis = numpy.arange(int(period), dtype = numpy.float) * omega

"""
This snippet calculates the sin for each value in xaxis and multiplies that value with 16384.  Here we're creating the y-axis data.
"""
ydata = 16384 * numpy.sin(xaxis) * (1. + xaxis)


"""
If we were to graph the sets now, we would see an inclining sin wave.  Resize creates an extended array which repeats the ydata chunk, the result being something that looks a bit more like a saw wave than a sin wave due to the omega calculation.
"""
signal = numpy.resize(ydata, (samples,))

for i in signal:
    packed_value = wave.struct.pack('h', i)
    noise_output.writeframes(packed_value)

noise_output.close()