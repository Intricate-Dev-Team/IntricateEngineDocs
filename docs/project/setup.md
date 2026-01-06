# Setup

This document serves as a guide on how to setup Intricate after cloning.

---

## Prerequisites

- Intricate must be **recursively cloned** to properly pull all the required submodules.
- Intricate uses [Premake5](https://premake.github.io/) as its build system.

## How To Setup
- Run the setup script [Setup.py](../../Scripts/Setup.py), which will validate and or install the required versions of **Python**, **.NET** and the **Vulkan SDK**.
    - You may have to run the script multiple times and or restart your computer as prompted by the script for all the required environment variables to be properly registered.
- Once all this is done, the script will call the [GenerateVS.py](../../Scripts/GenerateVS.py) script which then uses Premake to generate all projects files targetting **Visual Studio 2022**.

**Required environment variables:**
- Python must be added to `PATH`
- `DOTNET_ROOT`: path to the root of the installed .NET runtime.
- `VULKAN_SDK`: path to the root of the installed Vulkan SDK.
- `VK_SDK_PATH`: synonym for `VULKAN_SDK`.

> **NOTE**: These variables will be automatically registered by the setup script however, in the event that the script fails to register them, you will need to do so manually!

---
