# C++ Style

This section defines stylistic, structural, and formatting standards for C++ source code.

> **Note**: Naming conventions are not covered in this section.  
> See: [Naming Conventions](naming-conventions.md).

---

## Formatting

Intricate uses [.editorconfig](https://editorconfig.org/) to enforce code-styling. In **Visual Studio**, the code formatter can be run by pressing the hotkey chord `Ctrl+K, Ctrl+D` on an open file.

> All formatting rules denoted by a `*` are automatically applied by **.editorconfig** or **Visual Studio**.

### Indentation

- \*Use **4 spaces** per indentation level.
- Do not use tab characters.
- \*Continuation lines should be indented once with respect to the current indentation level.

> **Note:** Pressing the tab key will add **4 spaces** instead of a tab character for indentation.

### Line Length

- Soft limit: **130 characters**
- Split long expressions across multiple physical lines if required.
- Break long expressions at logical boundaries (e.g. in-between parameters of a method call.)

### Whitespace and Newlines

- Use **exactly one blank line** between:
    - Method definitions
    - Class members grouped by purpose
    - Logical blocks of code grouped by purpose
- \*Do not leave trailing whitespace.
- \*Use **exactly one space** after commas and semicolons inside parameter lists and other constructs.
- \*Use **exactly one space** before and after binary operators.
  - Example: `a + b`, `x == 3`, `value * 2`
  - **No spaces** for:
    - Indexing: `arr[i]`
    - Unary operators: `-x`, `!flag`, `~mask`, `++i`, `i--`
    - Scope resolution: `std::string`
- \*Insert a **final newline** at the end of source files.

> **Note**: More than one blank line should never be used anywhere other than in-between the `#include` directives and the namespace declaration.

### Braces

- \*Use the **Allman style**:
``` C++
void Foo()
{
    if (true)
    {
        // Block-bodies covering multiple lines must always have the opening brace on a newline.
    }
}
```

- Omit the braces for single-line control-flow blocks:
``` C++
if (true)
    Foo();
else
    Bar();

if (printNumbers)
{
    for (int i : numbers)
        _IE_CORE_TRACE("{0}", i);
}
```

- Empty function bodies should be defined as:
``` C++
void Foo() { }; // Inlined empty braces with a space in-between ended with a semicolon
```

- \*Multi-line lambda function bodies should have their braces indented:
``` C++
Helpers::FetchExecuteIfValid<Scene>(nativeID, [&](const Ref<Scene>& scene)
    {
        scene->DestroyEntity(entityID);
    });
```

### Control Flow Blocks

- Do not inline control-flow blocks:
``` C++
// Don't do this
while (true) DoWork();

// Do this instead
while (true)
    DoWork();
```

- `else`, `catch` and `finally` must always appear on its own line.
- Prefer ternary expressions over simple `if-else` blocks.

### Pointers and References

- \*Place `*` and `&` adjacent to the type:
``` C++
int* ptr;
const Foo& ref;
```

- Multiple declarations per line are discouraged.

### Preprocessor Directives

- Preprocessor directives should be indented and follow an independent indentation level:
``` C++
#ifdef _IE_ENABLE_LOGGING
#   define _IE_NATIVE_USE_TYPE_TRACKING
#endif // _IE_ENABLE_LOGGING

#ifdef _IE_NATIVE_USE_TYPE_TRACKING
#   include <IntricateEngine/Core/Core.hpp>
#endif // _IE_NATIVE_USE_TYPE_TRACKING
```

- Prefer inserting ending comments to preprocessor `#if` directives as seen above.

---

## File Structure

### Header File Layout

- Order elements in the following sequence unless justified otherwise:
    1. File header, version history or copyright (if applicable)
    2. Header guard (`#pragma once`)
    3. Includes
    4. Module imports
    5. **Two blank lines**
    6. Namespace declaration
    7. Enum declaration(s)
    8. Class/struct declaration(s) (in order of dependency)
        Type layout:
        1. Constants
        2. Nested Types
        3. Constructors (`public` → `protected` → `private`)
        4. Destructor
        5. Public methods
            - Overrides
            - Specializations
            - Conversion operators
            - Operator overloads
        9. Public static constants
        10. Public static methods
        11. Protected methods
        12. Private methods
        13. Private static methods
        14. Instance variables (`public` → `protected` → `private`)

- Access specifiers should be grouped and not interleaved.
- Forward-declarations should be made in the appropriate scope or just before its first reference.

### Source Files

- Order elements in the following sequence unless justified otherwise:
    1. Precompiled header include
    2. Includes
    3. Module imports
    4. **Two blank lines**
    5. Namespace declaration
    6. Constants
    6. Nested namespaces with helpers (such as a `Utils` namespace)
    7. Internal global variables
    8. Internal methods
    9. Static member variable definitions
    10. Class/struct methods (in the order seen in the header file)

### #Include Directives

- Place `#include` directives **outside of namespaces**.
- Local includes should be specified using quotes: `#include "MyHeader.hpp"`.
- Non-local includes should be specified using angle brackets: `#include <IntricateEngine/Math/Vector2.hpp>`.
- Headers should always be included from top-to-bottom in terms of folder depth.
- Group and sort includes alphabetically in the following order:
    1. Precompiled header/local includes
    2. Paired header (for a source file)
    3. Current project's headers
    4. Intricate headers
    5. Vendor headers
    6. STL headers
    7. C standard headers
    8. Platform headers (`d3d11.h`, `windows.h`, `sys/mman.h`)
- Insert **two blank lines** after the final `#include` directive **before the namespace** declaration.

---

## Comments

### Documentation

Use XML documentation comments for:
- Public types
- Public and protected members

> **Note**: We may switch to Doxygen comments soon.

### Commenting Style

See: [Comments](comments.md).

---
