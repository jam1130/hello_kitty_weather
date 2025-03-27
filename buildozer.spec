[app]
title = Hello Kitty Weather
package.name = hellokittyweather
package.domain = org.hellokitty
source.dir = .
source.include_exts = py,jpg,kv,atlas,env
version = 1.0

requirements = python3,kivy,kivymd,requests,python-dotenv

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
ios.codesign.allowed = false

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

# 设置应用图标
ios.icon.filename = assets/hello_kitty.jpg

# 设置启动画面
ios.splash.filename = assets/hello_kitty.jpg

# 设置应用权限
ios.permissions = INTERNET

# 设置最低iOS版本
ios.minimum_version = 11.0

# 设置应用类别
ios.category = WEATHER

# 设置应用描述
ios.description = Hello Kitty主题天气应用，每天早上推送天气信息和温馨情话 