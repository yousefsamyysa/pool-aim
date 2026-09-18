# طرق بديلة مضمونة لبناء APK بدون اخطاء Colab

## الطريقة 1: GitHub Actions (الاسهل - 100% بدون تثبيت)
1. انشئ حساب GitHub و repo جديد (مثلا `pool-aim`)
2. ارفع كل ملفات `D:\8 Ball Pool` الى GitHub:
   ```
   git init
   git add .
   git commit -m "init"
   git branch -M main
   git remote add origin https://github.com/USERNAME/pool-aim.git
   git push -u origin main
   ```
3. اذهب الى تبويب Actions في GitHub -> سترى `Build APK` يعمل تلقائيا (15-25 دقيقة)
4. عند الانتهاء -> Artifacts -> حمل `poolaimassist-apk` -> بداخله `*.apk`

مميزات: بيئة Ubuntu نظيفة، لا اخطاء NDK/SDK، يحفظ كل build.

## الطريقة 2: Docker على جهازك (عندك Docker 29.6.1 جاهز)
لا تحتاج WSL ولا Colab. شغل فقط:
```bat
cd "D:\8 Ball Pool"
docker pull kivy/buildozer:latest
docker run --rm -v "%cd%:/home/user/hostcwd" kivy/buildozer android debug
```
الناتج: `D:\8 Ball Pool\bin\poolaimassist-0.1-debug.apk`

## الطريقة 3: بناء تجريبي خفيف (لاختبار السرعة بدون opencv)
اذا كان opencv هو سبب الفشل، جرب اولا بناء بدون opencv للتأكد من البيئة:
- عدل buildozer.spec: `requirements = python3,kivy==2.3.0,pillow`
- سيبني في 8 دقائق فقط. اذا نجح، نعيد opencv مع NDK 28c.

## ملاحظة عن خطأ Colab السابق
`Command failed: pythonforandroid.toolchain create ... --ndk-api=24` غالبا بسبب:
- opencv يحتاج NDK 28c مع API 33 (غير 25b)
- الحل: غير في buildozer.spec: `android.ndk = 28c` ثم `buildozer android clean` واعد البناء
