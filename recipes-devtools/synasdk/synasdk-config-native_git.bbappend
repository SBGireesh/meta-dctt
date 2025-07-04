FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://configs/product/sl1680_poky_aarch64_rdk/sl1680_poky_aarch64_rdk_defconfig"

do_configure:prepend() {
    cp ${WORKDIR}/configs/product/sl1680_poky_aarch64_rdk/sl1680_poky_aarch64_rdk_defconfig ${S}/configs/product/sl1680_poky_aarch64_rdk/sl1680_poky_aarch64_rdk_defconfig
}

