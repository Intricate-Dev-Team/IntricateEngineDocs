# Bindings Generator

This section discusses the purpose of the **Bindings Generator**, how it works, and how to use it.

---

## Foreword On C# Interop

For the interop systems to work correctly, there has to be a way for `C#` code to be able to call into `C++` code. The way we do this in Intricate, is by leveraging the [LibraryImport](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke-source-generation) system in C#, which is built off of the older [DLLImport](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.dllimportattribute?view=net-10.0) system.

For `C#` to be able to call `C++` code, a **LibraryImport** stub method must be present in `C#`, and this stub must map to a valid **exported unmangled** `C++` function/symbol in a **shared** or **static** library (`.dll`/`.lib`). This combination of `C#` binding stub and `C++` binding function is referred to as a **"binding pair"**.

!!! Example "Example binding pair"
    The `C#` binding stub:

    ``` C#
    [LibraryImport(LibIntricateEngine, EntryPoint = "RenderCommand_GetAPI")]
    [UnmanagedCallConv(CallConvs = [typeof(CallConvCdecl)])]
    internal static partial GraphicsAPI RenderCommand_GetAPI();
    ```

    The matching `C++` binding function:

    ``` C++
    _IE_BINDING_QUALIFIER GraphicsAPI RenderCommand_GetAPI()
    {
        return RenderCommand::GetAPI();
    }
    ```

    > **Note**: `#!C++ _IE_BINDING_QUALIFIER` is a macro which expands to: `#!C++ extern "C" __declspec(dllexport)`.

With this binding pair present and correctly written; all `C#` code that calls `RenderCommand_GetAPI()` now ultimately calls the `C++` `RenderCommand::GetAPI()` function.

### Why the underscore naming convention?

In `C++`, declaring a function as `#!C++ extern "C"` disables all **name-mangling** that would otherwise be performed on this function by the compiler and linker.

!!! Example "Mangled vs unmangled symbols"
    The mangled symbol declared **without** `#!C++ extern "C"`:  
    `?RenderCommand_GetAPI@Bindings@IntricateEngine@@YA?AW4GraphicsAPI@@XZ`

    The unmangled symbol declared **as** `#!C++ extern "C"`:  
    `RenderCommand_GetAPI`

As we can see from the above example, the **unmangled** symbol is much easier to work with, especially since this is the name that must be set for the `EntryPoint` field in `C#`'s `LibraryImportAttribute`:

``` C#
[LibraryImport(LibIntricateEngine, EntryPoint = "RenderCommand_GetAPI")]
```

Using **unmangled** symbols do however present us with a problem: all exported symbols must now be **unique**. This means no two functions can have the same name - including overloaded functions. This is the reason why we write **binding function names** in the format: `TypeName_FunctionName` - this ensures the uniqueness of the symbol.

### But how do we handle overloads?

Since all **exported symbols** must be unique, including overloads; we add **underscore suffixes** of the **type names** of the overloaded **parameters** to the binding name.

!!! Example
    Suppose we have `2` overloaded functions in the `SceneCamera` class:

    ``` C++
    void SetViewportSize(uint32 width, uint32 height);
    void SetViewportSize(Vector2Int bounds);
    ```

    As binding function declarations (in `C++`), these would be written as:

    ``` C++
    // NOTE: For primitives, the C# type name is preferred, hence 'uint' instead of 'uint32'
    _IE_BINDING_QUALIFIER void SceneCamera_SetViewportSize_uint_uint(uint32 width, uint32 height);
    _IE_BINDING_QUALIFIER void SceneCamera_SetViewportSize_Vector2Int(Vector2Int bounds);
    ```

---

## ABI Requirements & Calling Conventions

!!! Note
    For the rest of this section, `C++` code will be referred to as **Native code**, and `C#` code will be referred to as **Managed code**.

For two languages to interoperate, they must agree on the same **Application Binary Interface (ABI)**. The ABI defines the low-level **contract** that both sides must follow, including the **calling convention** used for function calls.

This agreement covers, among other things:

- Data layout and alignment in memory
- Which registers are used for parameters and return values
- Stack usage and stack-frame layout

And as such, all interop binding functions we write must also adhere to ABI requirements - otherwise everything turns into **undefined behaviour**.

