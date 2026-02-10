# Script de validación obligatorio
$md_content = Get-Content "anteproyecto_dlbp_coproductos.md" -Raw;
$md_content_final = Get-Content "docs/tesis/INFORME_FINAL_COMPLETO.md" -Raw;
$md_combined = $md_content + $md_content_final;

$citations = [regex]::Matches($md_combined, "@([a-zA-Z0-9_-]+)") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique;
$bib_content = Get-Content "referencias_dlbp.bib" -Raw;
$bib_keys = [regex]::Matches($bib_content, "@.*?{([a-zA-Z0-9_-]+),") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique;

# Identificar desalineaciones
$unused = $bib_keys | Where-Object { $_ -notin $citations };
$missing = $citations | Where-Object { $_ -notin $bib_keys };

Write-Host "--- Reporte de Consistencia Bibliográfica ---"
Write-Host "Total Citas en MD: $($citations.Count)"
Write-Host "Total Entradas BIB: $($bib_keys.Count)"
Write-Host ""
Write-Host "Referencias en BIB no usadas en MD ($($unused.Count)):"
$unused | ForEach-Object { Write-Host " - $_" }
Write-Host ""
Write-Host "Citas en MD sin entrada en BIB ($($missing.Count)):"
$missing | ForEach-Object { Write-Host " - $_" }
