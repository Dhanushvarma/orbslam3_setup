import numpy as np
import orbslam3

from config import Config
from calibration import export_settings
from camera import RealSenseStereo
from pose import pose_components
from visualizer import SlamVisualizer


def main():
    cfg = Config()

    # 1. Read intrinsics from the camera and write the settings file
    #    (device is released before the slow vocabulary load).
    fx = export_settings(cfg)

    # 2. Load ORB-SLAM3 (vocabulary load is the slow step).
    print("loading SLAM (vocabulary)...")
    slam = orbslam3.system(cfg.vocab, cfg.settings, orbslam3.Sensor.STEREO)
    slam.initialize()

    # 3. Start the web visualizer (prints its own URL, default :8080).
    viz = SlamVisualizer(cfg, fx)

    # 4. Start streaming and run the tracking loop.
    cam = RealSenseStereo(cfg)
    cam.start()
    try:
        while True:
            frame = cam.read()
            if frame is None:
                continue
            left, right, t = frame
            slam.process_image_stereo(left, right, t)

            if slam.get_tracking_state() == orbslam3.TrackingState.OK:
                Twc = np.linalg.inv(np.asarray(slam.get_current_pose()))
                pos, _, rpy = pose_components(Twc)
                viz.update(Twc, image=left)
                print(f"pos[{pos[0]:+.3f} {pos[1]:+.3f} {pos[2]:+.3f}]  "
                      f"rpy[{rpy[0]:+6.1f} {rpy[1]:+6.1f} {rpy[2]:+6.1f}]")
            else:
                print("tracking:", slam.get_tracking_state())
    except KeyboardInterrupt:
        pass
    finally:
        slam.shutdown()
        cam.stop()


if __name__ == "__main__":
    main()