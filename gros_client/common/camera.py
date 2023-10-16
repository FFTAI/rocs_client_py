from typing import Dict, Any

import requests


class Camera:
    """ 相机

    用于获取视频流状态和视频流
    """

    video_stream_status: bool = None
    video_stream_url: str = None

    def __init__(self, baseurl: str):
        self._baseurl = baseurl
        self.video_stream_status: bool = self._get_video_status()
        if self.video_stream_status:
            self.video_stream_url: str = f'{self._baseurl}/control/camera'

    def _get_video_status(self) -> bool:
        response = requests.get(f'{self._baseurl}/control/camera_status')
        if 'data' in response.json():
            return response.json()['data'] == True
        return False
