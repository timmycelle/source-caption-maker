<div align="center">
  <img src="src/assets/icon/scm.png" width=25%>
</div>

# source-caption-maker
source-caption-maker *(scm for short)* is a Python tool for creating and managing subtitles and closed captions for Source engine games. It converts JSON-formatted caption data into the Source engine's caption format, making it easy to add multilingual captions to Source engine mods.
> [!NOTE]
> **Closed captions & subtitles** function technically the same but are seperate things.
## What Does It Do?
1. Takes subtitle/caption data from a simple JSON format of a provided mod.
2. Converts it into Source engine-compatible captions (`.txt` files).
3. Optionally compiles the output `.txt` files into `.dat` files that the Source engine can use (using `captioncompiler.exe` of desired Source game).
> [!NOTE]
> For detailed information about Source engine's caption system, visit the [Valve Developer Wiki](https://developer.valvesoftware.com/wiki/Closed_Captions).
## Getting Started
### Prerequisites
- For using the compiled version (`.exe`): No additional requirements
- For running the Python script (`.py`/`.sh`):
  - Python 3.x
  - The `colour` library (only if you use HEX color codes)
### Linux Requirements
If you want to compile the output captions to `.dat` on Linux:
1. Install Wine (the script trys to use it to run `captioncompiler.exe`)
2. Enable Steam Play (Proton) for your Source game in Steam properties
3. Make sure the game is installed with Windows binaries (including `bin/captioncompiler.exe`)
## Usage
### Command Structure
#### EXE
```
scm.exe -mod <modname> [options]
```
#### Shell
```
sh scm.sh -mod <modname> [options]
```
#### Python
```
python3 scm.py -mod <modname> [options]
```
### Command Options
|Option|Type|Purpose|Required?|Description|
|-|-|-|:-:|-|
|`--mod`, `-m`|string|Mod Folder|Yes|Specifies which mod folder to process from the `in/` directory|
|`--game-path`, `-p`|string|Game Path|No|Path to Source game installation (for caption compilation)|
|`--subtitles`, `-s`|boolean|Process Subtitles|No|Convert subtitles of provided mod|
|`--captions`, `-c`|boolean|Process Captions|No|Convert captions of provided mod|
|`--clear`, `-cls`|boolean|Clear Screen|No|Clear console history before starting|
|`--langs`, `-l`|boolean|List Languages|No|Print all supported languages|
|`--verbose`, `-v`|boolean|Detailed Output|No|Print additional processing information|
|`--delete-output`, `-do`|boolean|Clear Output|No|Clear output folder before writing output (Proceed with caution!)|
|`--open-output`, `-oo`|boolean|Open Output|No|Open output folder when finished|
|`--copy-output`, `-co`|string|Copy Output|No|Copy output folder to specified location when finished|
## JSON
The tool uses a structured JSON format for defining captions. Here are the available keys and their purposes:
### Text and Display Keys
|Key|Type|Purpose|Required?|Example|
|-|-|-|:-:|-|
|`txt`|string|The actual text of the caption|Yes|`"txt": "Hello, world!"`|
|`dn`|string|Display name (character name)|No|`"dn": "GLaDOS"`|
|`ndn`|boolean|Hide display name|No|`"ndn": true`|
### Misc Keys
|Key|Type|Purpose|Required?|Example (JSON)|Example (Inline)|
|-|-|-|-|:-:|-|
|`clr`|string|Text color (HEX or RGB)|No, but advised|`"clr": "#FF0000"` or `"clr": "255,0,0"`|`<clr:255,0,0>`|
|`playerclr`|string|Player name color|No|`"playerclr": "255,255,0:255,0,255"` or `"playerclr": "#ffff00:#ff00ff"`|`<playerclr:255,255,0:255,0,255>`|
|`bold`|boolean|Bold text|No|`"bold": true`|`<B>`|
|`italic`|boolean|Italic text|No|`"italic": true`|`<I>`|
|`sfx`|boolean|Sound effect indicator|No|`"sfx": true`|`<sfx>`|
|`norepeat`|integer|Prevent caption repeat|No|`"norepeat": 1`|`<norepeat:1>`|
|`len`|integer|Display duration|No|`"len": 5`|`<len:5>`|

You can use inline keys in the txt key if you want to make additional modifications to the caption that isn't normally possible in the JSON style.

For example, instead of writing:
```json
{
    "txt": "Hello world",
    "clr": "#FF0000",
    "bold": true
}
```
You could write:
```json
{
    "txt": "<clr:255,0,0><B>Hello world"
}
```
*(This only applies to misc keys)*
## Planned features
- Developer Commentary
- GUI
- Replace the use of `captioncompiler.exe` with [source-caption-compiler](https://github.com/p0358/source-caption-compiler) for wider compatibility and more convenience
# FAQ
## What programming language did you use?
Python.
## Is this your first real project?
Yes.
## What was this project originally?
**source-caption-maker** was exclusively a tool for the development of a work-in-progress Portal 2 mod that I'm apart of, it was built quite differently but was basically the same concept as today's version.
## What do you want to accomplish with this?
My goal is to help modders quickly make subtitles/captions for their Source Engine mods across multiple languages, and potentially automate it.
## Can I convert the subtitle/caption files of games like Portal 2 to JSON (that's compatible with SCM) and then modify that to my liking?
I have thought about making this, but I'm not sure how I go about making it yet.
It's definitely still on my mind though.
## Is there a GUI planned?
Definitely.
## Is Developer Commentary supported?
Not yet - it's planned.