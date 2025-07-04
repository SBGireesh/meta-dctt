do_deploy:append () {
    if [ "${MACHINE}" != "sl1680usb_dct" ]; then
        if [ -f "${B}/target/release/uboot/sm_fw_en.bin" ]; then
            install -m 0644 "${B}/target/release/uboot/sm_fw_en.bin" ${DEPLOYDIR}
        fi
        exec_cmd="parse_pt_emmc 101 101 \
                  ${CONFIG_EMMC_BLOCK_SIZE} ${CONFIG_EMMC_TOTAL_SIZE}"
        if [ "${MACHINE}" = "sl1680spi_dct" ]; then
            . ${STAGING_DIR_NATIVE}/usr/share/syna/build/${SYNA_SDK_FLASH_TYPE_CFG_FILE}
            exec_cmd="parse_pt 0 0 \
                      ${spi_block_size} ${spi_total_size}"
        fi

        exec_args="${EMMC_PT_FILE} \
                  ${DEPLOYDIR}/linux_params_mtdparts \
                  ${DEPLOYDIR}/version_table \
                  ${DEPLOYDIR}/subimglayout "
        if [ "${MACHINE}" != "sl1680spi_dct" ]; then
                      exec_args+="${DEPLOYDIR}/emmc_part_table \
                                  ${DEPLOYDIR}/emmc_part_list \
                                  ${DEPLOYDIR}/emmc_image_list "
        fi

        # Parse pt file
        ${exec_cmd} ${exec_args}

        # Update the CRC of the version table
        crc -a ${DEPLOYDIR}/version_table
        if [ "${MACHINE}" != "sl1680spi_dct" ]; then
            # Change the subimage files to .gz
            sed -i -e 's:\([a-zA-Z0-9]\+\)\(_[a|b]\)\?\.subimg,:\1.subimg.gz,:' ${DEPLOYDIR}/emmc_image_list
        fi
    fi
}

