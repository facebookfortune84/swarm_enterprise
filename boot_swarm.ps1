$LaptopIP = (Get-NetRoute -DestinationPrefix 0.0.0.0/0 | Sort-Object RouteMetric | Select-Object -First 1).NextHop
Write-Host "Found Brain at: $LaptopIP" -ForegroundColor Cyan

# Update the .env file dynamically
$envPath = "C:\SwarmEnterprise\.env"
$content = Get-Content $envPath
$content = $content -replace "OLLAMA_URL=.*", "OLLAMA_URL=http://$LaptopIP:11434"
$content | Out-File $envPath -Encoding utf8

# Launch the factory
docker compose up -d --build