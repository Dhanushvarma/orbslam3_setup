# RealSense Stereo SLAM

Camera-pose tracking on an Intel RealSense D435 using ORB-SLAM3 (stereo, via the
infrared pair), with a live [viser](https://viser.studio) web visualization that
shows the current pose and a trail of image-bearing keyframe frustums.

## Layout
| File | Role |
|---|---|
| `config.py` | Tunable parameters (`Config` dataclass) |
| `calibration.py` | Reads IR intrinsics + baseline, writes the ORB-SLAM3 stereo YAML |
| `camera.py` | RealSense stereo IR capture |
| `pose.py` | Pose decomposition helpers (position / quaternion / Euler) |
| `visualizer.py` | viser frustum-history visualizer |
| `run.py` | Entry point + tracking loop |

## Setup

The devcontainer handles all dependency installation.Open the folder in VS Code and **Reopen in Container**.

You also need the ORB-SLAM3 vocabulary file `ORBvoc.txt` (ships with ORB-SLAM3
under `Vocabulary/`, usually gzipped — decompress it). Point `Config.vocab` at
its path.

A USB3 connection is required for dual IR @ 640x480x30; USB privileges are
already set in the devcontainer config.

## Run

```bash
python run.py
```

Open the viser URL it prints (default <http://localhost:8080>). Move the camera
gently in a textured, well-lit scene so stereo tracking can initialize.
