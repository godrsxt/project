[app]

# (str) Title of your application
title = mOnkeytype

# (str) Package name
package.name = monkeytyp3

# (str) Package domain (needed for android/ios packaging)
package.domain = com.type

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd,pillow,pyjnius

# (list) Supported orientations
orientation = landscape

# Android specific
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) Android additional adb arguments
android.adb_args = -H host.docker.internal

# (str) The format used to package the app for release mode
android.release_artifact = aab

# (str) The format used to package the app for debug mode
android.debug_artifact = apk

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

# (str) Path to build artifact storage
build_dir = ./.buildozer

# (str) Path to build output storage
bin_dir = ./bin
