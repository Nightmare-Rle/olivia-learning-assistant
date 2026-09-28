# Build OLIVIA-Mobile APK from web assets + minimal Android WebView wrapper.
# No Gradle / Android Studio needed. Uses aapt2 + javac + d8 + zipalign + apksigner.
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$tmp = "C:\Users\NIGHTM~1\AppData\Local\Temp\opencode"
$SDK = Join-Path $tmp "android-sdk"
$BT = Join-Path $SDK "build-tools\34.0.0"
$PLATFORM = Join-Path $SDK "platforms\android-34\android.jar"
$JAVA = Join-Path $tmp "jdk17"
$JAVAC = (Get-ChildItem ($JAVA) -Directory | Where-Object Name -like "jdk-17*").FullName
$JAVAC = Join-Path $JAVAC "bin"

$web = Join-Path $Root "web"
$www = Join-Path $web "assets\www"
$androidDir = Join-Path $Root "android"
$build = Join-Path $Root "build"

function Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }

# 1) rebuild web assets
Step "Rebuilding web assets (build_web.py)..."
Push-Location (Join-Path $Root "tools")
python build_web.py
if ($LASTEXITCODE -ne 0) { throw "build_web.py failed" }
Pop-Location

# 2) icons
Step "Generating launcher icons..."
python (Join-Path $Root "tools\gen_icon.py")

# 3) aapt2 compile resources
Step "Compiling resources with aapt2..."
Remove-Item -Recurse -Force (Join-Path $build "res.zip") -ErrorAction SilentlyContinue
& (Join-Path $BT "aapt2.exe") compile --dir (Join-Path $androidDir "res") -o (Join-Path $build "res.zip")
if ($LASTEXITCODE -ne 0) { throw "aapt2 compile failed" }

# 4) aapt2 link
Step "Linking base APK with aapt2..."
Remove-Item -Recurse -Force (Join-Path $build "gen"), (Join-Path $build "base.apk") -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path (Join-Path $build "gen") | Out-Null
& (Join-Path $BT "aapt2.exe") link -o (Join-Path $build "base.apk") `
  -I $PLATFORM --manifest (Join-Path $androidDir "AndroidManifest.xml") `
  --java (Join-Path $build "gen") (Join-Path $build "res.zip")
if ($LASTEXITCODE -ne 0) { throw "aapt2 link failed" }

# 5) javac
Step "Compiling Java with javac..."
Remove-Item -Recurse -Force (Join-Path $build "classes") -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path (Join-Path $build "classes") | Out-Null
& (Join-Path $JAVAC "javac.exe") -source 8 -target 8 -encoding UTF-8 `
  -bootclasspath $PLATFORM -d (Join-Path $build "classes") `
  (Join-Path $androidDir "MainActivity.java")
if ($LASTEXITCODE -ne 0) { throw "javac failed" }

# 6) d8 dex
Step "Running d8 to produce classes.dex..."
Remove-Item -Recurse -Force (Join-Path $build "dex") -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path (Join-Path $build "dex") | Out-Null
$classes = @(Get-ChildItem (Join-Path $build "classes") -Recurse -Filter *.class | ForEach-Object { $_.FullName })
& (Join-Path $JAVAC "java.exe") -cp (Join-Path $BT "lib\d8.jar") com.android.tools.r8.D8 `
  --release --lib $PLATFORM --output (Join-Path $build "dex") $classes
if ($LASTEXITCODE -ne 0) { throw "d8 failed" }

# 7) pack dex + assets into APK
Step "Packing classes.dex + assets/www into APK..."
Remove-Item -Force (Join-Path $build "unzipped.apk") -ErrorAction SilentlyContinue
python (Join-Path $Root "tools\pack_apk.py") (Join-Path $build "base.apk") `
  (Join-Path $build "dex\classes.dex") $www (Join-Path $build "unzipped.apk")
if ($LASTEXITCODE -ne 0) { throw "pack_apk failed" }

# 8) zipalign
Step "Zipaligning..."
Remove-Item -Force (Join-Path $build "aligned.apk") -ErrorAction SilentlyContinue
& (Join-Path $BT "zipalign.exe") -f 4 (Join-Path $build "unzipped.apk") (Join-Path $build "aligned.apk")
if ($LASTEXITCODE -ne 0) { throw "zipalign failed" }

# 9) sign
Step "Signing APK..."
$ks = Join-Path $build "olivia-debug.keystore"
if (-not (Test-Path $ks)) {
  & (Join-Path $JAVAC "keytool.exe") -genkeypair -v -keystore $ks -storepass android `
    -keypass android -alias olivia -keyalg RSA -keysize 2048 -validity 10000 `
    -dname "CN=OLIVIA Mobile,O=OLIVIA,C=PH" | Out-Null
}
$dist = Join-Path $Root "dist"
New-Item -ItemType Directory -Force -Path $dist | Out-Null
$final = Join-Path $dist "O.L.I.V.I.A-Mobile.apk"
Remove-Item -Force $final -ErrorAction SilentlyContinue
& (Join-Path $BT "apksigner.bat") sign --ks $ks --ks-pass pass:android --key-pass pass:android `
  --out $final (Join-Path $build "aligned.apk")
if ($LASTEXITCODE -ne 0) { throw "apksigner sign failed" }

# 10) verify
Step "Verifying signature..."
& (Join-Path $BT "apksigner.bat") verify --print-certs $final

$sizeMB = [math]::Round((Get-Item $final).Length / 1MB, 2)
Write-Host "`nBUILD COMPLETE:" -ForegroundColor Green
Write-Host "  $final  (${sizeMB} MB)" -ForegroundColor Green