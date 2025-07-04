require ${COREBASE}/../meta-synaptics/dynamic-layers/qt5-layer/recipes-bsp/images/astra-media-qt5-common.inc

IMAGE_INSTALL:append = " \
    ${@bb.utils.contains('DISTRO_FEATURES', 'wayland', ' synasdk-synaexplorer synasdk-syna-astra-about', '', d)} \
"
