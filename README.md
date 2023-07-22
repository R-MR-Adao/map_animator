# Map animator

![](doc/map_animator_wide.png)

A `Python`-based tool to animate a pre-set trajectory over a map.

<div align="center">
  <image src="doc/example_output.gif" />
</div>

# Table of Contents
- [Map animator](#map-animator)
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [`Python` Installation](#python-installation)
  - [Module Requirements](#module-requirements)
  - [Launch the tool](#launch-the-tool)
- [Using the tool](#using-the-tool)
  - [Designing your maps](#designing-your-maps)
  - [Generating the animation trajectory](#generating-the-animation-trajectory)
  - [Building the animation](#building-the-animation)
- [Configuration file](#configuration-file)
- [Example](#example)

![](doc/UnderConstruction.png)

# Getting Started

If you are already a `Python` user, you will have no trouble using this tool.
All you need to do is to make sure your environment fulfills the [requirements](#module-requirements) and you're good to go.

However, for those less experienced with `Python`, the following sections explain how you can get your setup up and running.

## Installation

In this open-source repository, I am sharing the source code that implements the tool.
Thus, there is no installation package required to use it.

If you don't have it already, all you need to do is to
  1. Download the source code by cloning the repository or pressing the `Code` -> `Download ZIP` buttons and extracting the files into a directory of your choice.
  2. [Install `Python`](#python-installation) in your machine
  3. Install the [required modules](#module-requirements)
  4. [Launch the tool](#launch-the-tool) from the terminal


## `Python` Installation

If you already have `Python` installed in your machine, you can skip this section.
Otherwise, you can follow these steps to install it:

1. **Visit the official website:** Go to the official `Python` website at [https://www.python.org/downloads/](https://www.python.org/downloads/), download and install `Python` for your operating system.

2. **Verify the installation:** Open a terminal (or command prompt) and type the following command:

    ```bash
    python --version
    ```

    If `Python` is installed correctly, you will see the version number displayed.
    If it gives you an error message saying "`'python' is not recognized as an internal or external command, operable program or batch file.`", then you may need to manually add `Python`'s path to your system variables, as described below.

3. **Adding `Python` to PATH (Windows users without admin rights):** If you don't have admin rights on your Windows machine, the installer won't be able to automatically add `Python` to the PATH system variables. However, you can add it to your user environment variables:

- After installing Python, navigate to the `Python` installation directory. If you cannot locate your `Python` installation folder, you can use the following command
  ```bash
  where python
  ```
- Copy the path of the `Python` installation directory.
- Search for "Environment Variables" in the Windows search bar and click on "Edit the system environment variables." In the System Properties window, click on the "Environment Variables..." button. In the Environment Variables window, under the "User variables" section, click "New."
- Set the variable name to `PATH` and paste the copied `Python` installation directory path as the variable value. Click "OK" to save the changes.

## Module Requirements

The tool relies on specific `Python` modules to function correctly. These modules and their versions are listed in the requirements.txt file.

To install the required modules, open a terminal (or command prompt) and navigate to the directory where you have extracted the source code. Then, run the following command:

```bash
pip install -r requirements.txt
```

This command will automatically read the requirements.txt file and install all the necessary dependencies.

## Launch the tool

Once you have completed the installation steps and installed the required modules, you can launch the tool by either:

1. double-clicking on the [launcher.bat](launcher.bat) file, or
2. opening a terminal (or command prompt) and navigate to the directory where the source code is located. Then, run the following command:
    ```bash
    cd [map_animator_directory]
    python launcher.py
    ```

This will start the tool, and you can now proceed to use it as described in the next section.

# Using the tool

Producing a map animation with this tool can be done in just three steps:

1. [Designing your maps](#designing-your-maps)
2. [Generating the animation trajectory](#generating-the-animation-trajectory)
3. [building the animation](#building-the-animation)

When you [launch the tool](#launch-the-tool), you can choose the execution mode by editing the `mode` parameter in the [config.json](config.json) file.
This parameter can take the following options:

- `"generate"`: to generate the animation trajectory
- `"animate"`: to build the animation
- `"CLI"` (default): to choose the execution mode by passing the designated keyword to the command line interpreter.

Upon launching the tool using the `"CLI"` mode option, you are presented with the following interface:

```
Please type one of the following options:
    'g' to generate a new trajectory
    'a': to build animation
    'q': to quit the CLI
 ("g", "a", "q"): _
```

which you can use to call the `Animator` methods.

The `"g"` and `"a"` commands can be called multiple times.
Every time a command is inserted, the config and data files are reloaded.
This allows you to iteratively optimize the animation parameters in the [configuration file](#configuration-file) described ahead

## Designing your maps

This step must be done using any `CAD` software of your choice.
IF you have no preference, I would personally recommend [Inkscape](https://inkscape.org/), an awesome free vector graphical editor that will allows building all sorts of illustrations.

In order to use this tool, you will have to export at least two images: (in any normal bitmap format such as `*.jpeg` or `*.png`):

1. The actual map that will show in the background
2. The trajectory map: almost empty image with the exact same dimensions as the background map, but containing only a fine line along the trajectory you wish to animate.

**Important**: Best results are obtained by exporting the road as a basic color (pure red, green, or blue). The chose color must match the `path->color` configuration in the [configuration file](#configuration-file)

Here is an example of a simple map design.

<div align="center">
  <image src="doc/example_simulation.png" />
</div>

For better performance
   1. "simulate" the span of the visualization window
   2. take note of its dimensions (in pixels) and add them to the `display->figure_size` configuration in the [configuration file](#configuration-file)
   3. make sure to have enough of a margin around the visualization window, to prevent stepping out of your map design.

Once you have a design, save the background and road files in the [resources](resources/) folder.
Make sure that the file names designated in the `maps->map_back` and `maps->map_road` settings of the [configuration file](#configuration-file) match the file names under which you stored your design images.

Examples of the two required map image files can be found in [map_back.png](resources/map_back.png) and [map_road.png](resources/map_road.png) in the [resources](resources/) folder.

## Generating the animation trajectory

To generate a new trajectory either:
 - set `mode` to `"generate"` and execute the launcher script
 - set `mode` to `"cli"`, execute the launcher script, and choose the `"g"` option

Once launched, the `Animator` will identify the trajectory path from the input `map_road` and apply a recursive filter to sort the correct order of the points in the supplied image.
The path generation results can be optimized by editing the `filters->diff_threshold` and `filters->recursion_limit` parameters.

During the path generation, you will be informed of the trajectory filter progress

```
Apllying recursive positional filter 0/2
Apllying recursive positional filter 1/2
Apllying recursive positional filter 2/2
Save coordinates to data file? ("y", "n"): _
```

Despite the recursive filters, the generated path will likely contain a few unsorted points at the end of the trajectory.

The figure below illustrates the a map design and the generated trajectory.
As it can be seen, the generated path is mostly correct except for a few straight lines at the end of the path.

The best way to deal with this effect is to save the generated path as a text data file, and delete the last few points (it should be pretty simple to identify the erroneous points).

<div align="center">
  <image src="doc/example_generated_path.png" />
</div>

Once you are done with generating and editing the animation path, make sure that the exported file name matches the `path->path_road` setting in the [configuration file](#configuration-file).
An example of an exported data file can be found in [path_road.dat](resources/path_road.dat) in the [resources](resources/) folder.

## Building the animation

To build the animation either:
 - set `mode` to `"animate"` and execute the launcher script
 - set `mode` to `"cli"`, execute the launcher script, and choose the `"g"` option

Cone launched, you will see the generation being rendered, and a loading bar will be shown on the terminal with a prediction of the remaining time

```
  1%|█                                                 | 4/342 [00:01<01:17,  4.34it/s]
```

Here is the result of using the current [config.json](config.json) file and resources available in the [resources](resources/) folder

<div align="center">
  <image src="doc/example_output.gif" />
</div>

Once finished, if the `output->mode` setting is set to `"save"`, you will have a chance to browse an select a file in which to save the generated animation. 

# Configuration file

The configuration file has the following structure
```jsonc
{
    "mode": "cli",                                  # execution mode
    "maps": {                                       # list of maps to be imported
        "map_back": "resources/map_back.png",       # "actual" map to show on the background
        "map_road": "resources/map_road.png"        # map containing the path to thread along
    },
    "path":{                                        # path settings
        "path_road": "resources/path_road.dat",     # data file where generated path is stored
        "color": [0,0,255],                         # color of road line in map_road
        "starting_direction": "east"                # path starting direction
    },
    "filters": {                                    # path-generation filters
        "diff_threshold": 5,                        # derivative rejection threshold
        "recursion_limit": 2                        # number of filter iterations
    },
    "output": {                                     # output settings
        "mode": "save",                             # "save" / "preview"
        "skip": 5,                                  # number of points to skip for animation
        "frame_duration": 50,                       # (ms) duration of each frame
        "loop": 0                                   # number of git file loops (0 for infinite)
    },
    "display": {                                    # display settings
        "figure_size": [960, 540],                  # display figure size
        "FoV": [676, 384],                          # field of view size
        "camera_smooth": 10,                        # camera smooth box width
        "line_width": 8,                            # width of displayed line
        "line_color": [0.7, 0.3, 0],                # displayed line color
        "line_style": "-"                           # displayed line style
    }
}
```

# Example

Here is an example of a personal application used as part of my [video on Instagram](https://www.instagram.com/reel/Cu2I9lXoe4V/?igshid=MTc4MmM1YmI2Ng%3D%3D), to illustrate my trip from Águeda (Portugal) to Bertrange (Luxembourg) and Calais (France).

<div align="center">
  <image src="doc/example_output_2.gif" />
  <p style="text">A reduced size example</p>
</div>
