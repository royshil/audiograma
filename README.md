# audiograma
An open source Audiogram maker - audio for your eyes!

![audiograma example](myvid.gif)

## Setup

Run
```
$ pipenv install
```

Make sure you have ChromeDriver installed.

## Running
:warning: This space station is not fully operational yet! :warning:

Create an audio file with (mostly) speech. Save as `.wav` file.
Run
```
$ python transcribe.py myaudiofile.wav
```
To get the transcription file from AWS saved as `myaudiofile.wav-transcription.json`.
Potentially, edit the transcription to find errors.

Then run
```
$ python drive.py myaudiofile.wav myaudiofile.wav-transcription.json
```
To get the audiogram video.
:metal:
