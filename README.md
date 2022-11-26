# markdown-tree
Draw a tree of your project in markdown format

## Documentation

```bash
usage: tree.py [-h] [-D DIRECTORY] [-f FILE] [-d MAX_DEPTH] [-e EXCLUDE] [-o ORDER] [-s] [-H] [-r] [-E] [-S] [-F] [-N NO_DEVELOP]

Markdown tree

options:
  -h, --help            show this help message and exit
  -D DIRECTORY, --directory DIRECTORY
                        Directory to display, default is current directory
  -f FILE, --file FILE  File to write the tree, default is stdout
  -d MAX_DEPTH, --max-depth MAX_DEPTH
                        Maximum depth of the tree, default is 5
  -e EXCLUDE, --exclude EXCLUDE
                        Exclude files matching the pattern
  -o ORDER, --order ORDER
                        Criteria for sorting, can be "default", "time" or "size", default is "default"
  -s, --separate        Separate files from directories
  -H, --show-hidden     Show hidden files
  -r, --reverse         Reverse the order of the files
  -E, --emotes          Use emotes
  -S, --summary         Display a summary of the tree
  -F, --display-from-directory
                        Display the tree from the directory (the directory you specified will be treated as ".")
  -N NO_DEVELOP, --no-develop NO_DEVELOP
                        Do not display the files in the directory matching the pattern, display "..." instead
```

You can find [here](https://github.com/Th3o-D/UTC-IA01) an example of output of this program.

<div align="right" style="display: flex">
   <img src="https://visitor-badge.glitch.me/badge?page_id=Th3o-D/markdown-tree&left_color=gray&right_color=blue" height="20"/>
   <a href="https://github.com/Th3o-D" alt="https://github.com/Th3o-D"><img height="20" style="border-radius: 5px" src="https://img.shields.io/static/v1?style=for-the-badge&label=CREE%20PAR&message=Th3o-D&color=1182c2"></a>
   <a href="LICENSE" alt="license"><img style="border-radius: 5px" height="20" src="https://img.shields.io/static/v1?style=for-the-badge&label=LICENCE&message=MIT&color=1182c2"></a>
</div>
