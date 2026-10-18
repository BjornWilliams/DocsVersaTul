API Contract Policy
===================

Nullable Reference Metadata
---------------------------

The audit releases enable C# nullable reference metadata in the library projects.
CLR signatures remain available, but callers compiling with nullable warnings
enabled should review diagnostics when upgrading. Optional inputs and valid
lookup absence are described by nullable annotations and the individual API's
XML documentation. A nullable annotation does not change runtime validation.

Each package's source compatibility impact is reviewed independently. Activating
metadata on a formerly oblivious public API is treated conservatively as a Major
migration. This does not assign one shared version number to all packages.

Keep caller-side null checks where an API can return an absent value. Do not
silence warnings globally when migrating. Refer to the package-specific
documentation for defaults, required settings and missing-key behavior.

Arguments And Unsupported Operations
----------------------------------------

Required dependencies and inputs reject null with ``ArgumentNullException``.
Non-null invalid values, including required strings that are empty or whitespace,
use ``ArgumentException`` or its range-specific subclass. APIs that normalize
optional null input retain their documented defaults; for example, the text case
helpers still return an empty string for null input, and cache options may select
defaults with null.

Unsupported operations use ``NotSupportedException``. In particular, the MongoDB
micron serializer rejects unsupported BSON representations with this exception
rather than ``NotImplementedException``. A missing destination table reported by
SQL bulk schema lookup uses ``InvalidOperationException`` and retains the SQL
exception as its cause.

When upgrading, review handlers that caught ``ArgumentNullException`` for empty
strings or a generic exception for unsupported operations. Check exception type
and ``ParamName`` for argument failures; do not match localized framework message
text. Required dependency guards run during construction or before operation
enumeration, rather than allowing a delayed null-reference failure.
