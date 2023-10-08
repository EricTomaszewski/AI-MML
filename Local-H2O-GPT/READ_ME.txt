READ:
README.md

All the offline models / weights were removed from "offline_folder" folder.

They were almost 26Gb...

They'd need to be redownloaded which happens automatically on initialisation of the code.

Nevertheless, there was an issue with using CPU only (rather than GPU) which meant that 
1. the text was only partially generated 
2. and at a speed of, perhaps, a word per minute.