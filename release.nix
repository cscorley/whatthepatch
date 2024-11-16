{ lib, python3Packages, setuptools }:
with python3Packages;
buildPythonPackage {
  pname = "whatthepatch";
  version = "1.0.7";
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
