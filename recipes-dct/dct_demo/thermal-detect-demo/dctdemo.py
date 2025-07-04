import os
os.environ["XDG_RUNTIME_DIR"] = "/var/run/user/0"
os.environ["WAYLAND_DISPLAY"] = "wayland-1"

import sys
import signal
import subprocess
import asyncio
import evdev
import pyudev
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QCheckBox, QPushButton, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import QThread, pyqtSignal

class GStreamerConfigUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCT Thermal Camera AI Demo")
        self.setGeometry(100, 100, 400, 250)

        self.categories_all = {
            "Object Detection": {
                "Body Pose - yolov8s-pose": (
                    "/usr/share/synap/models/object_detection/body_pose/model/yolov8s-pose/model.synap", None
                ),
                "People - mobilenet224_full1": (
                    "/usr/share/synap/models/object_detection/people/model/mobilenet224_full1/model.synap",
                    "/usr/share/synap/models/object_detection/people/info.json"
                ),
                "COCO - yolov8s-640x384": (
                    "/usr/share/synap/models/object_detection/coco/model/yolov8s-640x384/model.synap",
                    "/usr/share/synap/models/object_detection/coco/info.json"
                ),
                "COCO - mobilenet224_full80": (
                    "/usr/share/synap/models/object_detection/coco/model/mobilenet224_full80/model.synap",
                    "/usr/share/synap/models/object_detection/coco/info.json"
                ),
                "Face - yolov5s_face_640x480_onnx_mq": (
                    "/usr/share/synap/models/object_detection/face/model/yolov5s_face_640x480_onnx_mq/model.synap",
                    "/usr/share/synap/models/object_detection/face/info.json"
                )
            },
            "Image Processing": {
                "Sublima": (
                    "/usr/share/synap/models/image_processing/sublima/model/model.synap", None
                ),
                "Super Resolution - sr_qdeo_y_uv_640x360_1920x1080": (
                    "/usr/share/synap/models/image_processing/super_resolution/model/sr_qdeo_y_uv_640x360_1920x1080/model.synap", None
                ),
                "Super Resolution - sr_fast_y_uv_1920x1080_3840x2160": (
                    "/usr/share/synap/models/image_processing/super_resolution/model/sr_fast_y_uv_1920x1080_3840x2160/model.synap", None
                ),
                "Super Resolution - sr_qdeo_y_uv_1280x720_3840x2160": (
                    "/usr/share/synap/models/image_processing/super_resolution/model/sr_qdeo_y_uv_1280x720_3840x2160/model.synap", None
                ),
                "Super Resolution - sr_fast_y_uv_1280x720_3840x2160": (
                    "/usr/share/synap/models/image_processing/super_resolution/model/sr_fast_y_uv_1280x720_3840x2160/model.synap", None
                ),
                "Super Resolution - sr_fast_y_uv_960x540_3840x2160": (
                    "/usr/share/synap/models/image_processing/super_resolution/model/sr_fast_y_uv_960x540_3840x2160/model.synap", None
                ),
                "Super Resolution - sr_qdeo_y_uv_1920x1080_3840x2160": (
                    "/usr/share/synap/models/image_processing/super_resolution/model/sr_qdeo_y_uv_1920x1080_3840x2160/model.synap", None
                ),
                "Super Resolution - sr_qdeo_y_uv_960x540_3840x2160": (
                    "/usr/share/synap/models/image_processing/super_resolution/model/sr_qdeo_y_uv_960x540_3840x2160/model.synap", None
                ),
                "Sharpen": (
                    "/usr/share/synap/models/image_processing/sharpen/model/640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@1280x720_rgb@224x224": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@1280x720_rgb@224x224/model.synap", None
                ),
                "Preprocess - convert_nv12@7680x4320_rgb@640x360": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@7680x4320_rgb@640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@1280x720_rgb@640x360": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@1280x720_rgb@640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@2560x1440_rgb@1920x1080": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@2560x1440_rgb@1920x1080/model.synap", None
                ),
                "Preprocess - convert_nv12@2560x1440_rgb@224x224": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@2560x1440_rgb@224x224/model.synap", None
                ),
                "Preprocess - convert_nv12@854x480_rgb@640x360": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@854x480_rgb@640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@426x240_rgb@640x360": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@426x240_rgb@640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@640x360_rgb@1920x1080": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@640x360_rgb@1920x1080/model.synap", None
                ),
                "Preprocess - convert_nv12@1920x1080_rgb@640x360": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@1920x1080_rgb@640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@2560x1440_rgb@640x360": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@2560x1440_rgb@640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@1920x1080_rgb@224x224": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@1920x1080_rgb@224x224/model.synap", None
                ),
                "Preprocess - convert_nv12@7680x4320_rgb@224x224": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@7680x4320_rgb@224x224/model.synap", None
                ),
                "Preprocess - convert_nv12@426x240_rgb@1920x1080": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@426x240_rgb@1920x1080/model.synap", None
                ),
                "Preprocess - convert_nv12@1920x1080_rgb@1920x1080": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@1920x1080_rgb@1920x1080/model.synap", None
                ),
                "Preprocess - convert_nv12@854x480_rgb@224x224": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@854x480_rgb@224x224/model.synap", None
                ),
                "Preprocess - convert_nv12@640x360_rgb@224x224": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@640x360_rgb@224x224/model.synap", None
                ),
                "Preprocess - convert_nv12@3840x2160_rgb@640x360": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@3840x2160_rgb@640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@7680x4320_rgb@1920x1080": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@7680x4320_rgb@1920x1080/model.synap", None
                ),
                "Preprocess - convert_nv12@426x240_rgb@224x224": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@426x240_rgb@224x224/model.synap", None
                ),
                "Preprocess - convert_nv12@1280x720_rgb@1920x1080": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@1280x720_rgb@1920x1080/model.synap", None
                ),
                "Preprocess - convert_nv12@854x480_rgb@1920x1080": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@854x480_rgb@1920x1080/model.synap", None
                ),
                "Preprocess - convert_nv12@3840x2160_rgb@1920x1080": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@3840x2160_rgb@1920x1080/model.synap", None
                ),
                "Preprocess - convert_nv12@640x360_rgb@640x360": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@640x360_rgb@640x360/model.synap", None
                ),
                "Preprocess - convert_nv12@3840x2160_rgb@224x224": (
                    "/usr/share/synap/models/image_processing/preprocess/model/convert_nv12@3840x2160_rgb@224x224/model.synap", None
                )
            },
            "Object Recognition": {
                "Face - arcface_quant": (
                    "/usr/share/synap/models/object_recognition/face/model/arcface_quant/model.synap", None
                )
            },
            "Image Classification": {
                "Imagenet - mobilenet_v1_0.25_224_quant": (
                    "/usr/share/synap/models/image_classification/imagenet/model/mobilenet_v1_0.25_224_quant/model.synap",
                    "/usr/share/synap/models/image_classification/imagenet/info.json"
                ),
                "Imagenet - mobilenet_v1_0.25_224_quant_cpu": (
                    "/usr/share/synap/models/image_classification/imagenet/model/mobilenet_v1_0.25_224_quant_cpu/model.synap",
                    "/usr/share/synap/models/image_classification/imagenet/info.json"
                ),
                "Imagenet - mobilenet_v1_0.25_224_quant_gpu": (
                    "/usr/share/synap/models/image_classification/imagenet/model/mobilenet_v1_0.25_224_quant_gpu/model.synap",
                    "/usr/share/synap/models/image_classification/imagenet/info.json"
                ),
                "Imagenet - mobilenet_v1_0.25_224_quant_profiling": (
                    "/usr/share/synap/models/image_classification/imagenet/model/mobilenet_v1_0.25_224_quant_profiling/model.synap",
                    "/usr/share/synap/models/image_classification/imagenet/info.json"
                ),
                "Imagenet - mobilenet_v2_1.0_224_quant": (
                    "/usr/share/synap/models/image_classification/imagenet/model/mobilenet_v2_1.0_224_quant/model.synap",
                    "/usr/share/synap/models/image_classification/imagenet/info.json"
                ),
                "Imagenet - mobilenet_v2_12_onnx_quant_cpu": (
                    "/usr/share/synap/models/image_classification/imagenet/model/mobilenet_v2_12_onnx_quant_cpu/model.synap",
                    "/usr/share/synap/models/image_classification/imagenet/info.json"
                ),
                "TV Logo - tvlogo_mobilenetv2_ptq": (
                    "/usr/share/synap/models/image_classification/tv_logo/model/tvlogo_mobilenetv2_ptq/model.synap",
                    "/usr/share/synap/models/image_classification/tv_logo/info.json"
                ),
                "Blur - blur_quant": (
                    "/usr/share/synap/models/image_classification/blur/model/blur_quant/model.synap",
                    "/usr/share/synap/models/image_classification/blur/info.json"
                ),
                "TV Ads - tvads_mobilenetv2_ptq": (
                    "/usr/share/synap/models/image_classification/tv_ads/model/tvads_mobilenetv2_ptq/model.synap",
                    "/usr/share/synap/models/image_classification/tv_ads/info.json"
                )
            }
        }
        default_subset = {
            "Object Detection": {
                "Body Pose - yolov8s-pose": (
                    "/usr/share/synap/models/object_detection/body_pose/model/yolov8s-pose/model.synap", None
                ),
                "COCO - yolov8s-640x384": (
                    "/usr/share/synap/models/object_detection/coco/model/yolov8s-640x384/model.synap",
                    "/usr/share/synap/models/object_detection/coco/info.json"
                ),
                "Face - yolov5s_face_640x480_onnx_mq": (
                    "/usr/share/synap/models/object_detection/face/model/yolov5s_face_640x480_onnx_mq/model.synap",
                    "/usr/share/synap/models/object_detection/face/info.json"
                )
            }
        }
        if len(sys.argv) > 1 and sys.argv[1] == "all":
            self.categories = self.categories_all
        else:
            self.categories = default_subset

        layout = QVBoxLayout()

        category_layout = QHBoxLayout()
        category_label = QLabel("Select Category:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories.keys())
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)

        model_layout = QHBoxLayout()
        model_label = QLabel("Select Model:")
        self.model_combo = QComboBox()
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)

        self.category_combo.currentIndexChanged.connect(self.update_model_combo)
        self.update_model_combo()

        self.frame_label = QLabel("Frame Interval:")
        self.frame_spinbox = QSpinBox()
        self.frame_spinbox.setRange(1, 30)
        layout.addWidget(self.frame_label)
        layout.addWidget(self.frame_spinbox)

        self.fps_checkbox = QCheckBox("Enable FPS Display")
        layout.addWidget(self.fps_checkbox)
        self.fps_checkbox_prev_state = self.fps_checkbox.isChecked()

        radio_layout = QHBoxLayout()
        self.radio_label = QLabel("Mode:")
        self.play_radio = QRadioButton("Play")
        self.record_radio = QRadioButton("Record")
        self.play_radio.setChecked(True)
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.play_radio)
        self.radio_group.addButton(self.record_radio)
        radio_layout.addWidget(self.radio_label)
        radio_layout.addWidget(self.play_radio)
        radio_layout.addWidget(self.record_radio)
        layout.addLayout(radio_layout)

        self.record_radio.toggled.connect(self.on_record_toggled)
        self.play_radio.toggled.connect(self.on_play_toggled)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_demo)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        self.evdev_listener = EvdevListener()
        self.evdev_listener.quitKeyPressed.connect(self.handle_quit_key)
        self.evdev_listener.start()

        self.verify_files()

    def update_model_combo(self):
        self.model_combo.clear()
        category = self.category_combo.currentText()
        models = self.categories.get(category, {})
        self.model_combo.addItems(models.keys())

    def on_record_toggled(self, checked):
        if checked:
            self.fps_checkbox_prev_state = self.fps_checkbox.isChecked()
            self.fps_checkbox.setChecked(False)
            self.fps_checkbox.setEnabled(False)

    def on_play_toggled(self, checked):
        if checked:
            self.fps_checkbox.setEnabled(True)
            self.fps_checkbox.setChecked(self.fps_checkbox_prev_state)

    def start_demo(self):
        category = self.category_combo.currentText()
        model_name = self.model_combo.currentText()
        model_entry = self.categories.get(category, {}).get(model_name, (None, None))
        model_path, label_file = model_entry
        if model_path is None:
            print("No model selected.")
            return
        if label_file is None:
            label_file = "/usr/share/synap/models/object_detection/coco/info.json"
        frame_interval = self.frame_spinbox.value()
        fps_display = 1 if self.fps_checkbox.isChecked() else 0
        mode = "Play" if self.play_radio.isChecked() else "Record"
        settings_path = "/tmp/dct_demo_settings"
        with open(settings_path, "w") as f:
            f.write(f"{model_path}\n{label_file}\n{frame_interval}\n{fps_display}\n{mode}\n")
        subprocess.run(["systemctl", "start", "dctdemo.service"])
        self.start_button.setText("Stop")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.stop_demo)

    def stop_demo(self):
        subprocess.run(["systemctl", "stop", "dctdemo.service"])
        self.start_button.setText("Start")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.start_demo)

    def handle_quit_key(self):
        print("Quit key pressed. Stopping demo if running.")
        if self.start_button.text() == "Stop":
            self.stop_demo()

    def verify_files(self):
        for category, models in self.categories.items():
            for model_name, (model_path, label_file) in models.items():
                if not os.path.exists(model_path):
                    print(f"Warning: Model file '{model_path}' for '{model_name}' in category '{category}' does not exist.")
                if label_file is not None and not os.path.exists(label_file):
                    print(f"Warning: Label file '{label_file}' for '{model_name}' in category '{category}' does not exist.")
        default_label = "/usr/share/synap/models/object_detection/coco/info.json"
        if not os.path.exists(default_label):
            print(f"Warning: Default label file '{default_label}' does not exist.")

