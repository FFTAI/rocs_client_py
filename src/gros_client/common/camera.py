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
        self.video_stream_status: bool = self._get_video_status().get('data')
        if self.video_stream_status:
            self.video_stream_url: str = f'{self._baseurl}/control/camera'

    def _get_video_status(self) -> Dict[str, Any]:
        response = requests.get(f'{self._baseurl}/control/camera_status')
        return response.json()
