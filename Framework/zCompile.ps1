
$files = Get-ChildItem "./*.py"

foreach ($file in $files)
{
	$cmd = 'python -m py_compile ' + $file.Name
	Invoke-Expression $cmd
}

Write-Host -NoNewLine 'Press any key to continue...';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');