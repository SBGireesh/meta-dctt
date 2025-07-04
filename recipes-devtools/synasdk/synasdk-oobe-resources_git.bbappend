do_install:append () {
    install -d ${D}/etc
    install -d ${D}${rootdir}/demos/videos/mp4
    install -d ${D}${rootdir}/demos/videos/h264
    install -d ${D}${rootdir}/demos/configs

    cp ${S}/config_files/powervr.ini ${D}/etc/
    cp ${S}/videos/mp4/* ${D}${rootdir}/demos/videos/mp4/
    ${@bb.utils.contains('MACHINE', 'sl1680_dct', 'cp ${S}/videos/h264/sl1680/* ${D}${rootdir}/demos/videos/h264/; cp ${S}/config_files/syna_capability_demo_sl1680_config.txt ${D}/${rootdir}/demos/configs/', '', d)}
}

