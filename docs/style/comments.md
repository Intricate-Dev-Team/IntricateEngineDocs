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
  
## Doxygen Guidelines  

### 📍 Where to use?

- At the **header** of every file, explaining:
    - Filename
    - Brief description of file's purpose and contents.
    - Author(s)
    - Date of Creation
- **Above** every **Method**, describing:
    - The purpose briefly, in one line
    - The method in more detail. (What algorithms were used, unique decisions made.)
    - The parameter(s) and result.
- **Class/Struct** documenation:
    - Brief class description
    - Detailed usage information.
    - Template parameters.
    - Important Member relationships

### :writing_hand: Writing Style guidelines

**Grammar & Tone:**

- Present tense

  |  |  |
  |--|--|
  | ❌ Bad | `The function will sort the array.`|
  | ✅ Good| `Sorts the array using quicksort.`|

- Active voice: *Subject + Verb + Object*

    |  |  |
    |--|--|
    | ❌ Bad | `The integer is modified by the method.`|
    | ✅ Good| `The function modifies the integer.`|

- Write in Third Person instead of First Person:

    |  |  |
    |--|--|
    | ❌ No usage of: <em>I, me, we</em>. | `# I calculate the average here.` <br> `# We initialize the module`|
    | ✅ Use Third person| `Calculates the average of the values.`<br>`Initializes the communication module.`|

- Be direct and concise,

- Start summaries with a verb:

    |  |  |
    |--|--|
    | ❌ Bad | `This function is responsible for performing the task of data validation.` |
    | ✅ Good| `Validates input data format.`|

### TEMPLATES

**File headers [C++ only]:**

    /**
     * @file    filename.cpp
     * @brief   Brief description of file purpose
     * @author  John Doe (optional)
     * @date    2024-01-15
     * 
     * Detailed description of file contents, context, and usage...
     * Can span multiple lines...
     * 
     * @NOTE: ...    Important notes about this file
     * @WARNING: ... Any warnings for developers
     */

**Method Documentation:**

- C++:

        /**
        * @brief   One-line description of function purpose
        * 
        * Detailed description including algorithm, edge cases,
        * performance characteristics, etc.
        * 
        * @param   param1 Description of first parameter
        * @param   param2 Description of second parameter
        * @return  Description of return value
        * /

- C#:

        /// <summary>
        /// Calculates the sum of two integers.
        /// </summary>
        /// <param name="left">The first integer operand.</param>
        /// <param name="right">The second integer operand.</param>
        /// <returns>The sum of the two integers.</returns>
        public static int Add(int left, int right)
        {
            return left + right;
        }

**Class Documentation:**

- C++

        /**
        * @class   ClassName
        * @brief   Brief description of class purpose
        * 
        * Detailed explanation of class responsibilities, usage patterns,
        * and important design decisions.
        * 
        * @param  Description of template parameter requirements
        */
        public class ClassName<T>
        {
            // Class implementation
        }

- C#:

        /// <summary>
        /// A summary about this class.
        /// </summary>
        /// <remarks>
        /// These remarks would explain more about this class.
        /// In this example, these comments also explain the
        /// general information about the derived class.
        /// </remarks>
        public class MainClass
        {
        }

- For more examples, look here: <https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/examples>

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
