do_prepare_ini() {
    cp ${S}/weston-sl1680.ini ${S}/weston-${MACHINE}.ini
}
addtask prepare_ini before do_install after do_patch
