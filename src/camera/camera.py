import platform

import av


class Camera:
    def __init__(self, device=None):

        system = platform.system()
        self.frame = 0
        # self.options =

        if system == "Windows":
            # FFmpeg DirectShow
            self.source = device or "video=Integrated Camera"
            self.options = {"f": "dshow"}

        elif system == "Linux":
            # V4L2
            self.source = device or "/dev/video0"
            self.options = {
                "f": "v4l2",
                "video_size": "1280x720",
                "framerate": "30",
            }

        elif system == "Darwin":
            # AVFoundation
            self.source = device or "0"
            self.options = {"f": "avfoundation"}

        else:
            raise RuntimeError(f"Unsupported platform: {system}")

        self.container = av.open(
            self.source,
            options=self.options,
        )

    def frames(self):
        for frame in self.container.decode(video=0):
            yield frame.to_ndarray(format="rgb24")
            print(f"Frame {self.frame}: ")
            print(f"{frame.width}x{frame.height}")
            self.frame += 1

    def capture(self):
        for frame in self.container.decode(video=0):
            frame.to_image().save(f"{self.frame}-%04d.jpg")
            print(f"{frame}-%04d.jpg -- saved")
            self.frame += 1

    def close(self):
        self.container.close()


camera = Camera()

try:
    #    camera.capture()
    for frame in camera.frames():
        print(frame.shape)
finally:
    camera.close()
