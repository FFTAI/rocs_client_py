import requests


class Camera:
    """
    Obtain the video stream status and access the video stream.

    Note: This functionality is specific to the `Intel RealSense D435` series. Consider alternative methods for camera access if you are not using this camera model. For other camera types or models, explore appropriate interfaces or libraries that suit your camera hardware and requirements.

    Args:
       baseurl(str):
          The IP address and port of the robot host.

    """

    video_stream_status: bool = None
    """ Indicates whether the `Intel RealSense D435` camera is open. It is set to `True` when the camera is open."""

    video_stream_url: str = None
    """ Provides the address to access the video stream when the `Intel RealSense D435` camera is open."""

    def __init__(self, baseurl: str):
        """
        Initializes the Camera object with the specified robot host address.

        Args:
            baseurl(str):
                the IP address and port of the robot host
        """
        self._baseurl = baseurl
        self.video_stream_status: bool = self._get_video_status()
        if self.video_stream_status:
            self.video_stream_url: str = f'{self._baseurl}/control/camera'

    def _get_video_status(self) -> bool:
        """
        Checks the status of the `Intel RealSense D435` camera.
        """
        response = requests.get(f'{self._baseurl}/control/camera_status')
        if 'data' in response.json():
            return response.json()['data'] is True
        return False
