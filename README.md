# mlg2txt, a simple utility to convert IL-2 .mlg binary logs to text

IL-2 Sturmovik Battle of x can be configured to dump mission log files, which a number of tools can then parse. However, it's easy to forget to set the option, and I recently had an issue where my settings got reset, and so I was unable to turn in a PWCG mission due to not having the log file. IL2 will actually dump the same data into a binary .mlg file in the data/FlightLogs directory, and will always write these files without needing a config setting. mlg2txt can convert the .mlg files into the equivalent text representation, allowing tools to parse the logs.

The script is written in Python, so you'll need to download and install a Python 3.x version from <https://www.python.org/downloads/windows/>.

To run, use

```
py mlg2txt.py <paths to mlg files>
```

By default, a single txt file will be generated for each mlg file. The actual game will generate the files in chunks as the mission progresses. Adding the --split option will replicate the game's behaviour and generate multiple txt files.

The --output option can be used to specify where to put the generated files. If not provided, they will be written to the current directory.

One thing to note about the mlg file generation in the game is that they appear to be written when the mission is finished. This means that if the game crashes, no binary log is provided (while the text logs, as they're written in chunks, will be present).

