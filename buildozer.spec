[app]
title = 8 Ball Pool Aim Assist
package.name = poolaimassist
package.domain = com.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
# requirements: mss removed (desktop only), opencv is p4a recipe name
requirements = python3,kivy==2.3.0,numpy,opencv,pillow
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA
android.api = 33
android.minapi = 24
android.ndk = 25b
p4a.bootstrap = sdl2
p4a.accept_sdk_license_agreements = True
android.accept_sdk_license_agreements = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
