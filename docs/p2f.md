# The P2F format (P<sup>2</sup>epperoni pages Format)

Every p2f file must include a *P2FORMATVER* variable. this tells the generator how to parse the file. The latest format version is 0.

### Variables

Variables are very simple, and lack much purpose. 

Example: ```VariableName=value``` 

VariableName is self-explanatory, it is the variable's name. 

value is also simple, just replace this with whatever value you want to set.

In the P2F 0 standard, variables are only used for setting the P2Format version.

**WARNING:** Variables cannot be set inside the MD source of the file.

### Creating your page contents

Once basic setup is complete, you will want to add content to your page. This is done by embedding markdown into the file. 

To do this, you must type ```mdstart``` into your file. This will tell the parser everything from here until ```mdend``` is the contents of the page.

Comments in the non-markdown sections of the file can be added be prefixing the line with ```!!``` . 

**WARNING:** Comments cannot start anywhere but the first character of a line, because the parser goes through every single line in the file, and if the first two characters of that line are equal to ```["?", "!"]``` respectively, that **entire** line is removed.

### Generator commands

| Command | Arg0 | Arg1 | Purpose                                                  |
| ------- | ---- | ---- | -------------------------------------------------------- |
| mdstart | N/A  | N/A  | Marks the beginning of the markdown portion of the file. |
| mdend   | N/A  | N/A  | Marks the end of the markdown portion of the file.       |

### 

### Generator pre-processor directives

| Directive | Arg0             | Purpose                                                                       |
| --------- | ---------------- | ----------------------------------------------------------------------------- |
| ?!        | N/A              | Marks a line of the file to be removed by the preprocessor.                   |
| ?inc      | File to include. | Tells the preprocessor to open a file and paste its contents at its location. |

#### How to use the ```?inc``` preprocessor directive

 Example: ```?inc ./path/to/file/file.md``` 

There should be nothing before,  or after your include statement on that line.

### Generator variables

The generator's behavior may be modified using variables.

These variables are:

| Variable    | Default Value | Purpose                                               |
| ----------- | ------------- | ----------------------------------------------------- |
| P2FORMATVER | 0             | Sets the version of the P2F for the generator to use. |

### Generation

When the generator generates the pages, it parses the page file, takes the text from inbetween ```mdstart``` and ```mdend``` and converts it to HTML.