!!! note
    In Intricate, on the `x86_64` platform, the **Microsoft x64 ABI** is used.

### Plain Old Data types (PODs)

A type is considered a **POD** if:

- It is a primitive type (`int`, `float`, etc...)
- It is a struct that contains only other PODs
- It is trivially-copyable
- It defines no constructors (in `C++`)

!!! tip
    Even if a `C++` struct contains only POD types and is **trivially-copyable**, the compiler will stop treating it as a POD the moment it sees any explicitly defined constructors. In other words, PODs may **not** adhere to any form of **RAII**.

### Why PODs matter

PODs are very important from an ABI perspective as they don't require any explicit **marshalling**. This means that PODs may be directly passed as **function parameters** and **function return-values** in binding functions.

!!! note
    Non-PODs may be passed as **function parameters** so long as the native and matching managed types have the **exact same memory layout**.

In the **IntricateEngine** codebase, types like `Vector2` may be freely passed around in **binding function parameters** as it is a **trivially copyable** type since it only contains `float` fields - provided that the matching `C#` `Vector2` type is of the same nature with the same **sequential memory layout**.

!!! danger
    `Vector2` **cannot** be directly passed as a **function return-value**. Since `Vector2` contains explicitly-defined **constructors**, the compiler doesn't treat it as a POD - it is treated as a **non-POD type**. And when non-POD types are returned: according to the ABI, since they can't fit inside the return register, a **pointer-to** the return data is passed in the return register rather than the return data itself. This then leads `C#` to interpret the **pointer** to the data as the **data itself** which is very dangerous and highly incorrect.

### How to return non-PODs

Non-PODs must be returned as **out pointers**.

!!! example
    Suppose we're writing a **binding pair** named `GetVector`. The `C#` binding would be written as:

    ``` C#
    [LibraryImport(LibIntricateEngine, EntryPoint = "GetVector")]
    [UnmanagedCallConv(CallConvs = [typeof(CallConvCdecl)])]
    internal static partial void GetVector(out Vector2 vector);
    ```

    And the `C++` binding would be written as:

    ``` C++
    _IE_BINDING_QUALIFIER void GetVector(Vector2* outVector)
    {
        // This dereferences a pointer to managed memory and assigns it a value
        *outVector = GetVectorFromSomewhere();
    }
    ```

---

## The Bindings Generator

The **Bindings Generator** is a code generator that automatically generates `C++ -> C#` **interop binding pairs** during build-time. It is written in `C#` and is integrated into **Premake** such that it runs before `IntricateEngine` & `IntricateEngine.NET` are compiled during builds. This ensures that the **interop bindings** are always up-to-date.

The Bindings Generator uses a series of **Interface Definition Language (IDL)** files written in `jsonc` as input. The IDL schema used is as follows:

``` json
{
    "Metadata": {
        "Type": "TypeName",
        "Headers": [
            "IntricateEngine/Header1.hpp",
            "IntricateEngine/Header2.hpp"
        ],
        "Source": "IntricateEngine/SourceFile.cpp"
    },
    "Functions": {
        "TypeName_FuncName": {
            "FuncSigType": "FetchExecute",
            "Params": "(void* param, NativeID objID)",
            "ParamsT": [
                {
                    "Type": "void*",
                    "Name": "param"
                },
                {
                    "Type": "NativeID",
                    "NativeType": "NativeObjectType", // OPTIONAL: NativeType only needs to be defined if Type = "NativeID"
                    "Name": "objID"
                }
            ],
            "Return": "void"
        },
        // Rest of the binding functions...
    }
}
```

### Function signature types

The Bindings Generator emits a fixed set of native and managed function shapes depending on the ownership model, return type, and call target. The generator has a list of **function signatures** that are used to define the `FuncSigType` field seen in the `jsonc` schema earlier. Each **function signature** determines the shape of the generated binding pair.

!!! warning
    It is of **critical importance** that the `FuncSigType` used for a particular binding pair is correct, otherwise compile-time errors and or crashes and undefined behaviour may occur.

!!! note
    `...` represents a placeholder for zero or more ABI-safe parameters.  
    It does not indicate C-style variadic arguments.

The following signatures document the canonical patterns generated by the system.

#### NativeObjectCreate
  
Used for `Create` functions when a new `NativeObject` needs to be created

``` C++
_IE_BINDING_QUALIFIER uint32 TypeName_Create(...)
{
    return Helpers::Create<_Ty>(...);
}
```

#### FetchExecute

Executes an instance method if the native object is valid.

``` C++
_IE_BINDING_QUALIFIER void TypeName_Foo(NativeID nativeID, ...)
{
    Helpers::FetchExecuteIfValid<TypeName>(nativeID, [&](const Ref<TypeName>& x)
    {
        x->Foo(...);
    });
}
```

#### FetchReturn

Executes an instance method with an ABI-safe return if the object is valid.

``` C++
_IE_BINDING_QUALIFIER ReturnType TypeName_GetFunc(NativeID nativeID, ...)
{
    return Helpers::FetchExecuteIfValid<ReturnType, TypeName>(nativeID, [&](const Ref<TypeName>& x)
    {
        return x->GetFunc(...);
    });
}
```

#### FetchReturnOut

Executes an instance method with an out-pointer return if the object is valid.

``` C++
_IE_BINDING_QUALIFIER void TypeName_GetFunc(NativeID nativeID, ..., ReturnType* outVal)
{
    *outVal = Helpers::FetchExecuteIfValid<ReturnType, TypeName>(nativeID, [&](const Ref<TypeName>& x)
    {
        return x->GetFunc(...);
    });
}
```

#### FetchReturnOutField

Returns a pointer to a native object's field as an out-pointer return if the object is valid.

``` C++
_IE_BINDING_QUALIFIER void TypeName_GetFieldNamePtr(NativeID nativeID, ReturnType** outVal)
{
    *outVal = Helpers::FetchExecuteIfValid<ReturnType*, TypeName>(nativeID, [&](const Ref<TypeName>& x)
    {
        return &x->FieldName;
    });
}
```

#### FetchReturnNativeObject

Executes an instance method returning the ID to a NativeObject if this object is valid.

``` C++
_IE_BINDING_QUALIFIER uint32 TypeName_GetFunc(NativeID nativeID, ...)
{
    return Helpers::FetchExecuteIfValid<uint32, TypeName>(nativeID, [&](const Ref<TypeName>& x)
    {
        return (uint32)x->GetFunc(...)->GetNativeID();
    });
}
```

#### FetchReturnString

Executes an instance method returning a string as an ABI-safe `void*` if the object is valid.

``` C++
_IE_BINDING_QUALIFIER void* TypeName_GetString(NativeID nativeID, ...)
{
    return Helpers::FetchExecuteIfValid<void*, TypeName>(nativeID, [&](const Ref<TypeName>& x)
    {
        return (void*)x->GetString(...).data();
    });
}
```

!!! warning
    The `void*` returned here is not stable, so managed code must copy the contents of the string into managed memory as soon as possible when using this.

#### FetchReturnPinned

Executes an instance method returning a complex data type that must be "pinned" in native heap memory to extend it's lifetime long enough for managed code to copy it.

``` C++
_IE_BINDING_QUALIFIER Memory::PinnedBlock TypeName_GetFunc(NativeID nativeID, ...)
{
    return Memory::Pin<ReturnType>(Helpers::FetchExecuteIfValid<ReturnType, TypeName>(nativeID, [&](const Ref<TypeName>& x)
    {
        return x->GetFunc(...);
    }));
}
```

#### StaticExecute

Executes a static method.

``` C++
_IE_BINDING_QUALIFIER void TypeName_Foo(...)
{
    TypeName::Foo(...);
}
```

#### StaticReturn

Executes a static method with an ABI-safe return.

``` C++
_IE_BINDING_QUALIFIER ReturnType TypeName_Foo(...)
{
    return TypeName::Foo(...);
}
```

#### StaticReturnOut

Executes a static method with an out-pointer return.

``` C++
_IE_BINDING_QUALIFIER ReturnType TypeName_Foo(..., ReturnType* outVal)
{
    *outVal = TypeName::Foo(...);
}
```

#### StaticReturnPinned

Executes a static method returning a complex data type that must be "pinned" in native heap memory to extend it's lifetime long enough for managed code to copy it.

``` C++
_IE_BINDING_QUALIFIER Memory::PinnedBlock TypeName_Foo(...)
{
    return Memory::Pin<ReturnType>(TypeName::Foo(...));
}
```

