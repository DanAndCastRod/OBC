# Validation script for anteproyecto_coproductos.md
Write-Host "=== VALIDATION REPORT ==="
Write-Host ""

# 1. DLBP check
Write-Host "--- DLBP Occurrences ---"
$dlbp = Select-String -Path "anteproyecto_coproductos.md" -Pattern "DLBP"
if ($dlbp) {
    foreach ($match in $dlbp) {
        Write-Host "  L$($match.LineNumber): $($match.Line.Trim())"
    }
} else {
    Write-Host "  0 occurrences (PASS)"
}

Write-Host ""

# 2. Mermaid blocks
Write-Host "--- Mermaid Blocks ---"
$mermaid = Select-String -Path "anteproyecto_coproductos.md" -Pattern "``````mermaid"
Write-Host "  $($mermaid.Count) blocks found"

Write-Host ""

# 3. Section numbering
Write-Host "--- Section Numbering (### level) ---"
$sections = Select-String -Path "anteproyecto_coproductos.md" -Pattern "^### [0-9]"
foreach ($s in $sections) {
    Write-Host "  L$($s.LineNumber): $($s.Line.Trim())"
}

Write-Host ""

# 4. Figure/Table captions
Write-Host "--- Figure/Table Captions ---"
$captions = Select-String -Path "anteproyecto_coproductos.md" -Pattern "\*\*(Figura|Tabla) [0-9]"
foreach ($c in $captions) {
    $text = $c.Line.Trim()
    if ($text.Length -gt 80) { $text = $text.Substring(0, 80) + "..." }
    Write-Host "  L$($c.LineNumber): $text"
}

Write-Host ""

# 5. Bib validation
Write-Host "--- Bibliography Validation ---"
$md = Get-Content "anteproyecto_coproductos.md" -Raw
$cites = [regex]::Matches($md, "@([a-zA-Z0-9_-]+)") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$bib = Get-Content "referencias_coproductos.bib" -Raw
$keys = [regex]::Matches($bib, "@.*?\{([a-zA-Z0-9_-]+),") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$missing = $cites | Where-Object { $_ -notin $keys }
Write-Host "  Citations in MD: $($cites.Count)"
Write-Host "  Entries in BIB: $($keys.Count)"
Write-Host "  Missing refs: $($missing.Count)"
if ($missing) {
    foreach ($m in $missing) { Write-Host "    MISSING: $m" }
}

Write-Host ""
Write-Host "=== VALIDATION COMPLETE ==="
