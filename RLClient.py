from xbox.nano.render.client.base import Client
from xbox.nano.render.sink import Sink
from xbox.nano.enum import VideoCodec
from xbox.nano.render.codec import FrameDecoder

import threading
import time


class RLClient(Client):
    def __init__(self, width, height):
        self._video_render = RLVideoRenderer(width, height)
        super(RLClient, self).__init__(
            self._video_render,
            Sink(),
            Sink()
        )


class RLVideoRenderer(Sink):
    TITLE = 'Nano RL no render'

    def __init__(self, width, height):
        self._decoder = None
        self._last_frame = None
        self._last_frame_time = time.time()
        self._lock = threading.Lock()

    def open(self, client):
        pass

    def close(self):
        pass

    def setup(self, fmt):
        if fmt.codec == VideoCodec.H264:
            pass
        elif fmt.codec == VideoCodec.YUV:
            raise TypeError("YUV format not implemented")
        elif fmt.codec == VideoCodec.RGB:
            raise TypeError("RGB format not implemented")
        else:
            raise TypeError("Unknown video codec: %d" % fmt.codec)
        self._decoder = FrameDecoder.video(fmt.codec)

    def render(self, data):
        try:
            frames = self._decoder.decode(data)
            if len(frames) > 0:
                self._lock.acquire()
                self._last_frame = frames[-1]
                self._lock.release()
                t = time.time()
                print("{:.2f} FPS {} frames".format(1/(t - self._last_frame_time), len(frames)))
                self._last_frame_time = t
        except Exception as e:
            print(e)

    def pump(self):
        pass

    def get_last_frame_np(self):
        self._lock.acquire()
        im = self._last_frame.to_ndarray()
        self._lock.release()
        return im


