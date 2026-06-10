import numpy as np
import pyrealsense2 as rs


class RealSenseStereo:
    """Streams the two infrared imagers (the D435's hardware-rectified stereo pair)."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.pipeline = None

    def start(self):
        self.pipeline = rs.pipeline()
        rscfg = rs.config()
        c = self.cfg
        rscfg.enable_stream(rs.stream.infrared, 1, c.width, c.height, rs.format.y8, c.fps)
        rscfg.enable_stream(rs.stream.infrared, 2, c.width, c.height, rs.format.y8, c.fps)

        profile = self.pipeline.start(rscfg)
        sensor = profile.get_device().first_depth_sensor()
        if sensor.supports(rs.option.emitter_enabled):
            sensor.set_option(rs.option.emitter_enabled, 1 if c.emitter else 0)

        for _ in range(c.warmup_frames):
            self.pipeline.wait_for_frames()

    def read(self, timeout_ms=10000):
        """Return (left, right, timestamp_seconds) or None if a frame is missing."""
        frames = self.pipeline.wait_for_frames(timeout_ms)
        left, right = frames.get_infrared_frame(1), frames.get_infrared_frame(2)
        if not left or not right:
            return None
        return (
            np.asanyarray(left.get_data()),
            np.asanyarray(right.get_data()),
            left.get_timestamp() * 1e-3,  # ms -> s
        )

    def stop(self):
        if self.pipeline:
            self.pipeline.stop()
            self.pipeline = None
