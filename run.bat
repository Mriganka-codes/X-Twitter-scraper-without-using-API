@echo off
setlocal

REM Set the title of the command prompt window
title Twitter Scraper

:menu
cls
echo =====================================
echo  Twitter Scraper - Control Panel
echo =====================================
echo.
echo  Please choose an option:
echo.
echo  1. Run Setup (First time or to reset)
echo  2. Run Scraper Once (For testing)
echo  3. Start Continuous Scraping (Scheduled)
echo  4. Open Scraped Data Folder
echo  5. Exit
echo.
set /p choice="  Enter your choice (1-5): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto run_once
if "%choice%"=="3" goto run_scheduler
if "%choice%"=="4" goto open_data
if "%choice%"=="5" goto exit_script

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:setup
cls
echo =====================================
echo  Running Setup
echo =====================================
echo.
python setup.py
echo.
echo Setup finished.
pause
goto menu

:run_once
cls
echo =====================================
echo  Running Scraper Once
echo =====================================
echo.
python scheduler.py --once
echo.
echo Scraping finished.
pause
goto menu

:run_scheduler
cls
echo =====================================
echo  Starting Continuous Scraping
echo =====================================
echo.
echo The scraper will run at the time specified in your .env file.
echo Press Ctrl+C to stop the scheduler.
echo.
python scheduler.py
echo.
echo Scheduler stopped.
pause
goto menu

:open_data
cls
echo =====================================
echo  Opening Data Folder
echo =====================================
echo.
if exist "data" (
    explorer "data"
    echo Data folder opened.
) else (
    echo Data folder not found. Run the scraper first.
)
pause
goto menu

:exit_script
exit /b 0
