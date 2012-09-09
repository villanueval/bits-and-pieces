#!/usr/bin/python
from struct import pack, unpack         #Some unpacking for the WAV encoding
from FFT import *       		#Some FFT goodness
from Numeric import *                   #Gotta have speedy math
import wave                             #For opening WAV files
from pylab import *	             	#For ploting
from matplotlib.widgets import Slider, Button, RadioButtons

import os #Interact with Operating System
from time import time


specwindow = 60	 #Number of seconds for each spectrogram
fftsize = 2048	#Size of FFT window

##
##class WavTools(object):
##		def __init__(self,filename):
##			self.fh = wave.open(filename)
##						
##		def packcode(self):
##			self.sampwidth = self.fh.getsampwidth()
##			if sampwidth == 1:
##			#8 bits are unsigned, 16 & 32 signed
##				return 'B'
##			#unsiged 8 bits
##			elif sampwidth == 2:
##				return 'h'
##			#signed 16 bits
##			elif sampwidth == 4:
##				return 'i'
##			#signed 32 bits
##			f.close()
##		def info(self):
##			self.fh.getsampwidth()
##			self.fh.
##		def unpackpart(self):
			

def packing_code(samp_width):
	if samp_width == 1:
	#8 bits are unsigned, 16 & 32 signed
		return 'B'
	#unsiged 8 bits
	elif samp_width == 2:
		return 'h'
	#signed 16 bits
	elif samp_width == 4:
		return 'i'
	#signed 32 bits

#def html_head(path):
#	fh = open(path + "/index.html", "w")
#	fh.writeline("<html><body><table border = 0>")
#	fh.close()
#
#def html_entry(path,item):
#	fh = open(path + "/index.html", "w")
#	fh.writeline("<td><img src='" + item + "'</td>">
#	fh.close()
#
#def html_footer(path):
#	fh = open(path + "/index.html", "w")
#	fh.writeline("</table></body></html>")
#	fh.close()



def open_wave(filename,outpath): #Reads WAV file and plots spectrogram
	f = wave.open(filename)
	samplength = f.getnframes()
	sampfreq = f.getframerate()
	print filename
	print float(sampfreq/1000), "kHz", float(samplength/sampfreq), "\tSeconds"
	seconds = samplength/sampfreq
	sampwidth = f.getsampwidth()
	
	#frames = f.readframes(samplength)	
	osig = [] #Making a tuple (cannot be sorted or re-ordered)
	conv_code = packing_code(sampwidth)
	out = list()
	window_width = sampfreq * specwindow
	for window in range(0,seconds/specwindow):
		out = list()
		osig = []
		frames = f.readframes(window_width)
		print "Window #", window,
		#for i in range(window * window_width,(window + 1) * window_width):
		for i in range(0,window_width):
			frame = frames[i*sampwidth:(i+1)*sampwidth]
			osig.append(unpack(conv_code,frame))
			out.append(osig[i][0]) #This cleans up output of unpack, puts it in a list instead of the thing that comes out
		max_out, min_out = max(out), min(out)
		print max(out), min(out) #Ceiling and floor values for window
		outfile = "0" + str(window*specwindow) + "s-spec" #Name the file
		make_spectrogram(out,True,outpath + "/" + outfile,fftsize,sampfreq)
		html_entry(outpath,outfile)
		del osig
		del out
	f.close()
	#return out

def find_max_min(filename):
	f = wave.open(filename)
	samplength = f.getnframes()
	sampfreq = f.getframerate()
	sampwidth = f.getsampwidth()
	conv_code = packing_code(sampwidth)
	frames = f.readframes(samplength)
	osig = []
	out = list()
	max_val, min_val = 0, 0
	for i in range(0,samplength):
		frame = frames[i * sampwidth:(i + 1) * sampwidth]
		temp = unpack(conv_code,frame)
		val = temp[0]
		if val > max_val:
			max_val = val
		elif val < min_val:
			min_val = val
	outval = max_val, "Max", min_val, "Min"
	return outval
		

def make_spectrogram(signal,save=False,filename="specgram",fftsize=1024,sampfreq=44000):
	t0 = time() #Used as a start value to construct a simple timer to see how long this takes (starts the timer)
	figure(figsize=(16, 6),dpi=100) #Set plot's canvas
	axes((0,0,1,1)) #Make it fill the entire canvas with no margins
	Pxx, freqs, bins, im = specgram(signal,NFFT=fftsize,Fs=sampfreq,noverlap=0)#,cmap=get_cmap('Blues'))
	print "Took:", time()-t0, "Seconds",
	clim(-30,90)
	#colorbar()
	#print bins
	if save == True:
		print "Saving image", filename + ".png"
		savefig(filename + ".png", dpi=100, format='png')
		close()
	if save == False:	
		show()

def power_spectrum(signal,start,stop):
	print "Computing power spectrum...",
	signal = signal[start:stop]
	pspec = 10*log10(1e-20+abs(real_fft(signal)))
	print "done!"
	return pspec

def spec_window(frame): #Produce spectrogram for each SPECWINDOW-length window
	print "Window", frame
	print SAMP_FREQ*SPECWINDOW*frame, "Start", SAMP_FREQ*SPECWINDOW*(frame + 1), "Stop"
	make_spectrogram(wave_signal[SAMP_FREQ*SPECWINDOW*frame:SAMP_FREQ*SPECWINDOW*(frame + 1)],save=True, filename=str(frame) + "test")



	

#print "Opening WAV", filename,
#wave_signal = open_wave(filename)
ls = os.listdir(os.curdir)
html_head()
for item in ls:
	wpath = "s-" + item[:-4]
	html_head(wpath)
	if item[-4:] == ".WAV" or item[-4:] == ".wav":
		print "Making spectrograms for:", item
		if os.path.exists("s-" + item[:-4]) == False:
			os.mkdir(wpath)
		open_wave(item)
	html_footer(wpath)
			
		




