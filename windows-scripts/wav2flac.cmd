REM
REM Script to compress all the wav files in a directory to flac.
REM 
REM It compresses the files and then moves the flac files to the sub-directory 'flac'
REM
REM The pause at the end was because I wanted to see that it had finished when double-clicked.
REM

set encoder="C:\Program Files (x86)\FLAC\flac.exe"

for %%f in (*.wav) do %encoder% -V %%f

mkdir flac

move *.flac flac\

pause

