
# Use this to control building and pushing of Docker images in a significantly less ugly fashion.
#

# Image build command definitions
define build-rucio-ferry-sync-cmd =
podman build -t rucio-ferry-sync --build-arg RUCIO_VERSION=${RUCIO_VERSION} .
endef

# Image build command declarations
build-rucio-ferry-sync:
	$(build-rucio-ferry-sync-cmd)

# Image push command definitions
define push-rucio-ferry-sync-cmd =
	podman tag rucio-ferry-sync imageregistry.fnal.gov/rucio-ams/rucio-ferry-sync:${RUCIO_VERSION}
	podman push imageregistry.fnal.gov/rucio-ams/rucio-ferry-sync:${RUCIO_VERSION}
endef

# Image push command declarations
push-rucio-ferry-sync:
	$(push-rucio-ferry-sync-cmd)