# 1. 定义登录函数
function Get-AuthToken {
    $loginResponse = Invoke-WebRequest -Method Post -Uri "http://localhost:5000/api/v1/security/login" `
        -ContentType "application/json" `
        -Body '{"username":"admin","password":"admin","provider":"db"}'
    return ($loginResponse.Content | ConvertFrom-Json).access_token
}

# 2. 定义带错误处理的API请求函数
function Invoke-ApiRequest {
    param(
        [string]$Uri,
        [string]$Method = "GET",
        [string]$Body,
        [string]$Token
    )

    $headers = @{
        "Authorization" = "Bearer $Token"
        "Content-Type" = "application/json"
    }

    $params = @{
        Uri = $Uri
        Method = $Method
        Headers = $headers
        ErrorAction = "Stop"
    }

    if ($Body) { $params["Body"] = $Body }

    try {
        $response = Invoke-WebRequest @params
        return $response.Content | ConvertFrom-Json
    }
    catch {
        if ($_.Exception.Response.StatusCode -eq 401) {
            Write-Host "令牌已过期，正在自动刷新..." -ForegroundColor Yellow
            $newToken = Get-AuthToken
            $headers["Authorization"] = "Bearer $newToken"
            $response = Invoke-WebRequest @params
            return @{
                Data = ($response.Content | ConvertFrom-Json)
                NewToken = $newToken
            }
        }
        else {
            Write-Host "请求失败: $($_.Exception.Message)" -ForegroundColor Red
            if ($_.Exception.Response) {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $errorResponse = $reader.ReadToEnd() | ConvertFrom-Json
                Write-Host "错误详情: $($errorResponse.message)" -ForegroundColor Red
            }
            return $null
        }
    }
}

# 3. 使用示例
$token = Get-AuthToken

# 调用私有端点
#$privateData = Invoke-ApiRequest -Uri "http://localhost:5000/api/v1/example/private" -Token $token
#$privateData

# 调用组端点
$groupData = Invoke-ApiRequest -Uri "http://localhost:5000/api/v1/group/1" -Token $token
$groupData