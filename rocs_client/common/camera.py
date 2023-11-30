import requests


class Camera:
    """
    Obtain the video stream status and video stream

    ``Attention! This is not necessary!
    get you have a better solution to get the camera, this case only applies to the `Intel Real Sence D435` series``

    Args:
        baseurl(str):
            This address is the ip:port address of the robot host
    """

    video_stream_status: bool = None
    """ When `intel real sence D435` Camera is Opened! It it Ture."""

    video_stream_url: str = None
    """ When `intel real sence D435` Camera is Opened! You will be given an address to get the video stream."""

    def __init__(self, baseurl: str):
        """
        When Rocs gets the `intel real sence D435` Camera signal
        You will be given an address to get the video stream,
        You can access the video stream through http requests

        Args:
            baseurl(str):
                This address is the ip:port address of the robot host
        """
        self._baseurl = baseurl
        self.video_stream_status: bool = self._get_video_status()
        if self.video_stream_status:
            self.video_stream_url: str = f'{self._baseurl}/control/camera'

    def _get_video_status(self) -> bool:
        """
        Check the `intel real sence D435` Camera status
        """
        response = requests.get(f'{self._baseurl}/control/camera_status')
        if 'data' in response.json():
            return response.json()['data'] is True
        return False
