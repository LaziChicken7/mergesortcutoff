@echo off
setlocal
echo ==================================================
echo  MergeSort CUTOFF - Reproducibility Runner
echo ==================================================

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [1/4] Installing Python dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

if not exist "benchmark.exe" (
    echo [INFO] benchmark.exe not found, compiling with g++...
    g++ -std=c++17 -O2 -DNDEBUG -static src/benchmark.cpp src/mergesort_user.cpp -o benchmark.exe
    if errorlevel 1 exit /b 1
)

echo [2/4] Generating datasets...
python scripts/generate_data.py
if errorlevel 1 exit /b 1

echo [3/4] Running benchmark (15 trials + warmup)...
python scripts/run_experiments.py --exe ./benchmark.exe --trials 15
if errorlevel 1 exit /b 1

echo [4/4] Analyzing results and generating charts...
python scripts/analyze.py
if errorlevel 1 exit /b 1
python scripts/full_analysis.py
if errorlevel 1 exit /b 1

echo ==================================================
echo  DONE! Results saved in results\ and results\charts\
echo ==================================================
pause
