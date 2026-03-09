# Introduction

This is a simple [**GIMP 3**](https://www.gimp.org/downloads/) plugin written in **python 3** that allows you to blend two layers together.

# Usage

- Load your two textures as separate layers (layer order matters!)
- Open `Filters` → `Blend two layers transition`
- Pick the percentage value (`20%` is a good starting point).
- Press `OK`

# Demonstration

Below image shows how plugin works in **GIMP 3.0.8 (rev 2)**

![Image showing how plugin works in GIMP 3](demo.gif)

# How it works

The plugin creates the simple gradient mask under the hood, that manipulates the alpha channel.  
The transition of between the two layers is created in the middle of an image `height` dimension.  
As a user, you can also specify the percentage value how dense gradient you want to use.

# Installation

- [Download the plugin](https://github.com/Patrix9999/blend-two-layers-transition/archive/refs/heads/main.zip)
- Put in `plugins` dir, example path for windows users: `%AppData%\GIMP\3.0\plug-ins\`
- Extract the `blend-two-layers-transition` directory directly into `plug-ins` folder
- Enjoy!

# Debugging the plugin

The easiest way to debug the plugin, is to launch it `gimp-3.0` with the following arguments: 
- `--verbose`
- `--console-messages`

Here's the minimal example how you can launch `gimp-3.0.exe` under windows using **powershell** (be sure to `cd` into `YourDir\GIMP 3\bin` first!):
```ps
./gimp-3.0.exe --verbose --console-messages
```

**NOTE!** You need to restart the `gimp-3.0` each time, you make changes.