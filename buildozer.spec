[app]

# (str) Title of your application
title = Mobile Quiz Game

# (str) Package name
package.name = mobilequizgame

# (str) Package domain (used for the apk package name)
package.domain = com.yourcompany

# (str) App version
version = 0.1

# (list) Application requirements (KivyMD depends on Kivy and Pillow)
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow

# (str) Main application file relative to the current directory.
source.dir = .

# (list) Python files to exclude from the source.
source.exclude_exts = spec

# (list) List of exclusions for standard Android build files
android.exclude_exts = png,jpg,jpeg

# (list) Permissions
# Needed for standard Android mobile use
android.permissions = INTERNET

# (int) The Android SDK version to target
android.api = 33

# (int) Minimum Android API required
android.minapi = 21

# (str) The directory to store the APK in
bin.dir = bin

# (str) The name of the resulting APK file
apk.name = %(title)s-%(version)s-debug.apk

# --------------------------------------------------
# Advanced Buildozer Configuration (Leave as default)
# --------------------------------------------------

[buildozer]
log_level = 2
