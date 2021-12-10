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

## Built with

- [Selenium](https://www.selenium.dev/) and [chromedriver](https://chromedriver.chromium.org/)
- [audiomotion.dev](audiomotion.dev)
- [canvasTxt](https://canvas-txt.geongeorge.com/#/)
- [Pizzicato](https://alemangui.github.io/pizzicato/)
- [coolors.co](https://coolors.co/75b9be-006494-ffe5d4-003554-051923)
- And a whole lot of Stackoverflow.com ...
