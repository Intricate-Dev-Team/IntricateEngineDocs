# C# Style

This section defines stylistic, structural, and formatting standards for C# source code.

!!! info "Naming Conventions"
    Naming conventions are not covered in this section.  
    See [Naming Conventions](naming-conventions.md).

---

## Formatting

Intricate uses [.editorconfig](https://editorconfig.org/) to enforce code-styling. In **Visual Studio**, the code formatter can be run by pressing the hotkey chord `Ctrl+K, Ctrl+D` on an open file.

!!! info
    All formatting rules denoted by a `*` are automatically applied by **.editorconfig** or **Visual Studio**.

### Indentation

- Use **4 spaces** per indentation level.\*
- Do not use tab characters.
- Continuation lines should be indented once with respect to the current indentation level.\*

!!! tip
    Pressing the tab key will add **4 spaces** instead of a tab character for indentation when **.editorconfig** is enabled.

### Line Length

- Soft limit: **130 characters**
- Split long expressions across multiple physical lines if required.
- Break long expressions at logical boundaries (e.g. in-between parameters of a method call.)

### Whitespace and Newlines

- Use **exactly one blank line** between:
    - Method definitions
    - Class members grouped by purpose
    - Logical blocks of code grouped by purpose
- Do not leave trailing whitespace.\*
- Use **exactly one space** after commas and semicolons inside parameter lists and other constructs.\*
- Use **exactly one space** before and after binary operators.\*
    - Example: `a + b`, `x == 3`, `value * 2`
    - **No spaces** for:
        - Indexing: `arr[i]`
        - Unary operators: `-x`, `!flag`, `~mask`, `++i`, `i--`
- Insert a **final newline** at the end of source files.\*

!!! warning
    More than one blank line should **never** be used anywhere other than in-between the `using` directives and the namespace declaration.

### Braces

- Use the **Allman style**\*:

``` C#
public void Foo()
{
    if (true)
    {
        // Block-bodies covering multiple lines must always have the opening brace on a newline.
    }
}
```

- Omit the braces for single-line control-flow blocks:

``` C#
if (true)
    Foo();
else
    Bar();

if (printNumbers)
{
    foreach (int i in numbers)
        Console.WriteLine(i);
}
```

- Empty function bodies should be defined as:

``` C#
public void Foo() { } // Inlined empty braces with a space in-between
```

### Control Flow Blocks

- Do not inline control-flow blocks:

``` C#
// Don't do this
while (true) DoWork();

// Do this instead
while (true)
    DoWork();
```

- `else`, `catch`, `finally` and `case` must always appear on its own line.
- Prefer ternary expressions over simple `if-else` blocks.

---

## File Structure

### File Layout

- Order elements in the following sequence unless justified otherwise:
    1. File header, version history or copyright (if applicable)
    2. Using directives
    3. **Two blank lines**
    4. Namespace declaration
    5. Enum declaration(s)
    6. Class/struct/record/interface declaration(s) (in order of dependency)
        Type layout:
        1. Constants
        2. Nested Types
        3. Constructors (`static` → `public` → `internal` → `protected` → `private`)
        4. Destructor/Finalizer
        5. Public methods
            - Overrides (including `ToString`, `Equals`, `GetHashCode`)
            - Interface methods
            - Conversion operators
            - Operator overloads
        6. Public properties
        7. Public events
        8. Public static readonly fields
        9. Public static methods
        10. Internal/protected methods
        11. Private methods
        12. Private static methods
        13. Instance variables (`public` → `internal` → `protected` → `private`)
        14. Private properties (rare, avoid using)

### Using Directives

- Place `using` statements **outside of namespaces**.
- Group and sort (alphabetical):
    1. Our project's namespaces
    2. External package/submodule namespaces
    3. System namespaces
- Insert **two blank lines** after the final `using` directive **before the namespace** declaration.

---

## Comments

### Documentation

Use XML documentation comments for:

- Public types
- Public and protected members

!!! note
    We may switch to Doxygen comments soon.

### Commenting Style

See: [Comments](comments.md).

---

## Code Style

### Modifier Order

Field modifiers should appear in the following order:

``` C#
// This ordering is enforced by .editorconfig and can be auto-applied from Visual Studio hints
public, private, protected, internal, static, extern, new, virtual, abstract, sealed, partial, override, readonly, unsafe, volatile, async
```

### Expression Syntax

- Use expression-bodied members for trivial property getters and simple inline methods:

``` C#
public int Count => m_Count;

public float Mass
{
    get => Bindings.RigidBody_GetMass(m_NativeID);
    set => Bindings.RigidBoody_SetMass(m_NativeID, value);
}

public bool Awake() => Bindings.RigidBody_Awake(m_NativeID);

```

- Use block-bodies for everything else.

### Pattern Matching

- Favor pattern matching over explicit type casting when checking types.

``` C#
public class Entity 
{ 
    /* ... */

    // Explicit type casting in a block-bodied member
    public override bool Equals(object other)
    {
        if (other is null)
            return false;

        if (other is not Entity)
            return false;

        return m_NativeID == ((Entity)other).m_NativeID; 
    }

    // Pattern matching in an expression-bodied member
    public override bool Equals(object other) => obj is Entity entity && (m_NativeID == entity.m_NativeID);
}
```

### Immutability

- Prefer `readonly` where applicable.
- Avoid modifying method parameters unless it's an `out` or `ref` parameter.

### LINQ

- Using LINQ is encouraged for clarity and expressiveness, but not required.
- Avoid deeply nested and "clever" LINQ chains - keep it readable.

### Unsafe

- Minimize the `unsafe` scope as far as possible.
- Avoid declaring methods and types as `unsafe`.

``` C#
// Avoid declaring the method as unsafe
public void CopyToNative(ReadOnlySpan<byte> data, nint dst)
{
    ulong sizeBytes = data.Length; // Unsafe is not needed for this

    // Rather open the unsafe block here
    unsafe
    {
        fixed (byte* ptr = data)
            Buffer.MemoryCopy(ptr, dst.ToPointer(), sizeBytes);
    }
}
```

- Avoid passing and storing raw pointers, use `nint` instead.

---

## Source Control Expectations

- Changes must adhere to this style guide.
- Automated formatting tools should be run prior to commit.

!!! note
    In-future we may implement CI linting and formatting.

---