#### SingletonExecute

Executes a static method on a singleton.

``` C++
_IE_BINDING_QUALIFIER void TypeName_Foo(...)
{
    TypeName::Get().Foo(...);
}
```

#### SingletonReturn

Executes a static method on a singleton with an ABI-safe return.

``` C++
_IE_BINDING_QUALIFIER ReturnType TypeName_Foo(...)
{
    return TypeName::Get().Foo(...);
}
```

#### SingletonReturnPinned

Executes a static method on a singleton returning a complex data type that must be "pinned" in native heap memory to extend it's lifetime long enough for managed code to copy it.

``` C++
_IE_BINDING_QUALIFIER Memory::PinnedBlock TypeName_Foo(...)
{
    return Memory::Pin(TypeName::Get().Foo(...));
}
```

#### PointerCastExecute

Executes an instance method on a raw `this` pointer passed from managed code.

``` C++
_IE_BINDING_QUALIFIER void TypeName_Foo(void* ptr, ...)
{
    _IE_CORE_ASSERT(ptr, "ptr from managed was null!");
    (static_cast<TypeName*>(ptr))->Foo(...);
}
```

#### PointerCastReturn

Executes an instance method with an ABI-safe return on a raw `this` pointer passed from managed code.

``` C++
_IE_BINDING_QUALIFIER ReturnType TypeName_Foo(void* ptr, ...)
{
    _IE_CORE_ASSERT(ptr, "ptr from managed was null!");
    return (static_cast<TypeName*>(ptr))->Foo(...);
}
```

#### EcsGetNativeObject

Returns the ID to a NativeObject field of a component part of the **entity-component-system**.

``` C++
_IE_BINDING_QUALIFIER uint32 ComponentName_GetFieldName(NativeID sceneID, uint32 entityID)
{
    return Helpers::GetComponentNativeObjectField<ComponentName, TypeName, &ComponentName::FieldName>(sceneID, entityID);
}
```

!!! note
    The `FieldName` must be the same as the `TypeName` here.

#### EcsGetField

Returns an ABI-safe field of a component part of the **entity-component-system**.

``` C++
_IE_BINDING_QUALIFIER ReturnType ComponentName_GetFieldName(NativeID sceneID, uint32 entityID)
{
    return Helpers::GetComponentField<ComponentName, ReturnType, &ComponentName::FieldName>(sceneID, entityID);
}
```

#### EcsGetOutField

Returns a field of a component part of the **entity-component-system** as an out-pointer.

``` C++
_IE_BINDING_QUALIFIER void ComponentName_GetFieldName(NativeID sceneID, uint32 entityID, ReturnType* outVal)
{
    Helpers::GetComponentField<ComponentName, ReturnType, &ComponentName::FieldName>(sceneID, entityID, outVal);
}
```

#### EcsGetStringField

Returns a string field of a component part of the **entity-component-system** as an out-void-pointer.

``` C++
_IE_BINDING_QUALIFIER void ComponentName_GetFieldName(NativeID sceneID, uint32 entityID, void** outStrPtr)
{
    Helpers::GetComponentField<ComponentName, std::string, &ComponentName::FieldName>(sceneID, entityID, outStrPtr);
}
```

#### EcsSetField

Sets an ABI-safe field of a component part of the **entity-component-system**.

``` C++
_IE_BINDING_QUALIFIER void ComponentName_SetFieldName(NativeID sceneID, uint32 entityID, TypeName val)
{
    Helpers::SetComponentField<ComponentName, TypeName, &ComponentName::FieldName>(sceneID, entityID, val);
}
```

#### EcsSetStringField

Sets a string field of a component part of the **entity-component-system**.

``` C++
_IE_BINDING_QUALIFIER void ComponentName_SetFieldName(NativeID sceneID, uint32 entityID, ManagedUTF8String val)
{
    Helpers::SetComponentField<ComponentName, std::string, &ComponentName::FieldName>(sceneID, entityID, val);
}
```

#### MacroExecute

Executes functionality defined in a `C++` macro.

``` C++
_IE_BINDING_QUALIFIER void TypeName_Foo(...)
{
    _IE_FOO(...);
}
```

---
