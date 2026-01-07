# Comments

This section outlines the conventions used for writing comments in code.

---

## Comment Structure

**General format of a comment:** 

``` C++
// <COMMENT_TAG>([optional metadata]): <short imperative summary>
```

**Rules:**

- Always include a space between the comment symbol (`//`) and the start of the comment text.
- Write comments in **imperative mood** to keep phrasing concise and action-oriented. (Example: *`"Validate session token"` instead of `"Validating session token"` or `"This validates the session token"`*.)

**Metadata formatting:**

When including metadata, list multiple elements as **comma-separated values** without spaces.

Example:
``` C++
// FIXME(Adam,medium): These allocations are leaking memory and need to be fixed!
```

---

## Comment Tags

| Tag           | Metadata      | Usage                                      | Example                                     |
|---------------|---------------|--------------------------------------------|---------------------------------------------|
| **TODO** | author | Identify work that still needs to be completed. | `// TODO(Hasan): Pass params by const-reference here` |
| **FIXME** | author, severity(low\|medium\|high) | Identify code known to be broken or incorrect. | `// FIXME(Adam,medium): Need to fix this line` |
| **NOTE** | - | Document reasoning, context, or non-obvious design decisions. | `// NOTE: This field is required by the Renderer` |
| **INVARIANT** | - | Document assertion conditions that must always be true. | `// INVARIANT: Vector3 index must be in range [0,2]` |
| **REVIEW** | requested-reviewer | Request a review on a specific line or block. | `// REVIEW(Azaam): Should these fields be lazily-allocated?` |
| **DEPRECATED** | as-of-date(dd/mm/yyyy) | Mark an API or function as deprecated. | `// DEPRECATED(19/06/2025): Replaced this function with Foo()` |
| **WTF** | - | Identify confusing or unexpected behavior requiring investigation. *(Use sparingly.)* | `// WTF: Behavior differs between debug and release builds` |

---

## Discouraged Comment Styles

Avoid the following patterns:

``` C++
// This code makes no sense
```

``` C++
// Fix this later
```

!!! note
    This pattern may be used for documenting `private`/`internal` members as well as non-obvious code behavior inside methods.

Instead, prefer tagged comments with clear, traceable meaning:

``` C++
// FIXME(Muddathir,high): Investigate undefined behavior when size < capacity
```

``` C++
// NOTE: Uses std::launder due to ABI assumptions in external library
```
