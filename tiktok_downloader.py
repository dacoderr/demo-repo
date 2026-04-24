#!/usr/bin/env python3
"""Simple TikTok video/audio downloader powered by yt-dlp."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.stderr.write(
        "yt-dlp is not installed. Install it with:\n"
        "    pip install -U yt-dlp\n"
    )
    sys.exit(1)


def build_options(mode: str, output_dir: Path, insecure: bool = False) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(output_dir / "%(uploader)s - %(id)s.%(ext)s")

    opts: dict = {
        "outtmpl": outtmpl,
        "restrictfilenames": True,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        "nocheckcertificate": insecure,
    }

    if mode == "audio":
        opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
    else:
        opts["format"] = "bv*+ba/best"
        opts["merge_output_format"] = "mp4"

    return opts


def download(urls: list[str], mode: str, output_dir: Path, insecure: bool = False) -> int:
    opts = build_options(mode, output_dir, insecure=insecure)
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.download(urls)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download TikTok videos or audio using yt-dlp.",
    )
    parser.add_argument(
        "urls",
        nargs="+",
        help="One or more TikTok video URLs.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=("video", "audio"),
        default="video",
        help="Download full video (default) or extract audio as mp3.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("downloads"),
        help="Output directory (default: ./downloads).",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Skip TLS certificate verification (use only on trusted networks, "
             "e.g. behind a corporate MITM proxy).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return download(args.urls, args.mode, args.output, insecure=args.insecure)
    except yt_dlp.utils.DownloadError as err:
        sys.stderr.write(f"Download failed: {err}\n")
        return 1
    except KeyboardInterrupt:
        sys.stderr.write("\nInterrupted.\n")
        return 130


if __name__ == "__main__":
    sys.exit(main())
