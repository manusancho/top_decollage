

class Api:
    
    url = None
    
    def __init__(self, url):
        self.url = url


class VideoApi(Api):
    
    def get_frame(self, timestamp):
        """
        Return a frame of the video
        @:param timestamp: the timestamp of the frame in seconds from the 
        beginning of the video
        """
        raise NotImplementedError