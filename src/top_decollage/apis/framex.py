import logging
import requests
import urllib.parse

from .common import VideoApi

logger = logging.getLogger("top_decollage.analyzer")


FRAME_X_API_URL = "https://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/"


class FrameXApi(VideoApi):
    
    frames = None
    
    def __init__(self, context):
        super().__init__(FRAME_X_API_URL)
        if "frames" not in context:
            self.frames = self.get_frames()
            context['frames'] = self.frames

    def get_frames(self) -> int:
        """
        Return number of frames in the video
        """
        if self.frames:
            return self.frames
        else:
            req = requests.get(self.url)
            assert req.status_code == 200
            data = req.json()
            assert data["frames"]        
            return int(data["frames"])

    def get_frame(self, frame=0) -> str:
        """
        Return a url of a given frame of the video
        @:param frame: the frame number from the 
        beginning of the video
        @return a requests object
        """
        return urllib.parse.urljoin(
            self.url,
            'frame/%s' % str(frame),
        )
    