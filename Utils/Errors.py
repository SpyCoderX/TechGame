class ImageError(Exception):
    def __init__(self,message) -> None:
        super().__init__(self.f(message))
    def f(self,m):
        return "ImageError: "+m

class ImageLoadError(ImageError):
    def f(self, m):
        return "ImageLoadingError: "+m