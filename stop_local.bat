@echo off
title MarketMind AI - Stop Local Services
powershell -ExecutionPolicy Bypass -File "%~dp0stop_local.ps1"
pause
