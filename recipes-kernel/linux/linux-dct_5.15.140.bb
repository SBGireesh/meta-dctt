LINUX_VERSION ?= "5.15.140"
PR = "r1"

require ${COREBASE}/../meta-synaptics/recipes-kernel/linux/linux-syna.inc
LIC_FILES_CHKSUM = "file://COPYING;md5=6bc538ed5bd9a7fc9398086aedcd7e46"

S = "${WORKDIR}/git"
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI = " \
    ${SYNA_SRC_LINUX_5_15} \
    file://0001-Synaptics-overlay.patch \
	file://0001-Device-tree-overlay.patch \
    file://add-full-hid-support.cfg \
    file://iptables.cfg \
    file://${SYNA_KERNEL_CONFIG_FILE} \
    git://git.yoctoproject.org/yocto-kernel-cache;type=kmeta;name=meta;branch=yocto-5.15;destsuffix=${KMETA} \
"

KMETA = "kernel-meta"

SRCREV_meta = "20e5ef444aa6054cea2acb756a092defeb1abf68"
SRCREV_linux_main = "${SYNA_SRCREV_LINUX_5_15}"

SRC_URI += "${@bb.utils.contains('DISTRO_FEATURES', 'systemd', 'file://systemd.cfg', '', d)}"
SRC_URI += "${@bb.utils.contains('DISTRO_FEATURES', 'bluetooth', 'file://add-bcm-bt-driver.cfg', '', d)}"
SRC_URI += "${@bb.utils.contains('KGDB_ENABLE', '1', ' \
    file://0001-kgdb_Fix_incorrect_single_stepping_into_the_irq_handle.patch \
    file://debug_info.cfg \
    file://kgdb.cfg', '', d)}"
SRC_URI += "${@bb.utils.contains('DISTRO_FEATURES', 'virtualization', 'file://add-docker.cfg', '', d)}"

python () {
    # OpenBMC loads in kernel features via other mechanisms so this check
    # in the kernel-yocto.bbclass is not required
    d.setVar("KERNEL_DANGLING_FEATURES_WARN_ONLY","1")
}

COMPATIBLE_MACHINE = "syna"
PACKAGE_ARCH = "${MACHINE_ARCH}"

CMDLINE_EMMC_BOOT:sl1680usb_dct = "shell earlycon console=ttyS0,115200 rootwait rootfstype=ext4"
CMDLINE_EMMC_BOOT:sl1680spi_dct = "shell earlycon console=ttyS0,115200 rootwait rootfstype=ext4"
