@echo off

echo  =====================
echo    Echoes Room Timer
echo  =====================
echo  -p (Disable time output when paused: cutscenes, textboxes, etc)
echo  -x (Disable time output when a room begins to load)

echo(
set /p flags= Enter flags (separated by space): 
echo(

python echoes_room_timer.py %flags%

pause
