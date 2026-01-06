# Naming Conventions

This document defines consistent naming rules used across all projects to improve readability, maintainability, and predictability.
These conventions apply primarily to `C++` and `C#` - and then other languages or frameworks as well, unless the specific language or framework guideline overrides them.

---

## General Principles

- Names must be **clear, descriptive, and unambiguous**.
- Avoid abbreviations unless widely recognized.
- Use whole words where possible - longer more descriptive names are encouraged within reason.
- Acronyms are written in PascalCase (e.g. `HttpRequest`, not `HTTPRequest`).

---

## Casing Rules

| Identifier Type               | Style                      | Example                       |
|-------------------------------|----------------------------|-------------------------------|
| Projects / Solutions          | PascalCase                 | `IntricateEngine`             |
| Classes, Structs, Enums       | PascalCase                 | `DotNetRuntime`               |
| Enum Values                   | PascalCase                 | `ShaderStage.Fragment`        |
| Functions / Methods           | PascalCase                 | `EnqueueToMainThread`         |
| Variables (local)             | camelCase                  | `frameCount`                  |
| Parameters                    | camelCase                  | `frameCount`                  |
| Public Member Variables       | PascalCase                 | `FrameCount`                  |
| Private Member Variables      | PascalCase + `m_` prefix   | `m_FrameCount`                |
| Constants                     | UPPER_CASE                 | `MAX_VERTEX_COUNT`            |
| Private Static Variables      | PascalCase + `s_` prefix   | `s_FrameCount`                |
| Global variables (C++)        | PascalCase + `g_` prefix   | `g_FrameCount`                |
| Internal symbols (C++)        | PascalCase + `_` prefix    | `_AtomicRefCount`             |
| Template Type Parameters (C++)| PascalCase + `_` prefix    | `_Ty`                         |
| Preprocessor directives (C++) | UPPER_CASE + `_IE_` prefix | `_IE_PROFILE_FN`              |
| Namespaces (C++)              | PascalCase                 | `IntricateEngine::Interop`    |
| Namespaces (C#)               | PascalCase                 | `IntricateEngine.Interop`     |
| Interfaces (C#)               | PascalCase + `I` prefix    | `IEditorPanel`                |
| Properties (C#)               | PascalCase                 | `SqrMagnitude`                |
| Generic Type Parameters (C#)  | PascalCase + `_` prefix    | `_Ty`                         |
| Internal symbols (Py)         | PascalCase + `_` prefix    | `_DeleteFolder`               |
| Source Code Files             | PascalCase                 | `Renderer.cpp`                |
| Markdown Source Files         | kebab-case                 | `naming-conventions.md`       |
| Folders                       | PascalCase                 | `IntricateEngine/`            |

> **Note**: C++ specfic directories, Premake files, Git artifacts and other miscellaneous config files are exempt from these naming conventions. Name according to the convention required by the relevant toolchain.

---

## Boolean Naming

Boolean function and variable names should indicate a condition or state.

**Preferred:**
- `IsVisible`
- `HasTransparency`
- `UseCache`
- `ShouldRebuild`

**Avoid These:**
- `Visible`
- `Transparency`
- `Cache`
- `Rebuild`

---

## Function/Method Naming

Functions should be **action-oriented** and effectively describe their behavior using *verbs* - even if it means that the function name may become longer. Avoid unreadable abbreviations!

| Action Category       | Prefix Examples        | Function Examples                 |
|-----------------------|------------------------|-----------------------------------|
| Get value             | `Get`                  | `GetTextureCount()`               |
| Set value             | `Set`                  | `SetClearColor()`                 |
| Create object         | `Create`               | `CreatePipeline()`                |
| Compute value         | `Calculate`, `Compute` | `ComputeHash()`                   |
| Validate input        | `Is`, `Has`, `Can`     | `IsValidPath()`                   |
| Search object         | `Lookup`, `Fetch`,     | `LookupID()`                      |
| Engine-level events   | `On`                   | `OnKeyPressEvent()`               |
| Actions               | `Start`, `Update`      | `Start()`                         |

> **Note**: These are only a small example subset of all the different possible action categories.

---

## Namespace Naming

- Namespaces may be created for the subsystems that absolutely require them - which should be decided upon through team discussion.
- All new namespaces within a project must be a sub-namespace of the project's namespace.

**Example:**
- `IntricateEngine.Interop` is a sub-namespace of `IntricateEngine` in the project `IntricateEngine.NET`.

---

## Type Naming (Classes, Structs, Enums & Interfaces)

- Class names should be **nouns** clearly describing what the class does and or encapsulates.
- C# Interfaces **must** use the `I` prefix for quick identification.
- Avoid using type names for unrelated purposes (e.g. `Manager` when no managing occurs).

**Examples:**
- `TextureCache` (noun clearly identifies what this type encapsulates)
- `AssetManager` (acceptable if this type genuinely manages assets)
- `Utils` (avoid this! Split responsibilities into meaningful classes)

---

## Abbreviations

Allowed common abbreviations:
- `ID`, `GUID`, `URL`, `HTML`, `UI`, `GUI`, `API`, `GPU`, `CPU`

Avoid local or project-specific abbreviations unless documented or blatantly-obvious.

**Example defined abbreviations:**
- `IE`: IntricateEngine
- `VBO`: Vertex Buffer Object
- `VK`: Vulkan
- `D3D`: DirectX/Direct3D
- `SRV`: DirectX Shader Resource View
- `RTV`: DirectX Render Target View

---

## File Naming Rules

File names should reflect the primary type or purpose. One main class or responsibility per file where practical.

**Examples:**
- The class `FrameBuffer` belongs inside `FrameBuffer.cs`.
    - The struct `FrameBufferSpecification` which is directly related to `FrameBuffer` also belongs inside `FrameBuffer.cs`.
- The file `BindingsCommon.hpp` contains a collection of all the shared behaviors of the C++ interop bindings.

## Folder Naming Rules

Folders are created for every major or minor subsystem that requires the implementation of multiple source files. (e.g. There are many source files part of the `Math` library, therefore these files are deserving of their own folder: `IntricateEngine/Math/`).

Folders should always be named in **PascalCase** except in instances where a certain directory tree may either currently or in-future be made web-accessible; such as the `Docs/` folder - which uses **kebab-case** as is standard for web traffic.

---
