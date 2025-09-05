@echo off
setlocal

:: Get the path of this script's folder (i.e. the vault folder)
set "VAULT_DIR=%~dp0"

:: Remove trailing backslash
if "%VAULT_DIR:~-1%"=="\" set "VAULT_DIR=%VAULT_DIR:~0,-1%"

:: Escape the ampersand (&) and other special characters if necessary (not needed here)

:: Open the vault via Obsidian protocol
start "" "obsidian://open?path=%VAULT_DIR%"
