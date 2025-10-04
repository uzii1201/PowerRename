@echo off
reg delete "HKCR\*\shell\PowerRename" /f
reg delete "HKCR\Directory\shell\PowerRename" /f
echo PowerRename eliminado del menú contextual de Windows.
pause