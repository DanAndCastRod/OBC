$md_content = Get-Content "anteproyecto_dlbp_coproductos.md" -Raw
$citations = [regex]::Matches($md_content, "@([a-zA-Z0-9_-]+)") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$bib_content = Get-Content "referencias_dlbp.bib" -Raw
$bib_keys = [regex]::Matches($bib_content, "@.*?\{([a-zA-Z0-9_-]+),") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

Write-Host "Citas en MD: $($citations.Count)"
Write-Host "Entradas en BIB: $($bib_keys.Count)"

$unused = $bib_keys | Where-Object { $_ -notin $citations }
$missing = $citations | Where-Object { $_ -notin $bib_keys }

Write-Host "`n---UNUSED ($($unused.Count))---"
$unused | ForEach-Object { Write-Host "  $_" }

Write-Host "`n---MISSING ($($missing.Count))---"
$missing | ForEach-Object { Write-Host "  $_" }

$match_pct = [math]::Round(($citations.Count - $missing.Count) / $citations.Count * 100, 1)
Write-Host "`nCoincidencia: $match_pct%"
