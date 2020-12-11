# sketchcodemaker
Uses  Selenium to generates sketch codes from https://sketch.hoylu.com/ based on preset values.

# Instructions

Create a tsv file with three columns. Each row is a class, and each column gives (a) the name of the class, (b) the first lesson number, and (c) the last lesson number. 
See courses.tsv for an example.

## Example

```
from codemaker import CodeMaker
cm = CodeMaker('courses.tsv', output_folder='codes')
cm.run()
```
