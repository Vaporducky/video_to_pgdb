#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 20:04:41 2023

Split a video into multiple parts using moviepy package [1].In particular the
class [2] has been used

REFERENCES
[1] https://pypi.org/project/moviepy/
[2] https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html#videofileclip

@author: elianther
"""

# %% IMPORT PACKAGES
from pathlib import Path
from datetime import datetime
from moviepy.editor import VideoFileClip
# %% MAIN LOGIC


def video_splitter(source_file_path, output_path, segment_duration=60):
    # Create object
    try:
        video_clip = VideoFileClip(source_file_path)
    except OSError as e:
        print(e)

    # Extract all relevant attributes from object
    stem = str(Path(video_clip.filename).stem)  # Only name not extension
    filename = str(Path(video_clip.filename).name)
    duration = video_clip.duration
    fps = video_clip.fps

    # Create output path
    date = datetime.now().strftime('%Y%m%d')
    output_folder = Path(output_path).joinpath(date).joinpath(stem)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Iterate over n partitions
    iterations = int(duration // segment_duration)
    for k in range(iterations + 1):
        frame_name = int(k * fps * segment_duration)
        segment_name = f"{frame_name}-{filename}"

        # Final step should be length of the video
        if k == iterations:
            clip = video_clip.subclip(k * segment_duration,
                                      video_clip.duration)
        else:
            clip = video_clip.subclip(k * segment_duration,
                                      (k+1) * segment_duration)

        # Write video segment to output directory
        output_filename = output_folder.joinpath(segment_name)
        clip.write_videofile(str(output_filename),
                             codec="libx264",  # Standard codec for .mp4
                             temp_audiofile='temp-audio.m4a',
                             )
