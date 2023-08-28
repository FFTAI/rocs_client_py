from typing import Dict, Any

import requests


class Camera:

    video_stream_status: bool = None

    def __init__(self, baseurl: str):
        self._baseurl = baseurl
        self.video_stream_url = f'{self._baseurl}/control/camera'
        if self.video_stream_status is None:
            self.video_stream_status = self._get_video_status().get('data')

    def _get_video_status(self) -> Dict[str, Any]:
        response = requests.get(f'{self._baseurl}/control/camera_status')
        return response.json()
