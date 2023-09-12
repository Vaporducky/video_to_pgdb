#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 20:04:41 2023

Split a video into multiple parts using moviepy package:
                    https://pypi.org/project/moviepy/
In particular the class [2] has been used


[2] https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html#videofileclip
@author: elianther
"""

# %% IMPORT PACKAGES
from pathlib import Path
from moviepy.editor import VideoFileClip
# %% MAIN LOGIC


def video_splitter(file_path, target_dir, segment_duration=60):
    video_clip = VideoFileClip(file_path)
    # Extract all relevant attributes from object
    filename = str(Path(video_clip.filename).name)
    duration = video_clip.duration
    fps = video_clip.fps

    # Create a folder within output path
    output_folder = Path(target_dir).joinpath("segmented_video")
    try:
        output_folder.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        print("Output directory exists. Purge before reprocess.")

    # Iterate over n partitions
    iterations = int(video_clip.duration // segment_duration)
    for k in range(iterations + 1):

        if k == iterations:
            segment_name = f"{round(duration * fps)}-{filename}"
            clip = video_clip.subclip(k * segment_duration,
                                      video_clip.duration
                                      )
        else:
            frame_name = int(k * fps * segment_duration)
            segment_name = f"{frame_name}-{filename}"
            clip = video_clip.subclip(k * segment_duration,
                                      (k+1) * segment_duration
                                      )

        # Write video segment to output directory
        output_filename = output_folder.joinpath(segment_name)
        clip.write_videofile(str(output_filename),
                             codec="libx264",  # Standard codec for .mp4
                             temp_audiofile='temp-audio.m4a',
                             )

# =============================================================================
#     while True:
#         endPos = startPos + segment_duration
#
#         if endPos > fullDura:
#             endPos = fullDura
#
#         clip = video_clip.subclip(startPos, endPos)
#
#         filename = str(Path(video_clip.filename).name)
#         segment_name = f"{i * fps * segment_duration}-{filename}.mp4"
#         output_filename = output_folder.joinpath(
#             segment_name + f"_{video_name}")
#
#         clip.write_videofile(str(output_filename),
#                              codec="libx264",  # Standard codec for .mp4
#                              temp_audiofile='temp-audio.m4a',
#                              )
#         print("part ", i, "done")
#         i += 1
#
#         startPos = endPos  # jump to next clip
#
#         if startPos >= fullDura:
#             break
# =============================================================================
