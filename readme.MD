# Premire Pro Automatic footage linker
Adobe Premire Pro has a big problem with linking medias after changing directory (moving project files between editors, clients, etc). This script automatically finds footage in folder (with all subfolder included) and links it into existing Premire Pro project.

This script was taken out of my rendering farm/editor tools that I made. I hope this could help editors, because linking hundereds of media manually is a big pain and waste of time. This issue is knows since `Premire Pro 23.4`. Adobe Please FIX it!

## Examples of people facing that problem online:
- [Can't link media despite having all of the necessary footage](https://www.reddit.com/r/premiere/comments/s3ai6g/cant_link_media_despite_having_all_of_the/) - Premire Pro forum
- [Trouble with Linking Media](https://community.adobe.com/t5/premiere-pro-bugs/trouble-with-linking-media-the-one-file-i-use-and-cut-repeats-after-every-cut/idi-p/13823984) - Premire Pro forum


This script suports English and Polish language (just change `EN_LANG` to `False` if you want it to be in Polish).



## Install
Just download and use it. I used only build in libraries/modules. I used `gzip`, `os`, `xml`. Be aware that this script does not support command line. You have to put your own variables there, or build program around it.