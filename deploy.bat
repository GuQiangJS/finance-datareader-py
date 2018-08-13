@echo off
echo 发版前先确认当前Github上没有commit还未被release。
echo 发版时会自动使用release的版本号。
pause
rmdir /s/q %~dp0dist
pause
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
pause