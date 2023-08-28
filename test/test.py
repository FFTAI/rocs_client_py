from src.gros_client import *

human = robot.Human()

video_stream_status: bool = human.camera.video_stream_status
print(video_stream_status)
