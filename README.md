# Introduction

This is a simple [**GIMP 3**](https://www.gimp.org/downloads/) plugin written in **python 3** that allows you to blend two layers together.

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