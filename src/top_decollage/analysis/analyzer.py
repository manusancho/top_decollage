
class Analyzer(object):
    """
    Pattern class to implement analyzers.
    """
    def is_found(self, tolerance=0) -> bool:
        """
        Return whether the target image has been found.
        """
        raise NotImplementedError("Method is_found() is not implemented")
        
    def get_next(self) -> str:
        """
        Return the url of the next frame to show the user
        """
        raise NotImplementedError("Method get_next() is not implemented")
    
    def restart(self):
        """
        Reset internal status.
        """
        raise NotImplementedError("Method restart() is not implemented")
    