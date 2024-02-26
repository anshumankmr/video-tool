"""
This module provides functionality to download videos 
from YouTube using the youtube-dl library.
It defines a VideoProcessor class that allows 
for downloading videos with custom options and hooks 
for post-download processing. 
The class supports specifying youtube-dl options upon
 initialization and offers a method to download videos byURL.
"""
import youtube_dl
from urllib.parse import urlparse, parse_qs
from contextlib import suppress
from moviepy.editor import VideoFileClip

class VideoProcessor:
    """
    A class to download YouTube videos using youtube-dl.
    Attributes:
        ydl_opts (dict): 
        A dictionary containing options for youtube-dl. Options include output template
         and progress hooks.
        file_name (str):
        The name of the downloaded file. It is updated during the
          download process via a custom hook.

    Methods:
        __init__(options=None):
          Initializes the VideoProcessor with specified options for youtube-dl.
        download_video(video_url): 
        Downloads the video from the specified URL and returns the download status and file name.
    """
    def my_hook(self,d):
        """Custom Hook"""
        print("final filename", d.get('filename'))
        if d['status'] == 'finished':
            print('Done downloading, now post-processing ...')
            # self.file_name = d.get('filename')

    def __init__(self, options=None):
        if options is None:
            options = {'outtmpl': '%(id)s.%(ext)s',
                           'progress_hooks': [self.my_hook],}
        self.ydl_opts = options
        self.file_name = None
    def get_yt_id(self, url, ignore_playlist=False):
        """ Examples:
        # - http://youtu.be/SA2iWivDJiE
        # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        # - http://www.youtube.com/embed/SA2iWivDJiE
        # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        4"""
        query = urlparse(url)
        if query.hostname == 'youtu.be': return query.path[1:]
        if query.hostname in {'www.youtube.com', 'youtube.com', 'music.youtube.com'}:
            if not ignore_playlist:
            # use case: get playlist id not current video in playlist
                with suppress(KeyError):
                    return parse_qs(query.query)['list'][0]
            if query.path == '/watch': return parse_qs(query.query)['v'][0]
            if query.path[:7] == '/watch/': return query.path.split('/')[1]
            if query.path[:7] == '/embed/': return query.path.split('/')[2]
            if query.path[:3] == '/v/': return query.path.split('/')[2]
        return None # for invalid YouTube url


    def download_video(self, video_url):
        """
        Downloads the video from the given URL.

        Parameters:
        video_url (str): The URL of the YouTube video to download.

        Returns:
        None
        """
        try:
            # Create a youtube-dl instance with the given options
            ydl = youtube_dl.YoutubeDL(self.ydl_opts)
            # Download the video
            ydl.download([video_url])
            return {"status": True, "message": "Video downloaded successfully", 
                    "file_name": f"{self.get_yt_id(video_url)}.mp4"}
        except Exception as e:
            print(f"Error downloading video: {e}")
            return {"status": False, "message": str(e)}

    def extract_mp3(self, mp4_file_path):
        """
        Extract MP3
        """
        try:
            video = VideoFileClip(mp4_file_path)
            output_audio_path = f"{mp4_file_path.split('.')[0]}.mp3"
            video.audio.write_audiofile(output_audio_path, codec='libmp3lame')
            return output_audio_path
        except:
            return None