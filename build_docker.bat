@echo off
REM بناء APK عبر Docker - يعمل على ويندوز مباشرة بدون WSL setup
REM المدة: 25-40 دقيقة أول مرة (تحميل SDK/NDK) ثم 5 دقائق بعدها
echo [1/2] سحب صورة kivy/buildozer...
docker pull kivy/buildozer:latest

echo [2/2] بدء البناء...
REM يعمل مجلد المشروع الحالي داخل Docker
docker run --rm -v "%cd%:/home/user/hostcwd" kivy/buildozer android debug

echo.
echo === انتهى البناء ===
echo اذا نجح ستجد الملف في: bin\poolaimassist-0.1-debug.apk
pause
