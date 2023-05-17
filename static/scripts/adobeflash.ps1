Invoke-WebRequest -Uri 'https://fpdownload.macromedia.com/get/flashplayer/current/support/uninstall_flash_player.exe' -OutFile 'c:\temp\uninstall_flash_player.exe'

c:\temp\uninstall_flash_player.exe -uninstall

Start-Sleep -Seconds 60

Remove-Item -Path "c:\temp\uninstall_flash_player.exe"
