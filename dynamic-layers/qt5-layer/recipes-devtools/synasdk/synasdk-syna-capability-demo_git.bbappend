do_install:append() {
    if [ "${MACHINE}" = "sl1680_dct" ]; then
        install -m 0644 ${S}/qmls/sl1680-capability-demo.qml ${D}${qmldir}/
    fi
}

