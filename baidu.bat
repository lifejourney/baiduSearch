@echo off

:A
echo ���� q �˳�
SET /P OP1="�����ѯ�ؼ���: "

if "%OP1%"=="q" goto exit
if "%OP1%"=="Q" goto exit
if "%OP1%"=="" goto A

baidu.pyc %OP1%

pause

cls
goto A

:exit
exit