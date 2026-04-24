# TikTok Downloader

A simple command-line TikTok video/audio downloader built on top of
[yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Install

```bash
pip install -r requirements.txt
```

For audio extraction you also need [`ffmpeg`](https://ffmpeg.org/) available on
your `PATH`.

## Usage

Download a TikTok video (mp4):

```bash
python tiktok_downloader.py https://www.tiktok.com/@user/video/1234567890
```

Extract the audio as mp3:

```bash
python tiktok_downloader.py -m audio https://www.tiktok.com/@user/video/1234567890
```

Multiple URLs and a custom output directory:

```bash
python tiktok_downloader.py -o my_clips URL1 URL2 URL3
```

### Options

| Flag | Description | Default |
| --- | --- | --- |
| `-m`, `--mode` | `video` or `audio` | `video` |
| `-o`, `--output` | Output directory | `./downloads` |
