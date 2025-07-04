do_install:append () {
		if [ "${MACHINE}" = "sl1680_dct" ]; then
				install -m 0644 ${S}/qmls/sl1680-ai.qml  ${D}${qmldir}/
				install -m 0644 ${S}/qmls/panels/FaceDetection.qml ${D}${qmldir}/panels/FaceDetection.qml
				install -m 0644 ${S}/qmls/panels/ObjectDetection.qml ${D}${qmldir}/panels/ObjectDetection.qml
				install -m 0644 ${S}/qmls/panels/PoseEstimation.qml ${D}${qmldir}/panels/PoseEstimation.qml
				install -m 0644 ${S}/qmls/panels/MultiAi.qml ${D}${qmldir}/panels/MultiAi.qml
				install -m 0644 ${S}/qmls/panels/AIEncoding.qml ${D}${qmldir}/panels/AIEncoding.qml
		fi
}
