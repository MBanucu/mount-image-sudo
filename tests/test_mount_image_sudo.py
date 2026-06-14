"""Unit tests for mount_image_sudo — mocked subprocess calls."""

import unittest
from unittest.mock import patch, MagicMock


class TestSudoMount(unittest.TestCase):
    @patch('mount_image_sudo.subprocess.run')
    @patch('mount_image_sudo.tempfile.mkdtemp')
    def test_mount_image_success(self, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = '/tmp/mp'
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout='/dev/loop0\n'),
            MagicMock(returncode=0, stdout=''),
        ]
        from mount_image_sudo import mount_image
        dev, mp = mount_image('/tmp/test.img', 'vfat', None)
        self.assertEqual(dev, '/dev/loop0')
        self.assertEqual(mp, '/tmp/mp')

    @patch('mount_image_sudo.subprocess.run')
    @patch('mount_image_sudo.tempfile.mkdtemp')
    def test_mount_image_losetup_fails(self, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = '/tmp/mp'
        mock_run.return_value = MagicMock(returncode=1, stderr='Permission denied')
        from mount_image_sudo import mount_image
        with self.assertRaises(RuntimeError) as ctx:
            mount_image('/tmp/test.img', 'vfat', None)
        self.assertIn('losetup failed', str(ctx.exception))

    @patch('mount_image_sudo.subprocess.run')
    @patch('mount_image_sudo.tempfile.mkdtemp')
    def test_mount_image_mount_fails_cleans_up(self, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = '/tmp/mp'
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout='/dev/loop0\n'),
            MagicMock(returncode=1, stderr='mount failed'),
            MagicMock(returncode=0, stdout=''),
        ]
        from mount_image_sudo import mount_image
        with self.assertRaises(RuntimeError) as ctx:
            mount_image('/tmp/test.img', 'vfat', None)
        self.assertIn('mount failed', str(ctx.exception))

    @patch('mount_image_sudo.subprocess.run')
    @patch('mount_image_sudo.tempfile.mkdtemp')
    def test_mount_image_custom_options(self, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = '/tmp/mp'
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout='/dev/loop0\n'),
            MagicMock(returncode=0, stdout=''),
        ]
        from mount_image_sudo import mount_image
        mount_image('/tmp/test.img', 'ext4', ['ro', 'noexec'])
        args = mock_run.call_args_list[1][0][0]
        self.assertIn('-o', args)
        self.assertIn('ro,noexec', args)

    @patch('mount_image_sudo.subprocess.run')
    def test_umount_image(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='')
        from mount_image_sudo import umount_image
        umount_image('/dev/loop0', '/tmp/mp')

    @patch('mount_image_sudo.subprocess.run')
    def test_attach_image_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='/dev/loop0\n')
        from mount_image_sudo import attach_image
        dev = attach_image('/tmp/test.img')
        self.assertEqual(dev, '/dev/loop0')

    @patch('mount_image_sudo.subprocess.run')
    def test_attach_image_fails(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stderr='error')
        from mount_image_sudo import attach_image
        with self.assertRaises(RuntimeError):
            attach_image('/tmp/test.img')

    @patch('mount_image_sudo.subprocess.run')
    def test_detach_image(self, mock_run):
        from mount_image_sudo import detach_image
        detach_image('/dev/loop0')
        mock_run.assert_called_once_with(
            ['sudo', 'losetup', '-d', '/dev/loop0'], capture_output=True)
