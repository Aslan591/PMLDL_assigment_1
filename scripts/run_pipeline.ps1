$ErrorActionPreference = "Stop"
$projectRoot = "C:\Users\yakup\PycharmProjects\PMLDL_assigment_1"

Set-Location $projectRoot

Write-Output "=== pipeline run started ==="

Write-Output "Running DVC pipeline: data prep and training"
& "$projectRoot\.venv\Scripts\dvc.exe" repro

Write-Output "Rebuilding and restarting docker containers"
Set-Location "$projectRoot\src\deployment"
docker-compose up --build -d

Write-Output "=== pipeline run finished ==="