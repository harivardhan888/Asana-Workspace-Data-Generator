# Scrapers

This directory is intended for scripts that fetch real-world data to populate the simulation.

For this implementation, we have opted to use:
1.  **Static Lists** (e.g., standard Asana project templates, known tech stacks).
2.  **Faker Library** (for PII like names and emails).
3.  **Heuristics** (for distributions).

This approach ensures the simulation is:
-   **Deterministic**: Running with a seed produces the same result.
-   **Robust**: No network dependencies or API rate limits.
-   **Fast**: Generation happens instantly.

If "live" data is required in the future (e.g., scraping YC top companies), add the scripts here.
