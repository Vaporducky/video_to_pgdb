#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 19:00:25 2023

For more details check the PyTube API https://pytube.io/en/latest/api.html

@author: elianther
"""
# %% IMPORT PACKAGES
import sys
from datetime import datetime
from os import environ as env
from pathlib import Path
from pytube import YouTube
# %% DEFINE FUNCTIONS


def download_video(url, download_path,
                   file_ext='mp4', res='360p'):
    download_path = Path(download_path)

    try:
        yt = YouTube(url)
        if yt.length // 60 < 6:
            # Only download videos with MP4 format
            # No audio
            stream = yt.streams.filter(file_extension=file_ext,
                                       only_video=True,
                                       res=res).first()
        else:
            raise SystemExit

        # Create output directory
        date = datetime.now().strftime('%Y%m%d')
        output_path = download_path.joinpath(f"{date}")
        output_path.mkdir(parents=True, exist_ok=True)
        # Create filename
        filename = yt.video_id + '.' + file_ext

        stream.download(output_path=output_path, filename=filename)
        print("Download completed successfully.")

        # Collect all relevant metadata from the video
        data_dict = {'clip_id': yt.video_id,
                     'clip_file_extension': file_ext,
                     'clip_duration': yt.length,
                     'clip_location': str(output_path)
                     }
        output_file = str(Path(output_path) / filename)

        return data_dict, output_file

    except SystemExit:
        print("Video length over 6 minutes.",
              "Consider downloading another video of shorter duration."
              )
        sys.exit(50)


# %% MAIN
if __name__ == '__main__':
    # SET STATIC ENV
    INGESTION_PATH = Path(env['INGESTION_PATH'])

    url = "https://www.youtube.com/watch?v=X5Qa0oe81tE"
    data = download_video(url, download_path=INGESTION_PATH)
    videos = [str(video.name) for video in INGESTION_PATH.glob("*")]
    print(videos)
