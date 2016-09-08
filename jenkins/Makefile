UID := $(shell id -u)
GID := $(shell id -g)

default:
	@echo "make centos6_rpm|centos7_rpm"

images:
	docker build --rm -t zenosslabs/rpm-builder-centos6 centos6
	docker build --rm -t zenosslabs/rpm-builder-centos7 centos7

rpms: el6_rpm el7_rpm
	@echo done	

el6_rpm:
	docker run --rm --privileged=true -v $(CURDIR):$(CURDIR) -w $(CURDIR) zenosslabs/rpm-builder-centos6 sh -c "python setup.py bdist_rpm --release='1.el6'; chown -R $(UID):$(GID) dist"

el7_rpm:
	docker run --rm --privileged=true -v $(CURDIR):$(CURDIR) -w $(CURDIR) zenosslabs/rpm-builder-centos7 sh -c "python setup.py bdist_rpm --release='1.el7'; chown -R $(UID):$(GID) dist"
