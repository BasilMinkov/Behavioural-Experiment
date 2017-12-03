cd %~dp0
python-3.6.3.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
python -m pip install expyriment future pygame pyopengl
echo cd %~dp0 > run.bat
echo python run_experiment.py >> run.bat