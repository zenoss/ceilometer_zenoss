default:
	@echo "make centos6_rpm|centos7_rpm"

images:
	sudo docker build -f Dockerfile.centos6 --rm -t zenosslabs/rpm-builder-centos6 .
	sudo docker build -f Dockerfile.centos7 --rm -t zenosslabs/rpm-builder-centos7 .

rpms: el6_rpm el7_rpm
	@echo done	

el6_rpm:
	sudo docker run --rm --privileged=true -v $(PWD):$(PWD) -w $(PWD) zenosslabs/rpm-builder-centos6 python setup.py bdist_rpm --release='1.el6'

el7_rpm:
	sudo docker run --rm --privileged=true -v $(PWD):$(PWD) -w $(PWD) zenosslabs/rpm-builder-centos7 python setup.py bdist_rpm --release='1.el7'
