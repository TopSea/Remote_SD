@echo off
rem bat命令读取文件示例

Title SD_IPv4
 
rem 判断文件是否存在
if not exist temp_ip.txt (
  echo temp_ip.txt file not exist
  goto end
)
 
rem 读取文件，每次读取一行，默认以空格分隔，默认取第一列
for /f %%i in ('type temp_ip.txt') do (
  echo %%i
  set PYTHON=
  set GIT=
  set VENV_DIR=
  set COMMANDLINE_ARGS= --theme dark --xformers --api
)
echo %COMMANDLINE_ARGS%

E:
cd E:\WebUI\stable-diffusion-webui\
call webui.bat