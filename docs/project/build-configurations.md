# Build Configurations

This document lists all of Intricate's build configurations and their intended purposes.

---

## Configurations

Intricate has `4` different build configurations which can be selected from inside **Visual Studio**.

| Configuration | Symbols | Optimizations | Runtime | Console | Asserts  | Logging   | Profiling | Defines         |
|---------------|---------|---------------|---------|---------|----------|-----------|-----------|-----------------|
| Debug         | On      | Off           | Debug   | Visible | Enabled  | All       | Disabled  | `_IE_DEBUG`     |
| Dev           | On      | On            | Release | Visible | Enabled  | All       | Disabled  | `_IE_DEV`       |
| Profiling     | Off     | On            | Release | Visible | Enabled  | All       | Enabled   | `_IE_PROFILING` |
| Release       | Off     | On            | Release | Hidden  | Disabled | File only | Disabled  | `_IE_RELEASE`   |

> **NOTE**: Intricate targets the `x86_64` architecture only.

**When to use each configuration:**
- **Debug:** When you need breakpoints, stack traces, hunting memory leaks and or external debug symbols.
    - Performance in this configuration is **significantly slower** than in **Dev** and **Release**.
- **Dev:** For everyday general development and testing.
    - This is the configuration that should be used for `98.992%` of development.
- **Profiling:** When something is running unusually slow and you need to figure out which function is the culprit.
    - This configuration measures the time taken for each function to execute when called and throws the results into a series of **JSON** files which can be viewed in your browser's **tracing** tool. (e.g. <chrome://tracing> or <brave://tracing>)
    - Performance in this configuration is **massively slower** than in all the others due to the overhead of profiling.
- **Release:** For official distribution. (note that a `5th` configuration named **"Dist""** may soon be added)

---
