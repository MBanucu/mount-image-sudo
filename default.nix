{
  lib
, buildPythonPackage
, setuptools
, src
}:
buildPythonPackage rec {
  pname = "mount-image-sudo";
  version = "0.1.0";
  pyproject = true;

  inherit src;

  nativeBuildInputs = [ setuptools ];
  propagatedBuildInputs = [ ];

  doCheck = false;
  pythonImportsCheck = [ "mount_image_sudo" ];

  meta = with lib; {
    description = "Disk image mounting via sudo losetup + mount (Linux)";
    homepage = "https://github.com/MBanucu/mount-image-sudo";
    license = licenses.gpl3Only;
    maintainers = with maintainers; [ ];
  };
}
