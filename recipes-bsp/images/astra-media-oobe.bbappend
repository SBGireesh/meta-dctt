IMAGE_INSTALL:append:dolphin = " \
    gstreamer1.0-plugins-bad \
	python3-pyqt5 \
	python3-evdev \
	python3-pyudev \
	thermal-detect-demo \
"

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += "file://dctk-syns-sw-version"

ROOTFS_POSTPROCESS_COMMAND += "add_dct_sw_version_file;"

add_dct_sw_version_file () {
	install -d ${IMAGE_ROOTFS}/etc
	install -m 0644 ${WORKDIR}/dctk-syns-sw-version ${IMAGE_ROOTFS}/etc/dctk-syns-sw-version
}
