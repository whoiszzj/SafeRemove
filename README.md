# SafeRemove
This is a Linux tool which aims to safe remove files only depends on python.
## Usage
![demo.png](pics/demo.png)

You can use the following code to safely delete files with a preview.
```
python main.py <path1> <path2> ...
```
Press 'y', 'Y' or nothing and then Enter, the files will be deleted, otherwise the files will be kept.
Mention that the path supports **regular expression**, so you can use the following code to delete all files in the current directory.
```
python main.py ./*
```

## Install
Besides you can build an executable file with the script [build.sh](build.sh), and the file will exist in the directory [dist](dist). (pyinstaller is required!)
If you meet the problem that the 'pathlib' package is an obsolete backport balabala...., you can refer to [this](https://stackoverflow.com/questions/75476135/how-to-convert-python-file-to-exe-the-pathlib-package-is-an-obsolete-backport), in brief, change you pyinstaller to a lower version such as, 5.1. 

## Log
2023-06-22: When delete a single file from a directory, it will show the complete path of the file. Besides, add ctrl + C to exit the program.

2023-06-11: upload the init version 1.0, add basic functions.
    
## Reference
Thank all answers from [https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python](https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python) and [https://stackoverflow.com/questions/75476135/how-to-convert-python-file-to-exe-the-pathlib-package-is-an-obsolete-backport](https://stackoverflow.com/questions/75476135/how-to-convert-python-file-to-exe-the-pathlib-package-is-an-obsolete-backport)
