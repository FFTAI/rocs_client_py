set FILE_FULL_PATH=%0
set FILE_NAME=%~n0
for /r %%i in (%FILE_NAME%) do set FILE_PATH=%%~dpi
cd %FILE_PATH%

rmdir /s /q source
rmdir /s /q build

mkdir source\_static
mkdir source\_template
mkdir build

xcopy /E conf.py .\source\
xcopy /E index.rst .\source\

sphinx-apidoc -o source ../src
.\make.bat markdown