$ErrorActionPreference = "Stop"

$sitePath = "D:\claude work\vibesafe"
if (!(Test-Path -LiteralPath $sitePath)) {
  throw "Missing expected VibeSafe site folder: $sitePath"
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"

function Write-Utf8NoBom {
  param([string]$Path, [string]$Value)
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Value, $utf8NoBom)
}

$manifestPath = Join-Path $sitePath "site.webmanifest"
$manifest = @'
{
  "name": "VibeSafe",
  "short_name": "VibeSafe",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0A1440",
  "theme_color": "#0A3AAF",
  "icons": [
    {
      "src": "/icon-256.png",
      "sizes": "256x256",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png"
    },
    {
      "src": "/favicon-96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/favicon-48x48.png",
      "sizes": "48x48",
      "type": "image/png"
    }
  ]
}
'@
Write-Utf8NoBom $manifestPath $manifest

$faviconBlock = @"
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
"@

$changed = New-Object System.Collections.Generic.List[string]
$htmlFiles = Get-ChildItem -LiteralPath $sitePath -Recurse -Filter "*.html" |
  Where-Object { $_.Name -ne "googlea45dffc8ea454638.html" }

foreach ($file in $htmlFiles) {
  $path = $file.FullName
  $html = Get-Content -LiteralPath $path -Raw
  $next = $html

  if ($next -notmatch '<link\s+rel="icon"') {
    if ($next -match '<meta\s+name="viewport"[^>]*>\s*') {
      $next = [regex]::Replace($next, '(<meta\s+name="viewport"[^>]*>\s*)', "`$1$faviconBlock", 1)
    } elseif ($next -match '<head>\s*') {
      $next = [regex]::Replace($next, '(<head>\s*)', "`$1$faviconBlock", 1)
    } else {
      Write-Warning "Skipped favicon insert for $path because no <head> was found."
    }
  } elseif ($next -notmatch '<link\s+rel="manifest"') {
    if ($next -match '<link\s+rel="apple-touch-icon"[^>]*>\s*') {
      $next = [regex]::Replace($next, '(<link\s+rel="apple-touch-icon"[^>]*>\s*)', "`$1<link rel=`"manifest`" href=`"/site.webmanifest`">`r`n", 1)
    } else {
      $next = [regex]::Replace($next, '(<link\s+rel="icon"[^>]*>\s*)', "`$1<link rel=`"manifest`" href=`"/site.webmanifest`">`r`n", 1)
    }
  }

  if ($next -ne $html) {
    Copy-Item -LiteralPath $path -Destination "$path.bak-favicon-$stamp" -Force
    Write-Utf8NoBom $path $next
    $changed.Add($path) | Out-Null
  }
}

Write-Host "Created/updated: $manifestPath"
Write-Host "Updated $($changed.Count) HTML file(s):"
$changed | ForEach-Object { Write-Host " - $_" }
Write-Host "Backups use suffix: .bak-favicon-$stamp"
