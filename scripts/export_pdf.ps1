$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    # Export BEEE_Circuit_Doctor_Project_Report.pdf
    $doc10 = $word.Documents.Open('D:\BEEE PROJECT\report\BEEE_Circuit_Doctor_Project_Report.docx')
    $pages = $doc10.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticPages)
    Write-Host "BEEE_Circuit_Doctor_Project_Report page count: $pages"
    $doc10.SaveAs([ref]'D:\BEEE PROJECT\report\BEEE_Circuit_Doctor_Project_Report.pdf', [ref]17)
    $doc10.Close()
    Write-Host "BEEE_Circuit_Doctor_Project_Report.pdf successfully exported."

    # Export Self_Learning_Circuit_Doctor_Report.pdf
    $doc1 = $word.Documents.Open('D:\BEEE PROJECT\report\Self_Learning_Circuit_Doctor_Report.docx')
    $doc1.SaveAs([ref]'D:\BEEE PROJECT\report\Self_Learning_Circuit_Doctor_Report.pdf', [ref]17)
    $doc1.Close()
    Write-Host "Self_Learning_Circuit_Doctor_Report.pdf successfully exported."
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
