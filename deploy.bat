@echo off
echo ����ǰ��ȷ�ϵ�ǰGithub��û��commit��δ��release��
echo ����ʱ���Զ�ʹ��release�İ汾�š�
pause
rmdir /s/q %~dp0dist
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
pause