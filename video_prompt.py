import cv2
import base64
import time
from openai import OpenAI
import os
import requests

class VideoPrompt:
    """
    Creates a video prompt object that extracts frames from a video
    and generates a description and voiceover script.
    """
    def __init__(self, api_key, video_path):
        self.api_key = api_key
        self.video_path = video_path
        self.client = OpenAI(api_key=self.api_key)
  
    def extract_frames(self, skip_frames=50):
        """
        Extracts frames from a video.
        Parameters:
        skip_frames (int): The number of frames to skip between each frame.
        Returns:
        list: A list of base64 encoded frames.
        """
        if not os.path.exists(self.video_path):
            raise ValueError("Video path does not exist.")
        if skip_frames <= 0:
            raise ValueError("Skip frames must be greater than 0.")
        if not os.path.isfile(self.video_path):
            raise ValueError("Video path is not a file.")
        if not self.video_path.endswith(".mp4"):
            raise ValueError("Video path is not a valid mp4 file.")
        if not os.path.exists(self.video_path):
            raise ValueError("Video path does not exist.")
        if not os.path.isfile(self.video_path):
            raise ValueError("Video path is not a file.")
        if not self.video_path.endswith(".mp4"):
            raise ValueError("Video path is not a valid mp4 file.")
        video = cv2.VideoCapture(self.video_path)
        base64_frames = []
        frame_count = 0
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            if frame_count % skip_frames == 0:
                _, buffer = cv2.imencode(".jpg", frame)
                base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
            frame_count += 1
        video.release()
        return base64_frames

    def generate_description(self, frames):
        """
        Generates a description for the video.
        Parameters:
        frames (list): A list of base64 encoded frames from the video.
        Returns:
        str: The generated description.
        """
        prompt_messages = [
            {
                "role": "user",
                "content": [
                    "These are frames from a video that I want to upload. Generate a compelling description that I can upload along with the video.",
                    *map(lambda x: {"image": x, "resize": 768}, frames),
                ],
            },
        ]
        params = {
            "model": "gpt-4-vision-preview",
            "messages": prompt_messages,
            "max_tokens": 200,
        }

        result = self.client.chat.completions.create(**params)
        return result.choices[0].message.content
   
    def generate_voiceover_script(self, frames):
        """
        Generates a voiceover script for the video.
        Parameters:
        frames (list): A list of base64 encoded frames from the video.
        Returns:
        str: The generated voiceover script.
        """
        # Use the following code if you want to use the OpenAI API to generate the voiceover script.
        prompt_messages = [
            {
                "role": "user",
                "content": [
                    "These are frames of a video. Create a short voiceover script in the style of David Attenborough. Only include the narration.",
                    *map(lambda x: {"image": x, "resize": 768}, frames),
                ],
            },
        ]
        params = {
            "model": "gpt-4-vision-preview",
            "messages": prompt_messages,
            "max_tokens": 500,
        }
        result = self.client.chat.completions.create(**params)
        return result.choices[0].message.content
    
    def generate_voiceover_audio(self, script):
        """
        Generate Voiceover audio for the video.
        Parameters:
        script (str): The voiceover script.
        Returns:
        bytes: The generated audio.
        """
        response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {self.api_key}",
            },
            json={
                "model": "tts-1-1106",
                "input": script,
                "voice": "onyx",
            },
            timeout=10000
        )
        audio = b""
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            audio += chunk
        return audio