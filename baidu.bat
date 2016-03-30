@echo off

:A
echo 输入 q 退出
SET /P OP1="输入查询关键字: "

if "%OP1%"=="q" goto exit
if "%OP1%"=="Q" goto exit
if "%OP1%"=="" goto A

baidu.pyc %OP1%

pause

cls
goto A

:exit
exit