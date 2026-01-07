# IDE Requirements

This section specifies the *Integrated Development Environment* (IDE) requirements for development on Intricate.

---

## IDE
Intricate development requires **Microsoft Visual Studio 2022 or newer**. A secondary text editor may also be used with **Visual Studio**, but should **not replace it**. Suggested secondary text editors are:

- VS Code
- Sublime
- Vim (DOS mode)
- Neovim (DOS mode)

!!! tip
    Intricate uses [.editorconfig](https://editorconfig.org/) to enforce code-styling. For any other text editors, please ensure that they support **.editorconfig** before using them. For **VS Code**, this extension should be used: [EditorConfig for VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig).

---

## Visual Studio Requirements

The following **Visual Studio** workloads are required:

- **.NET desktop development**
- **Desktop development with C++**
- **Python development** (optional)

The following **Visual Studio** individual components are required:

- **.NET**
    - .NET 10.0 Runtime
    - .NET SDK
- **Code tools**
    - NuGet package manager
    - NuGet targets and build tasks
- **Compilers, build tools, and runtimes**
    - Incredibuild - Build Acceleration
- **SDKs, libraries and frameworks**
    - Windows 11 SDK (latest)
    - Windows Performance Toolkit
    - Windows Universal C Runtime

!!! note
    Some of the individual components listed above may already be included by the selected workloads. Ensure they are all installed in the **Visual Studio Installer**.

---

## Recommended VS Code Extensions

- [C/C++ Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools-extension-pack)
- [C# Dev Kit](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit)
- [EditorConfig for VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)
- [Lua](https://marketplace.visualstudio.com/items?itemName=sumneko.lua)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Shader languages support for VS Code](https://marketplace.visualstudio.com/items?itemName=slevesque.shader)
- [YAML](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)

---
