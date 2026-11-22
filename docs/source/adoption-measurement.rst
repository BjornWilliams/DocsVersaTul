Adoption Measurement and Privacy
================================

This page explains which documentation adoption signals VersaTul reviews, how
they are defined, and what the current analytics can and cannot establish.

Measurement sources
-------------------

The site uses Read the Docs' first-party traffic and search analytics. Reports
use aggregate page-view, 404, and search-result counts. They do not add a
third-party analytics script, session replay, user identifier, or event
collector. See the Read the Docs `traffic analytics documentation
<https://docs.readthedocs.com/platform/stable/traffic-analytics.html>`_ and
`search analytics documentation
<https://docs.readthedocs.com/platform/stable/search-analytics.html>`_.

The current Read the Docs Community analytics window retains up to 90 days.
Monthly comparisons should record the date and selected window because views
can change as the rolling period advances.

Event definitions and availability
-----------------------------------

The following definitions are the adoption plan. The available counts are
descriptive proxies unless the source can observe the event itself.

.. list-table:: Adoption measures
   :header-rows: 1
   :widths: 20 35 25 20

   * - Measure
     - Operational definition
     - Available signal
     - Limitation
   * - Landing to quickstart
     - Report ``/index.html`` and ``/getting-started.html`` page views in the same window.
     - Aggregate page views.
     - The ratio of page views is not a visitor journey or conversion rate.
   * - Package page to NuGet
     - A click on a package page's primary NuGet link.
     - Campaign parameters identify the originating documentation page if the destination reports them.
     - Read the Docs does not expose outbound-click counts, and NuGet download totals do not attribute downloads to documentation referrals.
   * - Quickstart completion proxy
     - A visitor reaches the end of the quickstart and reports the sample output.
     - Quickstart page views can be reported as a reading proxy.
     - Page views do not establish that a visitor ran the local sample or completed the guide.
   * - Scenario navigation
     - Page views for the scenario index and each scenario page.
     - Aggregate page views by path.
     - Separate page counts do not establish that one visitor navigated between them.
   * - Search with no result
     - A search query for which the Read the Docs search index returns no results.
     - Read the Docs Search Analytics reports query terms and result counts when data is available.
     - No query data is available in the current dashboard snapshot; this is unknown, not a zero-failure baseline.
   * - Issue and support links
     - A click on a documentation issue or support link.
     - No click event is currently collected.
     - Page views on support pages do not measure outbound clicks.
   * - High-exit pages
     - A page with a high exit rate among sessions that entered it.
     - No session-level exit metric is currently collected.
     - Page-view totals cannot identify high-exit pages.

Privacy boundaries
------------------

* Do not add code, configuration, credentials, connection strings, or other
  application payloads to analytics events.
* Do not add a session replay, fingerprint, or user-level identifier for this
  report.
* Read the Docs Search Analytics can show search terms. Do not copy raw search
  strings into source control, work items, or monthly reports. Report only
  aggregate counts or a reviewed, non-sensitive topic category. Do not enter
  secrets or application configuration into the documentation search box.
* NuGet campaign values describe a documentation page, not a person. They do
  not contain a visitor ID or user-entered text. The destination may receive
  and log the URL query parameters.
* NuGet download totals are aggregate package statistics. They may include
  automated restores and are not proof of successful use.

Campaign link convention
------------------------

Primary package-acquisition links use these query parameters:

``utm_source=docsversatul``
   Identifies the documentation site.
``utm_medium=documentation``
   Identifies the link channel.
``utm_campaign=adoption``
   Identifies the adoption effort.
``utm_content=<page-slug>``
   Identifies the page containing the link.

These parameters do not themselves record a click or prove a download came
from the documentation. NuGet's public package statistics currently provide
downloads by package and version, not a documentation-referral breakdown.
Keep canonical package inventory URLs and exact-version reference links
unchanged.

Monthly review and experiments
------------------------------

For each monthly report, record the date, traffic window, top page views, 404
paths, search-query availability, and latest NuGet version downloads with
their separate reporting window. Convert a repeated, non-synthetic 404 into
a route or link review. When search data becomes available, review no-result
queries without copying sensitive raw terms. When session-level exit data is
available, rank pages by exit rate and create a content task for a specific
observed problem.

Do not run a controlled content experiment until the event source can measure
eligible exposures and outcomes, traffic supports the preselected minimum
effect, and the report can separate the variants without identifying
visitors. Choose the effect threshold before a test; do not use a small page
view count as evidence that one variant won.
