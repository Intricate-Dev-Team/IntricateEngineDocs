# Setup

This section outlines how to setup Intricate after cloning the repository.

---

## Cloning

Intricate must be **recursively cloned** to properly pull all the required submodules. Recursive cloning may be done either via the **GitHub Desktop** application, or with the following command:
``` shell
git clone --recurse-submodules https://github.com/DnA-IntRicate/IntricateEngine
```

---

## Build System

Intricate uses [Premake5](https://premake.github.io/) as its build system. The premake build system is configured to generate **Visual Studio** project and solution files off of **Lua** build scripts called **premake files**. These build scripts can be found littered around the repository and are most-commonly named `premake5.lua`.

!!! example "Example Premake file"
    ``` lua
    workspace "IntricateEngine"
        configurations { "Debug", "Release" }

    project "IntricateEditor"
        kind "ConsoleApp"
        language "C++"
        files { "**.hpp", "**.cpp" }

        filter "configurations:Debug"
            defines { "_IE_DEBUG" }
            symbols "On"

        filter "configurations:Release"
            defines { "_IE_RELEASE" }
            optimize "On"
    ```

---

## How To Setup
- Run the setup script `Setup.py`, which will validate and or install the required versions of **Python**, **.NET** and the **Vulkan SDK**.
    - You may have to run the script multiple times and or restart your computer as prompted by the script for all the **required environment variables** to be properly registered.
- Once all this is done, the script will call the `GenerateVS.py` script which then uses Premake to generate all projects files targetting **Visual Studio 2022**.

**Required environment variables:**

- Python must be added to `PATH`
- `DOTNET_ROOT`: path to the root of the installed .NET runtime.
- `VULKAN_SDK`: path to the root of the installed Vulkan SDK.
- `VK_SDK_PATH`: synonym for `VULKAN_SDK`.

!!! warning
    These variables will be **automatically registered** by the setup script however, in the event that the script fails to register them, you will need to do so **manually**!

---
