---
title: Net Narthollis - Of Windows and Unattended Installs
sitename: Net Narthollis
---
So about 3 months ago I started work in a job that is mostly Database Development, but with some general tech support thrown in as needed. One of the things that I was to look at as part of the tech support side of things was updating our unattended Windows XP install media, and looking at how to automate a Windows 7 install.

After a bit of screwing around I discovered that [vLite][1] wouldn't do everything I needed an unattended install to do (for example it couldn't install additional applications). A bit more poking around lead me to the [Windows Automated Install Kit (Windows AIK)][2] for Windows 7. After being entirely baffled by this glorified XML editor I once again turned to Google which lead me to the [Microsoft Deployment Toolkit (MDT)][3] and to [cluberti.com][4]'s article on MDT.

The depths of the Deployment toolkit are still a bit of a mystery to me, however I will attempt to document some of my efforts here.

So far I have managed to get Windows 7 x86 and Windows 7 x86_64 installing form USB media, with Windows XP Professional also on the USB media but not yet installing correctly. To get Windows 7 working simply follow the cluberti.com howto. As for Windows XP, this was as simple as inserting the CD and pointing MDT at that instead of a Windows 7 installer. Getting it working has been another thing entirely.

I have also managed to get a number of application installing automaticly - which is highly useful. I have done this with a combination of command line arguments and batch scripts (the batch scripts are mostly used for customising the default install, or ensuring the existence of icons on the desktop.) Eg.
~~~~{.batch}
@echo off
set ProgRoot=%ProgramFiles%
if not "%ProgramFiles(x86)%" == "" set ProgRoot=%ProgramFiles(x86)%
vnc-4_1_3-x86_win32.exe /sp- /verysilent /LOADINF="setup.inf" 
:: "%ProgRoot%\RealVNC\VNC4\winvnc4.exe" -noconsole -register
set STARTMENU=
if "%ALLUSERSPROFILE%"  == "C:\ProgramData" set STARTMENU=Microsoft\Windows
copy "%ALLUSERSPROFILE%\%STARTMENU%\Start Menu\Programs\RealVNC\VNC Server 4 (User-Mode)\Run VNC Server.lnk" "%ALLUSERSPROFILE%\%STARTMENU%\Start Menu\Programs\Startup"
regedit /s realvnc.reg
~~~~

[1]: http://www.vlite.net/ "vLite"
[2]: http://www.microsoft.com/downloads/details.aspx?displaylang=en&FamilyID=696dd665-9f76-4177-a811-39c26d3b3b34 "The Windows® Automated Installation Kit (AIK) for Windows® 7"
[3]: http://www.microsoft.com/downloads/details.aspx?FamilyId=3BD8561F-77AC-4400-A0C1-FE871C461A89&displaylang=en "Microsoft Deployment Toolkit (MDT) 2010"
[4]: http://www.cluberti.com/blog/2009/08/10/mdt-2010-and-deployment-from-a-usb-key/ "MDT 2010 and deployment from a USB key"