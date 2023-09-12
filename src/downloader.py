#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 19:00:25 2023

For more details check the PyTube API https://pytube.io/en/latest/api.html

@author: elianther
"""
# %% IMPORT PACKAGES
import sys
from pathlib import Path
from pytube import YouTube

# %% SET STATIC ENV
TARGET_PATH = Path.cwd().parent.joinpath("data").joinpath("video_clips")
TARGET_PATH.mkdir(parents=True, exist_ok=True)

# %% MAIN LOGIC


def Download(URL, donwload_path=str(TARGET_PATH)):
    try:
        yt = YouTube(URL)
        if yt.length // 60 < 6:
            # Only download videos with MP4 format
            stream = yt.streams.filter(file_extension='mp4',
                                       only_video=True,
                                       res="360p").first()
        else:
            raise SystemExit
        stream.download(output_path=TARGET_PATH)
        print("Download completed successfully.")
    except SystemExit:
        print("Video length over 6 minutes.",
              "Consider downloading another video of shorter duration."
              )
        sys.exit(50)


# %% SAMPLE
if __name__ == '__main__':
    URL = "https://www.youtube.com/watch?v=X5Qa0oe81tE"
    Download(URL)
    videos = [str(video.name) for video in TARGET_PATH.glob("*")]
    print(videos)
