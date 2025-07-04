#!/bin/sh
# File: start.sh
# Description: Reads settings from /tmp/dct_demo_settings and runs the appropriate GStreamer pipeline.
# If any of the settings are missing, default values are used.

# Set required environment variables
export XDG_RUNTIME_DIR=/var/run/user/0
export WAYLAND_DISPLAY=wayland-1

SETTINGS_FILE="/tmp/dct_demo_settings"

# Default values
DEFAULT_MODEL_PATH="/usr/share/synap/models/object_detection/body_pose/model/yolov8s-pose/model.synap"
DEFAULT_LABEL_FILE="/usr/share/synap/models/object_detection/coco/info.json"
DEFAULT_FRAME_INTERVAL=1
DEFAULT_FPS_DISPLAY=0
DEFAULT_MODE="Play"

# If the settings file exists, read values from it; otherwise, use defaults.
if [ -f "$SETTINGS_FILE" ]; then
  MODEL_PATH=$(sed -n '1p' "$SETTINGS_FILE")
  LABEL_FILE=$(sed -n '2p' "$SETTINGS_FILE")
  FRAME_INTERVAL=$(sed -n '3p' "$SETTINGS_FILE")
  FPS_DISPLAY=$(sed -n '4p' "$SETTINGS_FILE")
  MODE=$(sed -n '5p' "$SETTINGS_FILE")
else
  echo "Settings file not found. Using default values."
fi

# Replace any empty variables with default values.
[ -z "$MODEL_PATH" ] && MODEL_PATH="$DEFAULT_MODEL_PATH"
[ -z "$LABEL_FILE" ] && LABEL_FILE="$DEFAULT_LABEL_FILE"
[ -z "$FRAME_INTERVAL" ] && FRAME_INTERVAL="$DEFAULT_FRAME_INTERVAL"
[ -z "$FPS_DISPLAY" ] && FPS_DISPLAY="$DEFAULT_FPS_DISPLAY"
[ -z "$MODE" ] && MODE="$DEFAULT_MODE"

echo "MODEL_PATH:     $MODEL_PATH"
echo "LABEL_FILE:     $LABEL_FILE"
echo "FRAME_INTERVAL: $FRAME_INTERVAL"
echo "FPS_DISPLAY:    $FPS_DISPLAY"
echo "MODE:           $MODE"

case "$MODE" in
  Play)
    if [ "$FPS_DISPLAY" -eq 1 ]; then
      gst-launch-1.0 v4l2src device=/dev/video8 ! videoconvert ! \
        tee name=t_data t_data. ! queue ! synapoverlay name=overlay label="$LABEL_FILE" ! videoconvert ! \
        fpsdisplaysink text-overlay=true video-sink=waylandsink  t_data. ! queue ! videoconvert ! videoscale ! \
        video/x-raw,width=640,height=384,format=RGB ! synapinfer model="$MODEL_PATH" mode=detector frameinterval="$FRAME_INTERVAL" ! overlay.inference_sink
    else
      gst-launch-1.0 v4l2src device=/dev/video8 ! videoconvert ! \
        tee name=t_data t_data. ! queue ! synapoverlay name=overlay label="$LABEL_FILE" ! videoconvert ! \
        waylandsink fullscreen=true  t_data. ! queue ! videoconvert ! videoscale ! \
        video/x-raw,width=640,height=384,format=RGB ! synapinfer model="$MODEL_PATH" mode=detector frameinterval="$FRAME_INTERVAL" ! overlay.inference_sink
    fi
    ;;
  Record)
    gst-launch-1.0 -e v4l2src device=/dev/video8 ! videoconvert ! \
      tee name=t_data \
      t_data. ! queue ! synapoverlay name=overlay label="$LABEL_FILE" ! \
      tee name=final \
      final. ! queue ! videoconvert ! waylandsink fullscreen=true  \
      t_data. ! queue ! videoconvert ! videoscale ! video/x-raw,width=640,height=384,format=RGB ! \
      synapinfer model="$MODEL_PATH" mode=detector frameinterval="$FRAME_INTERVAL" ! overlay.inference_sink \
      final. ! queue ! videoconvert ! x264enc ! mp4mux ! filesink location="/home/root/video_$(date +%Y-%m-%d_%H-%M-%S).mp4" async=false
    ;;
  *)
    echo "Error: Unknown mode '$MODE'."
    exit 1
    ;;
esac
