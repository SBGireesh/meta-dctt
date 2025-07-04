FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://boot/preboot/prebuilts/dolphin/A0/generic/hwinit/"

do_configure:prepend() {
    rm -rf ${S}/boot/preboot/prebuilts/dolphin/A0/generic/hwinit/
	cp -r ${WORKDIR}/boot/preboot/prebuilts/dolphin/A0/generic/hwinit/ ${S}/boot/preboot/prebuilts/dolphin/A0/generic/hwinit/
}

do_deploy:append() {
    if [ ${MACHINE} == "sl1680usb_dct" ]; then
        cat target/preboot/intermediate/release/K0_BOOT_store.bin > ${DEPLOYDIR}/gen3_scs.bin.usb
        cat target/preboot/intermediate/release/K0_TEE_store.bin >> ${DEPLOYDIR}/gen3_scs.bin.usb
        cat target/preboot/intermediate/release/K1_BOOT_A_store.bin >> ${DEPLOYDIR}/gen3_scs.bin.usb
        cat target/preboot/intermediate/release/K1_BOOT_B_store.bin >> ${DEPLOYDIR}/gen3_scs.bin.usb
        cat target/preboot/intermediate/release/K1_TEE_A_store.bin >> ${DEPLOYDIR}/gen3_scs.bin.usb

        cat target/preboot/intermediate/release/K0_BOOT_store.bin > ${DEPLOYDIR}/gen3_bkl.bin.usb
        cat target/preboot/intermediate/release/K0_TEE_store.bin >> ${DEPLOYDIR}/gen3_bkl.bin.usb
        cat target/preboot/intermediate/release/K1_BOOT_A_store.bin >> ${DEPLOYDIR}/gen3_bkl.bin.usb
        cat target/preboot/intermediate/release/K1_BOOT_B_store.bin >> ${DEPLOYDIR}/gen3_bkl.bin.usb
        cat target/preboot/intermediate/release/K1_TEE_A_store.bin >> ${DEPLOYDIR}/gen3_bkl.bin.usb
        cat target/preboot/intermediate/release/bcm_kernel.bin >> ${DEPLOYDIR}/gen3_bkl.bin.usb
        cat target/preboot/intermediate/release/K1_TEE_B_store.bin >> ${DEPLOYDIR}/gen3_bkl.bin.usb
        cat target/preboot/intermediate/release/K1_TEE_C_store.bin >> ${DEPLOYDIR}/gen3_bkl.bin.usb
        cat target/preboot/intermediate/release/K1_TEE_D_store.bin >> ${DEPLOYDIR}/gen3_bkl.bin.usb

        install -m 0644 target/preboot/intermediate/release/erom.bin ${DEPLOYDIR}/gen3_erom.bin.usb
        install -m 0644 target/preboot/intermediate/release/boot_monitor.bin ${DEPLOYDIR}/gen3_boot_monitor.bin.usb
        install -m 0644 target/preboot/intermediate/release/scs_data_param.sign ${DEPLOYDIR}/gen3_scs_param.bin.usb
        install -m 0644 target/preboot/intermediate/release/sysinit_en.bin ${DEPLOYDIR}/gen3_sysinit.bin.usb
        install -m 0644 target/preboot/intermediate/release/miniloader_en.bin ${DEPLOYDIR}/gen3_miniloader.bin.usb
    else
        install -m 0644 target/preboot/preboot_esmt.bin ${DEPLOYDIR}/preboot.subimg
    fi
}
