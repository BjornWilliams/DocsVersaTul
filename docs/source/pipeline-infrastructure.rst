Pipeline Infrastructure
=======================

Overview
--------

``VersaTul.Pipeline.Infrastructure`` provides a lightweight implementation of the pipeline-and-step pattern for transforming values through composable processing units.

The package is intentionally small: a step interface, a pipeline base class, and extension methods that make chained step composition easy for both synchronous and asynchronous workflows.

When To Use This Package
------------------------

Use this package when you want to:

1. Break a multi-stage transformation into explicit reusable steps.
2. Chain sync or async processing with clear input and output types.
3. Add optional diagnostics around step execution time and failures.
4. Reuse the same pipeline pattern across formatters, validation, or normalization flows.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Pipeline.Infrastructure

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Pipeline.Infrastructure -Version latest

Related Packages
----------------

1. :doc:`display-attributes` because its formatting pipeline is built on these step abstractions.

Core Types And Concepts
-----------------------

``IStep<TIn, TOut>``
   Defines a single unit of work that transforms ``TIn`` into ``TOut``.

``Pipeline<TIn, TOut>``
   Base class for composing a pipeline through a ``Func<TIn, TOut>`` step chain.

``PipelineExtensions``
   Extension methods that chain steps fluently and add optional diagnostics.

Key Capabilities
----------------

1. Compose nested pipelines with strongly typed step boundaries.
2. Execute synchronous steps through ``AddStep()``.
3. Execute asynchronous steps through ``AddStep()`` overloads that return ``Task<TOut>``.
4. Capture elapsed time and exceptions through diagnostics callbacks.
5. Fail fast when a pipeline is executed before its step chain is configured.

Step Example
------------

.. code-block:: csharp

   using VersaTul.Pipeline.Infrastructure.Contracts;

   public class AddOneStep : IStep<int, int>
   {
       public int Execute(int input) => input + 1;
   }

   public class IntToStringStep : IStep<int, string>
   {
       public string Execute(int input) => input.ToString();
   }

Pipeline Example
----------------

.. code-block:: csharp

   using VersaTul.Pipeline.Infrastructure;
   using VersaTul.Pipeline.Infrastructure.Extensions;

   public class NumberPipeline : Pipeline<int, string>
   {
       public NumberPipeline()
       {
           Step = input => input
               .AddStep(new AddOneStep())
               .AddStep(new IntToStringStep());
       }
   }

Diagnostics Example
-------------------

.. code-block:: csharp

   var value = 5.AddStep(new AddOneStep(), (elapsed, error) =>
   {
       Console.WriteLine($"Elapsed: {elapsed}");
       if (error != null)
       {
           Console.WriteLine(error.Message);
       }
   });

Notes
-----

1. ``Pipeline<TIn, TOut>.Execute()`` throws if ``Step`` is not configured.
2. Async support is provided through ``PipelineExtensions`` overloads rather than a separate async pipeline base class.
3. This package is deliberately minimal, which makes it a good fit for custom domain pipelines without framework overhead.
