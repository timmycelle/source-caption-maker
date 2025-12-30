<div align="center">
  <img src="src/assets/icon/source-caption-maker.png" width=100%>
</div>

source-caption-maker *(scm for short)* is a Python tool for creating and managing subtitles and closed captions for Source engine games. It converts JSON-formatted caption data into the Source engine's caption format, making it easy to add multilingual captions to Source engine mods.
> [!NOTE]
> **Closed captions & subtitles** technically function the same but are seperate things.
## What Does It Do?
1. Takes subtitle/caption data from a simple JSON format of a provided mod.
2. Converts it into Source engine-compatible captions (`.txt` files).
3. Optionally compiles the output `.txt` files into `.dat` files that the Source engine can use (does so by using `captioncompiler.exe` of desired Source game).
> [!NOTE]
> For detailed information about Source engine's caption system, visit the [Valve Developer Wiki](https://developer.valvesoftware.com/wiki/Closed_Captions).
## Requirements
- Python 3.x
- Python `colour` module (Only if you use HEX color codes)
### Linux
If you want to compile the output captions to `.dat` on Linux:
1. Install Wine
2. Enable Steam Play (Proton) for your Source game in Steam properties (to get Windows binaries like the required `bin/captioncompiler.exe`)
3. That's it!
## Usage
### Command Structure
#### Windows
```
python3 scm.py --mod <modname> [options]
```
#### Linux
```
sh scm.sh --mod <modname> [options]
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
### Misc Keys
|Key|Type|Purpose|Required?|Example (JSON)|Example (Inline)|
|-|-|-|-|:-:|-|
|`ndn`|boolean|Hide display name|No|`"ndn": true`|-|
|`clr`|string|Text color (HEX or RGB)|No, but advised|`"clr": "#FF0000"` or `"clr": "255,0,0"`|`<clr:255,0,0>`|
|`playerclr`|string|Player name color|No|`"playerclr": "255,255,0:255,0,255"` or `"playerclr": "#ffff00:#ff00ff"`|`<playerclr:255,255,0:255,0,255>`|
|`bold`|boolean|Bold text|No|`"bold": true`|`<B>`|
|`italic`|boolean|Italic text|No|`"italic": true`|`<I>`|
|`sfx`|boolean|Sound effect indicator|No|`"sfx": true`|`<sfx>`|
|`norepeat`|integer|Prevent caption repeat|No|`"norepeat": 1`|`<norepeat:1>`|
|`len`|integer|Display duration|No|`"len": 5`|`<len:5>`|
## Example
### Input
`in/example/subtitles.json`:

```json
{
    "misc": {
        "Act 2": {
            "npc_floorturret": {
                "clr": "#aaf0d1"
            }
        }
    },
    "english": {
        "Act 2": {
            "npc_floorturret": {
                "dn": "Turret",
                "lines": {
                    "talkactive": {
                        "txt": "Activated!"
                    },
                    "talkcollide": {
                        "txt": "Coming through!"
                    },
                    "talkdisabled": {
                        "txt": "Critical Error!"
                    },
                    "talkdeploy": {
                        "txt": "Deploying!"
                    },
                    "talkshotat": {
                        "txt": "Hey! It's me!"
                    },
                    "talktipped": {
                        "txt": "Ouch!"
                    },
                    "talkdissolved": {
                        "txt": "Ow ow ow!"
                    },
                    "talkpickup": {
                        "txt": "Put me down!"
                    },
                    "talkautosearch": {
                        "txt": "Search mode activated!"
                    },
                    "talksearch": {
                        "txt": "Searching!"
                    },
                    "talkretire": {
                        "txt": "Target lost!"
                    }
                }
            }
        }
    },
    "german": {
        "Act 2": {
            "npc_floorturret": {
                "dn": "Turm",
                "lines": {
                    "talkactive": {
                        "txt": "Aktiviert!"
                    },
                    "talkcollide": {
                        "txt": "Platz da!"
                    },
                    "talkdisabled": {
                        "txt": "Kritischer Fehler!"
                    },
                    "talkdeploy": {
                        "txt": "Hochfahren!"
                    },
                    "talkshotat": {
                        "txt": "He, ich bin's!"
                    },
                    "talktipped": {
                        "txt": "Aua!"
                    },
                    "talkdissolved": {
                        "txt": "Aua!"
                    },
                    "talkpickup": {
                        "txt": "Ich will runter!"
                    },
                    "talkautosearch": {
                        "txt": "Suchmodus aktiviert!"
                    },
                    "talksearch": {
                        "txt": "Suche!"
                    },
                    "talkretire": {
                        "txt": "Zielverlust!"
                    }
                }
            }
        }
    }
}
```
`in/example/credits.txt`:
```
2025 timmycelle
```
### Output
`subtitles_english.txt`:
```
"lang"
{
"Language" "english"
"Tokens"
{
// ----- Act 2 -----
// --- npc_floorturret ---
"npc_floorturret.talkactive""<clr:170,240,209><B>Turret<B>: Activated!"
"npc_floorturret.talkcollide""<clr:170,240,209><B>Turret<B>: Coming through!"
"npc_floorturret.talkdisabled""<clr:170,240,209><B>Turret<B>: Critical Error!"
"npc_floorturret.talkdeploy""<clr:170,240,209><B>Turret<B>: Deploying!"
"npc_floorturret.talkshotat""<clr:170,240,209><B>Turret<B>: Hey! It's me!"
"npc_floorturret.talktipped""<clr:170,240,209><B>Turret<B>: Ouch!"
"npc_floorturret.talkdissolved""<clr:170,240,209><B>Turret<B>: Ow ow ow!"
"npc_floorturret.talkpickup""<clr:170,240,209><B>Turret<B>: Put me down!"
"npc_floorturret.talkautosearch""<clr:170,240,209><B>Turret<B>: Search mode activated!"
"npc_floorturret.talksearch""<clr:170,240,209><B>Turret<B>: Searching!"
"npc_floorturret.talkretire""<clr:170,240,209><B>Turret<B>: Target lost!"
}
}

