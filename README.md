# Frame-Taker
## Description

The "Frame-Taker" is a Python-based project designed to capture frames from a video and remove duplicate frames, optimizing the process of creating screenshots or benchmarks during application research and testing. This tool provides a convenient and efficient way to analyze recorded video content by extracting unique frames, eliminating redundant information, and generating a more concise representation of the video footage.

The tool is particularly useful for researchers, developers, and testers who record application experiences for evaluation and need a streamlined approach to extract meaningful frames from videos. By automating the frame extraction and deduplication process, users can efficiently generate a concise set of screenshots that accurately represent the application's behavior, making it an essential tool in the field of performance analysis and benchmarking.

## Parameters

* --video -> File video name in the script folder
* --fps -> Number of frames between screenshots
* --optimize -> If it's true, optimize the taken screenshots removing the duplicate ones

## Example

1. Install dependencies running pip3 install -r requirements.txt
2. Move the video into app folder (i.e. puppy_video.mp4)
3. Run the script 'python3 script.py --video puppy_video.mp4 --fps 30 --optimize true'
4. You will see a new folder started with 'screenshots_' with the output

## Author
Lucheti29
