# Deployment script for Letta DeepSeek

param(
    [string]$Environment = "development",
    [switch]$ForceOptimization
)

# Configuration
$config = @{
    development = @{
        InstanceType = "cpu-small"
        DiskSize = "10GB"
        Memory = "4GB"
    }
    staging = @{
        InstanceType = "cpu-medium"
        DiskSize = "20GB"
        Memory = "8GB"
    }
    production = @{
        InstanceType = "cpu-large"
        DiskSize = "50GB"
        Memory = "16GB"
    }
}

# Check environment variables
function Check-Environment {
    $required = @("DEEPSEEK_API_KEY", "TAVILY_API_KEY")
    $missing = @()
    
    foreach ($var in $required) {
        if (-not (Test-Path env:$var)) {
            $missing += $var
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Error "Missing required environment variables: $($missing -join ', ')"
        exit 1
    }
}

# Update Lightning configuration
function Update-LightningConfig {
    param($EnvConfig)
    
    $configPath = ".lightning"
    $content = Get-Content $configPath | ConvertFrom-Yaml
    
    $content.compute.instance_type = $EnvConfig.InstanceType
    $content.compute.disk_size = $EnvConfig.DiskSize
    $content.compute.memory = $EnvConfig.Memory
    
    $content | ConvertTo-Yaml | Set-Content $configPath
    Write-Host "Updated Lightning configuration for $Environment environment"
}

# Deploy to Lightning AI
function Deploy-Application {
    Write-Host "Deploying to Lightning AI..."
    
    # Check if optimization is needed
    if ($ForceOptimization -or (Test-OptimizationNeeded)) {
        Write-Host "Running memory optimization..."
        Invoke-WebRequest -Uri "http://localhost:8000/optimize" -Method POST
    }
    
    # Deploy using Lightning CLI
    lightning deploy app.py
}

# Check if optimization is needed
function Test-OptimizationNeeded {
    try {
        $health = Invoke-WebRequest -Uri "http://localhost:8000/health" | ConvertFrom-Json
        return $health.details.memory.needs_optimization
    }
    catch {
        Write-Warning "Could not check optimization status: $_"
        return $false
    }
}

# Main deployment process
try {
    Write-Host "Starting deployment to $Environment environment..."
    
    # Validate environment
    if (-not $config.ContainsKey($Environment)) {
        throw "Invalid environment: $Environment"
    }
    
    # Run checks
    Check-Environment
    
    # Update configuration
    Update-LightningConfig $config[$Environment]
    
    # Deploy
    Deploy-Application
    
    Write-Host "Deployment completed successfully!"
}
catch {
    Write-Error "Deployment failed: $_"
    exit 1
}