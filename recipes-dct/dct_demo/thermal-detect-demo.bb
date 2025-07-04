DESCRIPTION = "Copy files for the thermal object detection demo"
LICENSE = "CLOSED"

PN = "thermal-detect-demo"

FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI = "file://dctdemo.py \
		   file://dctdemo.service \
		   file://start.sh \
		   file://weston.ini.syna-weston-desktop \
		   file://dct-logo-big.png \
		   file://dct-logo.png "

S = "${WORKDIR}"

do_install() {
    # Copy demo file to /home/root
    install -d ${D}${ROOT_HOME}
    install -m 0755 ${WORKDIR}/dctdemo.py ${D}${ROOT_HOME}/
    install -m 0755 ${WORKDIR}/start.sh ${D}${ROOT_HOME}/
    install -m 0644 ${WORKDIR}/dct-logo-big.png ${D}${ROOT_HOME}/
    install -m 0644 ${WORKDIR}/dct-logo.png ${D}${ROOT_HOME}/

    # Copy dctdemo.service file to systemd
    install -d ${D}/etc/systemd/system
    install -m 0644 ${WORKDIR}/dctdemo.service ${D}/etc/systemd/system/

    # Copy new weston.ini to weston folder
    install -d ${D}/etc/xdg/weston
    install -m 0644 ${WORKDIR}/weston.ini.syna-weston-desktop ${D}/etc/xdg/weston/
}

FILES:${PN} += "/home/root/dctdemo.py \
			    /home/root/start.sh \
			    /home/root/dct-logo-big.png \
			    /home/root/dct-logo.png \
				/etc/systemd/system/dctdemo.service \
				/etc/xdg/weston/weston.ini.syna-weston-desktop "
