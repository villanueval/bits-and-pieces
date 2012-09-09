#!/usr/bin/env python

# wavdata
# Based on the wav2png.py script of Freesound.org
# 

prog_name="wavdata"
prog_ver="0.1"
prog_date="13-Mar-09"

import optparse, math, sys
import scikits.audiolab as audiolab
import numpy
from scipy.io import write_array
from decimal import *

class TestAudioFile(object):
    """A class that mimics audiolab.sndfile but generates noise instead of reading
    a wave file. Additionally it can be told to have a "broken" header and thus crashing
    in the middle of the file. Also useful for testing ultra-short files of 20 samples."""
    def __init__(self, num_frames, has_broken_header=False):
        self.seekpoint = 0
        self.num_frames = num_frames
        self.has_broken_header = has_broken_header

    def seek(self, seekpoint):
        self.seekpoint = seekpoint

    def get_nframes(self):
        return self.num_frames

    def get_samplerate(self):
        return 44100

    def get_channels(self):
        return 1

    def read_frames(self, frames_to_read):
        if self.has_broken_header and self.seekpoint + frames_to_read > self.num_frames / 2:
            raise IOError()

        num_frames_left = self.num_frames - self.seekpoint
        will_read = num_frames_left if num_frames_left < frames_to_read else frames_to_read
        self.seekpoint += will_read
        return numpy.random.random(will_read)*2 - 1 


class AudioProcessor(object):
    def __init__(self, audio_file, fft_size, nyquist_freq, window_function=numpy.ones):
        self.fft_size = fft_size
        self.window = window_function(self.fft_size)
        self.audio_file = audio_file
        self.frames = audio_file.get_nframes()
        self.samplerate = audio_file.get_samplerate()
        self.channels = audio_file.get_channels()
        self.spectrum_range = None
        self.lower = 1
        self.higher = nyquist_freq
        self.lower_log = math.log10(self.lower)
        self.higher_log = math.log10(self.higher)
        self.clip = lambda val, low, high: min(high, max(low, val))

    def read(self, start, size, resize_if_less=False):
        """ read size samples starting at start, if resize_if_less is True and less than size
        samples are read, resize the array to size and fill with zeros """
        
        # number of zeros to add to start and end of the buffer
        add_to_start = 0
        add_to_end = 0
        
        if start < 0:
            # the first FFT window starts centered around zero
            if size + start <= 0:
                return numpy.zeros(size) if resize_if_less else numpy.array([])
            else:
                self.audio_file.seek(0)

                add_to_start = -start # remember: start is negative!
                to_read = size + start

                if to_read > self.frames:
                    add_to_end = to_read - self.frames
                    to_read = self.frames
        else:
            self.audio_file.seek(start)
        
            to_read = size
            if start + to_read >= self.frames:
                to_read = self.frames - start
                add_to_end = size - to_read
        
        try:
            samples = self.audio_file.read_frames(to_read)
        except IOError:
            # this can happen for wave files with broken headers...
            return numpy.zeros(size) if resize_if_less else numpy.zeros(2)

        # convert to mono by selecting left channel only
        # add option to use either channel
        if self.channels > 1:
            samples = samples[:,0]

        if resize_if_less and (add_to_start > 0 or add_to_end > 0):
            if add_to_start > 0:
                samples = numpy.concatenate((numpy.zeros(add_to_start), samples), axis=1)
            
            if add_to_end > 0:
                samples = numpy.resize(samples, size)
                samples[size - add_to_end:] = 0
        
        return samples


    def spectral(self, seek_point, spec_range=120.0):
        """ starting at seek_point read fft_size samples, and calculate the spectral centroid """
        
        samples = self.read(seek_point - self.fft_size/2, self.fft_size, True)

        samples *= self.window
        fft = numpy.fft.fft(samples)

        #Test
	spectrum = fft[:fft.shape[0] / 2 + 1]

        db_spectrum = (20*(numpy.log10(spectrum + 1e-30))).clip(-spec_range, 0.0)

        #outFile = file('db_spectrum' + str(seek_point) + '.txt', 'w')
        #numpy.savetxt(outFile, db_spectrum, fmt='%3.5f')
        #outFile.close()

        return (db_spectrum)



def extract_data(input_filename, fft_size):
    print "\tProcessing file %s:\n\t" % input_file,
    audio_file = audiolab.sndfile(input_filename, 'read')

    no_samples = audio_file.get_nframes() + 0.0
    sample_rate = audio_file.get_samplerate() + 0.0
    sound_duration = no_samples / sample_rate + 0.0
    nyquist_freq = (audio_file.get_samplerate() / 2) + 0.0

    freq_precision = (sample_rate / fft_size)
    time_precision = (fft_size / sample_rate)
    time_steps = int((no_samples / sample_rate / time_precision))
    sample_steps = int(time_precision * sample_rate)
    processor = AudioProcessor(audio_file, fft_size, nyquist_freq, numpy.hanning)

    for x in range(time_steps):
        
        if x % (time_steps/1000) == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
            
        seek_point = int(x * sample_steps)
        next_seek_point = int((x + 1) * sample_steps)
        
        db_spectrum = processor.spectral(seek_point)
        outFile = file('out' + str(seek_point) + '.txt', 'a')
        numpy.savetxt(outFile, db_spectrum, fmt='%3.5f', delimiter=',')
        outFile.close()

    print " done"


if __name__ == '__main__':
    parser = optparse.OptionParser("usage: %prog [options] input-filename", conflict_handler="resolve")
    parser.add_option("-f", "--fft", action="store", dest="fft_size", type="int", help="fft size, power of 2 for increased performance (default %default)")
    parser.add_option("-v", "--version", action="store_true", dest="version", help="display version information")
    
    parser.set_defaults(fft_size=1024)

    (options, args) = parser.parse_args()

    if not options.version:
	    if len(args) == 0:
	        parser.print_help()
	        parser.error("not enough arguments")
	   
	    # process all files so the user can use wildcards like *.wav
	    for input_file in args:
	        
	        args = (input_file, options.fft_size)


	    extract_data(*args)
    else:
        print "\n%s version %s" % (prog_name,prog_ver)
        print " Binary file built on Ubuntu 8.04.2 using Python 2.5.2, Pyinstaller 1.3,\n  Audiolab module 0.8dev, and numpy 1.0.4\n"
