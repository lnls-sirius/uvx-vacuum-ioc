PREFIX ?= /usr/local

# Docker files
SRC_IOC_FILE = vac-ioc.py
SERVICE_NAME = opr3-vacuum-ioc

# Service files
SRC_SERVICE_FILE = ${SERVICE_NAME}.service
SERVICE_FILE_DEST = /lib/systemd/system
SRC_SERVICE_FILE_D = ${SERVICE_FILE_DEST}/${SERVICE_NAME}.service.d/

.PHONY: install uninstall

install:
	mkdir -p ${SRC_SERVICE_FILE_D}
	cp --preserve=mode ${SRC_IOC_FILE} ${SRC_SERVICE_FILE_D}
	cp --preserve=mode ${SRC_SERVICE_FILE} ${SERVICE_FILE_DEST}
	sed -i "s#/root/vacuum/#${SRC_SERVICE_FILE_D}#g" ${SERVICE_FILE_DEST}/${SRC_SERVICE_FILE}
	systemctl daemon-reload
	systemctl stop ${SRC_SERVICE_FILE}
	systemctl start ${SRC_SERVICE_FILE}

uninstall:
	systemctl stop ${SERVICE_NAME}
	rm -f ${SERVICE_FILE_DEST}/${SRC_SERVICE_FILE}
	rm -f -R ${DOCKER_FILES_DEST}
	systemctl daemon-reload
