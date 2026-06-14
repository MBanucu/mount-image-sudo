# mount-image-sudo

Disk image mounting via sudo losetup + mount (Linux).

[![PyPI version](https://img.shields.io/pypi/v/mount-image-sudo)](https://pypi.org/project/mount-image-sudo/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/MBanucu/mount-image-sudo)](LICENSE)
[![OS](https://img.shields.io/badge/OS-Linux-blue)](https://github.com/MBanucu/mount-image-sudo)

[![CI](https://img.shields.io/github/actions/workflow/status/MBanucu/mount-image-sudo/test.yml?branch=main)](https://github.com/MBanucu/mount-image-sudo/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/MBanucu/mount-image-sudo/branch/main/graph/badge.svg)](https://codecov.io/gh/MBanucu/mount-image-sudo)

[![Downloads total](https://pepy.tech/badge/mount-image-sudo)](https://pepy.tech/project/mount-image-sudo)
[![Downloads/month](https://pepy.tech/badge/mount-image-sudo/month)](https://pepy.tech/project/mount-image-sudo)
[![Downloads/week](https://pepy.tech/badge/mount-image-sudo/week)](https://pepy.tech/project/mount-image-sudo)

## Quick start

```python
from mount_image_sudo import mount_image, umount_image

device, mount_point = mount_image('/path/to/disk.img')
print(f'Mounted {device} at {mount_point}')
umount_image(device, mount_point)
```

## API

- `mount_image(path, fstype='exfat', options=None)` → `(device, mount_point)`
- `umount_image(device, mount_point=None)`
- `attach_image(path)` → `device`
- `detach_image(device)`

## License

GPL-3.0-only