// Auto-generated with source-caption-maker 1.0.2 by timmycelle
// More info: https://www.github.com/timmycelle/source-caption-maker

// Generated on 2025-10-31 at 20:36:53 UTC+1:00

// 2025 timmycelle
```
`subtitles_german.txt`:
```
"lang"
{
"Language" "german"
"Tokens"
{
// ----- Act 2 -----
// --- npc_floorturret ---
"npc_floorturret.talkactive""<clr:170,240,209><B>Turm<B>: Aktiviert!"
"npc_floorturret.talkcollide""<clr:170,240,209><B>Turm<B>: Platz da!"
"npc_floorturret.talkdisabled""<clr:170,240,209><B>Turm<B>: Kritischer Fehler!"
"npc_floorturret.talkdeploy""<clr:170,240,209><B>Turm<B>: Hochfahren!"
"npc_floorturret.talkshotat""<clr:170,240,209><B>Turm<B>: He, ich bin's!"
"npc_floorturret.talktipped""<clr:170,240,209><B>Turm<B>: Aua!"
"npc_floorturret.talkdissolved""<clr:170,240,209><B>Turm<B>: Aua!"
"npc_floorturret.talkpickup""<clr:170,240,209><B>Turm<B>: Ich will runter!"
"npc_floorturret.talkautosearch""<clr:170,240,209><B>Turm<B>: Suchmodus aktiviert!"
"npc_floorturret.talksearch""<clr:170,240,209><B>Turm<B>: Suche!"
"npc_floorturret.talkretire""<clr:170,240,209><B>Turm<B>: Zielverlust!"
}
}

// Auto-generated with source-caption-maker 1.0.2 by timmycelle
// More info: https://www.github.com/timmycelle/source-caption-maker

// Generated on 2025-10-31 at 20:36:53 UTC+1:00

// 2025 timmycelle
```

## Planned features
- Developer Commentary
- GUI
- Replace the use of `captioncompiler.exe` with [source-caption-compiler](https://github.com/p0358/source-caption-compiler) for wider compatibility and more convenience
# FAQ
## What programming language did you use?
![](readme/pythonpowered.gif)
## What was this project originally?
**source-caption-maker** was exclusively a tool for the development of a work-in-progress Portal 2 mod that I'm apart of, it was built quite differently but was basically the same concept as today's version.
## What do you want to accomplish with this?
My goal is to help modders quickly make subtitles/captions for their Source Engine mods across multiple languages, and potentially automate it.
## Can I convert the subtitle/caption files of Source games to JSON (that's compatible with SCM) and then modify that to my liking?
I have thought about making this, but I'm not sure how I go about making it yet.
It's definitely still on my mind though.
## Is there a GUI planned?
Definitely.
## Is Developer Commentary supported?
Not yet - it's planned.