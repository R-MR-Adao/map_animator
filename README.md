# Map animator

A `Python`-based tool to animate a pre-set trajectory over a map.

# Table of Contents
- [Map animator](#map-animator)
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [`Python` Installation](#python-installation)
  - [Module Requirements](#module-requirements)
  - [Launch the tool](#launch-the-tool)
  - [Using the tool](#using-the-tool)
  - [Configuration file](#configuration-file)

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

1. **Visit the official website:** Go to the official `Python` website at [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Download the installer:** Choose the appropriate installer for your operating system (Windows, macOS, or Linux) and download it.

3. **Run the installer:** Double-click the downloaded installer and follow the on-screen instructions to install `Python` on your machine.

4. **Verify the installation:** Open a terminal (or command prompt) and type the following command:

    ```bash
    python --version
    ```

    If `Python` is installed correctly, you will see the version number displayed.
    
    If it gives you an error message saying "`'python' is not recognized as an internal or external command, operable program or batch file.`", then you may need to manually add `Python`'s path to your system variables, as described below.

5. **Adding `Python` to PATH (Windows users without admin rights):** If you don't have admin rights on your Windows machine, the installer won't be able to automatically add `Python` to the PATH system variables. However, you can add it to your user environment variables:

- After installing Python, navigate to the `Python` installation directory (usually `C:\PythonXX` where `XX` represents the version number).
- If you cannot locate your `Python` installation folder, you can use the following command
  ```bash
  where python
  ```
- Copy the path of the `Python` installation directory.
- Search for "Environment Variables" in the Windows search bar and click on "Edit the system environment variables."
- In the System Properties window, click on the "Environment Variables..." button.
- In the Environment Variables window, under the "User variables" section, click "New."
- Set the variable name to `PATH` and paste the copied `Python` installation directory path as the variable value.
- Click "OK" to save the changes.

    Now, you should be able to run `Python` and `pip` commands from the command prompt.


## Module Requirements
The tool relies on specific `Python` modules to function correctly. These modules and their versions are listed in the requirements.txt file.

To install the required modules, open a terminal (or command prompt) and navigate to the directory where you have extracted the source code. Then, run the following command:

```bash
pip install -r requirements.txt
```

This command will automatically read the requirements.txt file and install all the necessary dependencies.

## Launch the tool

Once you have completed the installation steps and installed the required modules, you can now launch the tool.

Open a terminal (or command prompt) and navigate to the directory where the source code is located. Then, run the following command:

```bash
python map_animator.py
```

This will start the tool, and you can now proceed to use it as described in the next section.

## Using the tool



## Configuration file
