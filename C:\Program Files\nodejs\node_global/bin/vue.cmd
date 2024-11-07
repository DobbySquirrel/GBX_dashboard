@SETLOCAL
@IF NOT DEFINED NODE_PATH (
  @SET "NODE_PATH=%~dp0\..\lib\node_modules\@vue"
) ELSE (
  @SET "NODE_PATH=%NODE_PATH%;%~dp0\..\lib\node_modules\@vue"
)
@IF EXIST "%~dp0\node.exe" (
  "%~dp0\node.exe"  "%~dp0\..\lib\node_modules\@vue\cli\bin\vue.js" %*
) ELSE (
  @SET PATHEXT=%PATHEXT:;.JS;=;%
  node  "%~dp0\..\lib\node_modules\@vue\cli\bin\vue.js" %*
)
