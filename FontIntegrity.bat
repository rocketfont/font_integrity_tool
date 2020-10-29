@echo off
for %%I in (*.ttf) do python FontIntegrity.py "%%~nI"
for %%I in (*.otf) do python FontIntegrity.py "%%~nI"
pause