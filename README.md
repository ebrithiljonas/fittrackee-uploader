# FitTrackee Uploader

**A companion application for [FitTrackee](https://samr1.github.io/FitTrackee/) to upload your workout files**

With this application you can easily upload your workouts to your FitTrackee instance. Just set a source folder where you store your workouts, and it will show you the track and some basic stats. You can choose a sport type and set a title and then just hit upload and your file will automatically be converted to a GPX file and uploaded.

![](images/main_window.png)

## Features

- Upload workout files from a folder, for example your Garmin watch after connecting it
- Move uploaded files to a different folder and optionally add title and sport type to the filename
- Add some basic stats to the description on FitTrackee like calories and average heart rate.
- Allows uploading files that are not compatible with FitTrackee like FIT files

## Supported file types

- FIT
- GPX

## Installation

Clone repository

```sh
git clone https://github.com/ebrithiljonas/fittrackee-uploader.git
```

Run application
```sh
cd fittrackee-uploader
python fittrackee-uploader
```