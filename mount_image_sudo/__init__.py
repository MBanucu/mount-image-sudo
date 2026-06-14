"""Disk image mounting via sudo losetup + mount (Linux)."""

import os
import re
import shutil
import subprocess
import tempfile
import time

_LO_REGEX = re.compile(r'\(([^)]+)\)')


def mount_image(image_path: str, fstype: str = 'exfat',
                options: list[str] | None = None) -> tuple[str, str]:
    """Attach *image_path* as a loop device and mount it.

    Returns ``(device, mount_point)``.
    Raises ``RuntimeError`` on failure.
    """
    r = subprocess.run(
        ['sudo', 'losetup', '-f', '--show', str(image_path)],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"losetup failed: {r.stderr}")
    loop_dev = r.stdout.strip()

    mount_point = tempfile.mkdtemp(prefix='mount_image_')
    if options is not None:
        mount_opts = ','.join(options)
    else:
        mount_opts = f'uid={os.getuid()},gid={os.getgid()}'

    r = subprocess.run([
        'sudo', 'mount', '-t', fstype,
        '-o', mount_opts,
        loop_dev, mount_point,
    ], capture_output=True, text=True)
    if r.returncode != 0:
        subprocess.run(['sudo', 'losetup', '-d', loop_dev], capture_output=True)
        shutil.rmtree(mount_point, ignore_errors=True)
        raise RuntimeError(f"mount failed: {r.stderr}")

    return loop_dev, mount_point


def umount_image(device: str, mount_point: str | None = None):
    """Unmount and detach a disk image."""
    r = subprocess.run(['sudo', 'losetup', device],
                       capture_output=True, text=True)
    if r.returncode == 0:
        m = _LO_REGEX.search(r.stdout)
        if m:
            subprocess.run(['sudo', 'umount', device], capture_output=True)
            time.sleep(0.3)

    if mount_point:
        time.sleep(0.3)
        try:
            shutil.rmtree(mount_point, ignore_errors=True)
        except Exception:
            pass

    subprocess.run(['sudo', 'losetup', '-d', device], capture_output=True)


def attach_image(image_path: str) -> str:
    """Attach *image_path* as a block device without mounting.

    Returns the device path (e.g. ``/dev/loop0``).
    Raises ``RuntimeError`` on failure.
    """
    r = subprocess.run(
        ['sudo', 'losetup', '-f', '--show', str(image_path)],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"losetup failed: {r.stderr}")
    return r.stdout.strip()


def detach_image(device: str):
    """Detach a block device."""
    subprocess.run(['sudo', 'losetup', '-d', device], capture_output=True)