class EvdevListener(QThread):
    quitKeyPressed = pyqtSignal()

    async def read_events(self, device):
        try:
            async for event in device.async_read_loop():
                if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                    key_event = evdev.categorize(event)
                    if key_event.keycode == "BTN_RIGHT":
                        print(f"Detected right mouse click: {key_event.keycode}")
                        self.quitKeyPressed.emit()
        except (asyncio.CancelledError, OSError) as e:
            if isinstance(e, OSError) and e.errno == 19:
                print(f"Device {device.path} removed.")
            else:
                print(f"Error in read_events: {e}")

    async def hotplug_loop(self, monitor):
        loop = asyncio.get_event_loop()
        while True:
            try:
                dev_event = await loop.run_in_executor(None, monitor.poll, 1)
            except RuntimeError as e:
                print("Hotplug loop runtime error:", e)
                break
            if dev_event is None or dev_event.device_node is None:
                continue
            if dev_event.action == "add":
                try:
                    path = dev_event.device_node
                    new_device = evdev.InputDevice(path)
                    capabilities = new_device.capabilities()
                    if evdev.ecodes.EV_REL in capabilities and evdev.ecodes.EV_KEY in capabilities:
                        keycodes = capabilities[evdev.ecodes.EV_KEY]
                        if evdev.ecodes.BTN_LEFT in keycodes and evdev.ecodes.BTN_RIGHT in keycodes:
                            if path not in self.mouse_tasks:
                                task = asyncio.create_task(self.read_events(new_device))
                                self.mouse_tasks[path] = task
                                print(f"Hotplug: Added mouse {new_device.name} ({path})")
                except Exception as e:
                    print(f"Error adding device {dev_event.device_node}: {e}")
            elif dev_event.action == "remove":
                path = dev_event.device_node
                if path in self.mouse_tasks:
                    task = self.mouse_tasks.pop(path)
                    task.cancel()
                    print(f"Hotplug: Removed mouse {path}")

    async def main(self):
        self.mouse_tasks = {}
        for path in evdev.list_devices():
            try:
                device = evdev.InputDevice(path)
                capabilities = device.capabilities()
                if evdev.ecodes.EV_REL in capabilities and evdev.ecodes.EV_KEY in capabilities:
                    keycodes = capabilities[evdev.ecodes.EV_KEY]
                    if evdev.ecodes.BTN_LEFT in keycodes and evdev.ecodes.BTN_RIGHT in keycodes:
                        task = asyncio.create_task(self.read_events(device))
                        self.mouse_tasks[device.path] = task
                        print(f"Detected mouse: {device.name} ({device.path})")
            except Exception as e:
                print(f"Error reading device {path}: {e}")
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by("input")
        hotplug_task = asyncio.create_task(self.hotplug_loop(monitor))
        await asyncio.gather(*self.mouse_tasks.values(), hotplug_task)

    def run(self):
        try:
            asyncio.run(self.main())
        except Exception as e:
            print("Evdev listener exception:", e)

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GStreamerConfigUI()
    window.show()
    sys.exit(app.exec_())
