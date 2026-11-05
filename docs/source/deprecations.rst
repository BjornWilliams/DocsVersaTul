Deprecated APIs And Migrations
==============================

VersaTul packages are versioned independently, so a deprecation timeline is
tracked per package. A deprecated member remains available during its
compatibility period; consumers should migrate before the first major release
that removes it. No calendar removal dates are assigned for the APIs below.
Removal requires a documented replacement, a migration example, and a major
version review for the affected package.

Current deprecations
--------------------

.. list-table:: Deprecated public APIs
   :header-rows: 1

   * - Package
     - Deprecated API
     - Replacement
     - Removal timeline
   * - :doc:`caching`
     - ``ICacheProviderWithEvents<T>.ItemRemoved``
     - ``ICacheProviderWithEvents<T>.ItemRemovedDetailed``
     - No earlier than the next approved major release of ``VersaTul.Caching``; no release date is assigned.
   * - :doc:`scheduler`
     - ``IMethodCall.BeginExecute`` overloads
     - ``IAsyncMethodCall.ExecuteAsync(...)``
     - Retained through the current major line; removal is reserved for a later approved major release of ``VersaTul.Task.Scheduler``.

Cache removal events
--------------------

Use ``ItemRemovedDetailed`` to receive typed event data instead of the legacy
``ItemRemoved`` event:

.. code-block:: csharp
   :caption: Pseudocode: illustrative event subscription, not a standalone sample.

   cacheProvider.ItemRemovedDetailed += (_, args) =>
   {
       Console.WriteLine($"Removed {args.Key}: {args.Reason}");
   };

The event remains nullable-aware: a removal can have no key or reason, so
handle either value before using it.

Scheduler method calls
----------------------

Replace ``BeginExecute`` with the task-based interface and await completion:

.. code-block:: csharp
   :caption: Pseudocode: illustrative async migration, not a standalone sample.

   IAsyncMethodCall asyncCall = (IAsyncMethodCall)methodCall;
   object? result = await asyncCall.ExecuteAsync(cancellationToken);

Use the ``IParameterSetter`` overload when the call has bound parameters. Keep
the legacy overloads only while migrating; they are documented as removed in a
future major version.
