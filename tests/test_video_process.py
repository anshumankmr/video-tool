from video_processor import VideoProcessor
import pytest
import os
import sys
# Add the parent directory to the sys.path so the video_processor module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_download_video():
    """
    Test that the download_video() method
    returns the expected file name based on the video URL.
    """
    # Create a YouTubeDownloader instance with the outtmpl option set to '%(id)s.%(ext)s'
    # This will output the video file with the video ID and format extension.
    # For example, if the video ID is 'wvAWSUTyOJ8', the output file name will be 'wvAWSUTyOJ8.mp4'.
    # The test will pass if the expected file name matches the actual file name.   
    # Create a YouTubeDownloader instance with the outtmpl option set to '%(id)s.%(ext)s'
    # This will output the video file with the video ID and format extension.
    # For example, if the video ID is 'wvAWSUTyOJ8', the output file name will be 'wvAWSUTyOJ8.mp4'.
    # The test will pass if the expected file name matches the actual file name."""
    downloader = VideoProcessor({'outtmpl': '%(id)s.%(ext)s'})
    video_url = 'https://www.youtube.com/watch?v=5FNCukepaS8'
    response = downloader.download_video(video_url)
    print(response)
    assert response["status"] is True and response['file_name'] == '5FNCukepaS8.mp4'

def test_extract_mp3():
    """
    Test that the extract_mp3() method
    returns the expected file name based on the video URL.
    """
    # Create a YouTubeDownloader instance with the outtmpl option set to '%(id)s.%(ext)s'
    # This will output the video file with the video ID and format extension.
    # For example, if the video ID is 'wvAWSUTyOJ8', the output file name will be 'wvAWSUTyOJ8.mp4'.
    # The test will pass if the expected file name matches the actual file name.
    # Create a YouTubeDownloader instance with the outtmpl option set to '%(id)s.%(ext)s'
    # This will output the video file with the video ID and format extension.
    # For example, if the video ID is 'wvAWSUTyOJ8', the output file name will be 'wvAWSUTyOJ8.mp4'.
    # The test will pass if the expected file name matches the actual file name."""
    downloader = VideoProcessor({'outtmpl': '%(id)s.%(ext)s'})
    video_url = '5FNCukepaS8.mp4'
    response = downloader.extract_mp3(video_url)
    print(response)
    assert response == '5FNCukepaS8.mp3'
