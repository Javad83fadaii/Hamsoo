param([string]$Path = "/api/v1/version", [string]$Method = "GET", [string]$Body = "")

$ProgressPreference = 'SilentlyContinue'
$base = "http://87.107.9.100:8000"
$token = "2|ne3UZfqJOv8PCDUSDroLRuWxHn7ce3kGoDJUiviA88a8994c"
$headers = @{ Authorization = "Bearer $token"; Accept = 'application/json' }

try {
    if ($Body -ne "") {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
        $resp = Invoke-WebRequest -Uri "$base$Path" -Method $Method -Headers $headers -ContentType 'application/json' -Body $bytes -UseBasicParsing
    }
    else {
        $resp = Invoke-WebRequest -Uri "$base$Path" -Method $Method -Headers $headers -UseBasicParsing
    }
    "$($resp.StatusCode)"
    $resp.Content
}
catch {
    "ERR $($_.Exception.Message)"
    if ($_.Exception.Response) {
        try { (New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())).ReadToEnd() } catch {}
    }
}
