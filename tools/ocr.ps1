param([string]$dir,[string]$out)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[void][Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation,ContentType=WindowsRuntime]
[void][Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op,[Type]$t){ $task=$asTask.MakeGenericMethod($t).Invoke($null,@($op)); $task.Wait(); $task.Result }
[void][Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime]
$lang = [Windows.Globalization.Language]::new('ja')
$eng = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
$sw = New-Object System.IO.StreamWriter($out,$false,[System.Text.Encoding]::UTF8)
Get-ChildItem $dir -Filter *.png | Sort-Object Name | % {
  $f = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($_.FullName)) ([Windows.Storage.StorageFile])
  $s = Await ($f.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
  $d = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($s)) ([Windows.Graphics.Imaging.BitmapDecoder])
  $b = Await ($d.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
  $r = Await ($eng.RecognizeAsync($b)) ([Windows.Media.Ocr.OcrResult])
  $sw.WriteLine($_.BaseName + "`t" + $r.Text)
  $s.Dispose()
}
$sw.Close()
