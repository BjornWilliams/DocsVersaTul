Scenario Guides
===============

These guides show how multiple VersaTul packages work together to solve a concrete development task.

Use them when you already know the job you need to get done and want a practical, end-to-end path instead of isolated API reference pages.

What These Guides Focus On
--------------------------

1. The smallest package combination that solves a realistic workflow.
2. The order to install and wire the packages.
3. The expected result of the workflow.
4. The next package or page to read once the scenario works.

Recommended Order
-----------------

1. Start with :doc:`file-import` if your first need is moving flat-file data into a database workflow.
2. Start with :doc:`data-export` if your first need is generating CSV, JSON, or other file-based exports.
3. Start with :doc:`logging-setup` if your first need is operational visibility in a service or background process.
4. Start with :doc:`sql-data-access` if your first need is a reusable data-service layer over relational storage.

What To Read Next
-----------------

1. Read :doc:`/recommended-paths` if you want an opinionated starting set by application type before choosing a workflow.
2. Read :doc:`/package-selection` if you still need to narrow the package family before choosing a guide.
3. Return to :doc:`/index` if you want the highest-level evaluation path again.

.. toctree::
   :maxdepth: 1

   file-import
   data-export
   logging-setup
   sql-data-access