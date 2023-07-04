# Minecraft Map Tools

A tool to download maps from Dynmap and JourneyMap.

## Features

- Download maps from a Dynmap server via Minecraft coordinates, grid reference, and Dynmap tile coordinates
- Download maps from a JourneyMap server via Minecraft coordinates and grid reference
- Convert Minecraft region coordinates to grid references and vice versa
- Convert Minecraft coordinates to Dynmap tile coordinates and vice versa
- Ability to switch between multiple servers

## Usage

### Servers

Minecraft Map Tools allows you to register multiple servers and quickly switch between then. Each server contains its
own **Dynmap URL** and **JourneyMap URL**.

If a server doesn't contain a Dynmap or JourneyMap instance, the relevant URL field can be left blank. **Ignore SSL
certificate validation** can be checked if the server uses self-signed certificates.

### Downloading Maps

Once a server is selected, you will be able to download maps. You can specify whether to input the download extends as Minecraft coordinates, grid references, or Dynmap tile coordinates (only available for downloading from Dynmap).

You will also be able to choose where and what map to download. For example, with Dynmap you could download **world - flat** or with JourneyMap you could download **topo**.

When you have filled in the required details, specify an output directory and click **Download**. Minecraft Map Tools will download each tile individually and stitch them together into one image.

## Building

Python 3 must be installed in order to build this tool. If you are using the pre-built binary found in
the [Releases](https://github.com/ryanbester/minecraft-map-tools/releases) section, Python shouldn't need to be
installed.

```bash
# Install dependencies
pip install -r requirements.txt
# Run the application
python3 main.py

# Create an executable with PyInstaller
pyinstaller main.spec
```
