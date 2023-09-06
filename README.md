# Folder synchronization

This repository synchronizes files and folder from a source folder to a 
replica folder. Synchronization works one way. The destination folder contains
an exact copy of the source folder and this script can be used to schedule
synchronization after a certain intervals of time. The tool is created with 
minimal external dependencies. I created this tool within 2.5 days so please
point out any bugs by creating a pull request.

# Installation
The only non system python library used is 
[schedule](https://schedule.readthedocs.io/en/stable/) which can be installed 
via

```
pip install schedule
```
or
```bash
pip install -r requirements.txt
```
The tool was tested with Python 3.8.12
# Usage
How to run to tool? You can pass command line arguments.
```
python synctool/main.py -s /path/to/source/folder -d /path/to/destination/folder -l /path/to/logfile.txt
```
Use `-s` or `--source` flag for the path to the source folder, 
Use `-d` or `--destination` for the path to the destionation folder. 
The path to the log file must be specified with `-l` or `--log`.
You can also automatically synchronization after specific intervals. Pass
the command line flag `-i 10` or `--interval 10` which will auto sync the folders
after every 10 minutes. The value can be in float too e.g. 0.1. To quit this
auto sync use `Ctrl+C`. You can run the process in the background using [tmux](https://github.com/tmux/tmux/wiki/Getting-Started) 

# Pitfalls
Folder synchronization tools can become very complex and sophesticated e.g. rsync. To keep things
simple we have limited certain functionality of the tool. I will present some
pitfalls and workarounds those pitfalls. 

1. Stack overflow due to recursion  
    The tool recrusively parses the directories to be copied. Needless to say
    that if the number of directories is sufficient enough, we may encounter 
    call stack overload problem.
2. Symbolic links and special files  
    The program does not handle symbolic links or special files like device files or sockets.
3. File Permissions  
    The program cannot handle all file permission issues. E.g. source group folder
    has different group permissions than destination group. Other permission include
    reading, writing. Use `os.chmod` to change permissions but raise error
    if unable.
4. Handling Large Files
    While handling large files is cumbursome, it would be ideal to launch a subprocess
    for large files and write a separate copy function.
5. Character encoding  
    Assumption is that the character set is utf-8. 
6. Cross platform compatibility  
    Tested on linux. Not on Win / MacOS
7. File Locking  
    The program cannot handle a file that is being used by another program. 
8. Directory rename  
    If a directory is simply renamed while keeping the contents same, the program
    will rewrite the entire directory. Need to handle this efficiently. The
    log file will also skip the files that are being deleted in the directory if
    a directory is removed. A simple solution is to recursively find all files
    using `os.walk()` and log those deleted files too.
9. Scheduler  
    While the schedule library can call a simple function again and again in a 
    running program, it doesn't have job persistence. That means it will have
    to be launched again between restarts. Typically folder synchornization 
    programs run over remote servers. One way to automate such a script would 
    be `crontab` tool in linux. Crontab helps to launch scripts and manage 
    jobs running in the background. I couldn't find a nice and clean python
    solution for job scheduling.

# License
MIT License.