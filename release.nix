{ lib, python3Packages, setuptools }:
with python3Packages;
buildPythonPackage rec {
  pname = "whatthepatch";
  version = "1.0.3";
  format = "pyproject";
  src = ./.;

  checkInputs = [ pytestCheckHook ];

  pythonImportsCheck = [ "whatthepatch" ];

  nativeBuildInputs = [ setuptools ];

  meta = with lib; {
    description = "Python library for both parsing and applying patch files";
    homepage = "https://github.com/cscorley/whatthepatch";
    license = licenses.mit;
    maintainers = with maintainers; [ cscorley ];
  };
}
