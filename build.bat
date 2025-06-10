set PROJ_PATH=%~dp0
set SPEC_PATH=%PROJ_PATH%main.spec
uv --directory %PROJ_PATH% run pyinstaller %SPEC_PATH%