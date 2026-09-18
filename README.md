# 8 Ball Pool - Visual Assist & Practice Tool (Android APK Version)

نموذج أولي هندسي واحترافي مصمم خصيصاً للتحويل إلى **APK أندرويد** باستخدام **Buildozer** و**Kivy** للعبة **8 Ball Pool**.

---

## 🛠️ هيكلية المشروع (Modular Architecture)

1. **`app.py`**: واجهة المستخدم الرسومية المصممة باستخدام **Kivy** والمتوافقة تماماً مع نظام أندرويد.
2. **`detector.py`**: معالجة الصور وفضاء اللون (HSV) لكشف الكرة البيضاء والكرات المستهدفة بدقة.
3. **`geometry.py`**: النمذجة الرياضية لحساب مسار التسديد عبر نموذج **الكرة الوهمية (Ghost Ball)** وزاوية التسديد.
4. **`controller.py`**: التحكم الآلي في الشاشة عبر أوامر **`adb shell input swipe`** لتنفيذ التسديدات بدقة على أندرويد.
5. **`capture.py`**: التقاط الشاشة ديناميكياً باستخدام **`adb screencap`** (أو `mss` للاختبار المكتبي).

---

## 📦 بناء ملف APK للأندرويد عبر Buildozer

1. تثبيت Buildozer والمتطلبات على نظام Linux (أو WSL / بيئة بناء Buildozer):
   ```bash
   pip install buildozer
   ```
2. بدء بناء ملف APK بالوضع التجريبي (Debug):
   ```bash
   buildozer -v android debug
   ```
3. ستجد ملف APK الجاهز للتثبيت في المجلد:
   ```bash
   bin/poolaimassist-0.1-debug.apk
   ```
