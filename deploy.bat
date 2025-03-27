@echo off
REM 创建gh-pages分支
git checkout -b gh-pages

REM 复制必要的文件到根目录
xcopy /E /I /Y static .
xcopy /E /I /Y templates\* .
copy web_app.py app.py

REM 创建index.html重定向
echo ^<meta http-equiv="refresh" content="0;url=index.html"^> > index.html

REM 添加所有文件
git add .

REM 提交更改
git commit -m "Deploy to GitHub Pages"

REM 推送到gh-pages分支
git push origin gh-pages

REM 切回主分支
git checkout main

echo Deployment completed!
pause 