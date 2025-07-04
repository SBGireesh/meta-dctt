FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# Add patch for your new machine
SRC_URI:append:sl1680_dct = " file://dolphin_brcm_bt_start.patch"

# Override do_patch for new machine
do_patch:append() {
	if [ "${MACHINE}" = "sl1680_dct" ]; then
		cd ${WORKDIR}
		patch -p1 < dolphin_brcm_bt_start.patch
	fi
}
