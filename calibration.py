import pyrealsense2 as rs


def _write_yaml(path, cfg, K1, K2, baseline):
    with open(path, "w") as f:
        f.write(f"""%YAML:1.0
File.version: "1.0"
Camera.type: "PinHole"

Camera1.fx: {K1.fx}
Camera1.fy: {K1.fy}
Camera1.cx: {K1.ppx}
Camera1.cy: {K1.ppy}
Camera1.k1: 0.0
Camera1.k2: 0.0
Camera1.p1: 0.0
Camera1.p2: 0.0

Camera2.fx: {K2.fx}
Camera2.fy: {K2.fy}
Camera2.cx: {K2.ppx}
Camera2.cy: {K2.ppy}
Camera2.k1: 0.0
Camera2.k2: 0.0
Camera2.p1: 0.0
Camera2.p2: 0.0

Camera.width: {cfg.width}
Camera.height: {cfg.height}
Camera.fps: {cfg.fps}
Camera.RGB: 1

Stereo.ThDepth: 40.0
Stereo.b: {baseline:.6f}
Stereo.T_c1_c2: !!opencv-matrix
   rows: 4
   cols: 4
   dt: f
   data: [1.0, 0.0, 0.0, {baseline:.6f}, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

ORBextractor.nFeatures: 1200
ORBextractor.scaleFactor: 1.2
ORBextractor.nLevels: 8
ORBextractor.iniThFAST: 20
ORBextractor.minThFAST: 7

Viewer.KeyFrameSize: 0.05
Viewer.KeyFrameLineWidth: 1.0
Viewer.GraphLineWidth: 0.9
Viewer.PointSize: 2.0
Viewer.CameraSize: 0.08
Viewer.CameraLineWidth: 3.0
Viewer.ViewpointX: 0.0
Viewer.ViewpointY: -0.7
Viewer.ViewpointZ: -3.5
Viewer.ViewpointF: 500.0
""")


def export_settings(cfg):
    """Briefly open the camera to read IR intrinsics + baseline, write the YAML,
    then fully release the device. Releasing here is what prevents the frame
    timeout that otherwise happens while the (slow) vocabulary loads.

    Returns the left-camera fx, used later to set the viser frustum FoV.
    """
    pipeline = rs.pipeline()
    rscfg = rs.config()
    rscfg.enable_stream(rs.stream.infrared, 1, cfg.width, cfg.height, rs.format.y8, cfg.fps)
    rscfg.enable_stream(rs.stream.infrared, 2, cfg.width, cfg.height, rs.format.y8, cfg.fps)

    profile = pipeline.start(rscfg)
    ir1 = profile.get_stream(rs.stream.infrared, 1).as_video_stream_profile()
    ir2 = profile.get_stream(rs.stream.infrared, 2).as_video_stream_profile()
    K1, K2 = ir1.get_intrinsics(), ir2.get_intrinsics()
    baseline = abs(ir1.get_extrinsics_to(ir2).translation[0])  # meters
    pipeline.stop()

    _write_yaml(cfg.settings, cfg, K1, K2, baseline)
    print(f"settings: fx={K1.fx:.1f} cx={K1.ppx:.1f} baseline={baseline * 1000:.1f}mm")
    return K1.fx
