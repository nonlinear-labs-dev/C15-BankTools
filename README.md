# C15-BankTools
collection of Python-Scripts that allow introspection of C15 exported Banks.



# usage:
```
    cd ~/
    git clone git@github.com:nonlinear-labs-dev/C15-BankTools.git
    cd ~/C15-BankTools
    python3 theScriptYouWantToRun.py
```

If the `theScriptYouWantToRun` needs arguments to function it will exit early and print the help-text of the application.


for example running `python3 bankToCsv.py` prints:

```
use: ./bankToCsv <BANK>.xml <OUT>.csv
```
Indicating that you should supply a path to a Bank.xml file which will be used as input, and a path to where the result should be written.

All scripts (excluding ones living under /lib) follow this convention of printing their usage.

# working with paths on windows:
When using this tool on windows make sure to escape all paths with this symbol: "
example:
```
python test.py "path/to/directory or file/with spaces.xml"
``` 
