# Reflection

**1. Which issues were easiest and which hardest to fix?**
Style items (naming, docstrings, unused imports, `== None`) were mechanical. The hardest were `eval` and `os.system`, because removing them meant changing how the code works: the discount function now takes a numeric rate instead of an expression string, so the caller changed too. Swapping MD5 for SHA-256 changed the item-hash output, which matters if anything stored the old hashes.

**2. Did the tools report false positives, or miss real problems?**
Nothing was clearly a false positive here. Some findings were low value in context: B311 on a checkout PIN is only a real problem because PINs are security values, and Pylint's `global-statement` is a design hint rather than a defect. The tools missed two real problems: the hardcoded live payment key printed to the console (Bandit's secret check did not match the variable name `payment_gateway_key`), and `"%d" % price` silently dropping cents from the audit log. Both were found only by reading the code and running it.

**3. How would you integrate static analysis into a real workflow?**
Run Flake8, Pylint and Bandit as a pre-commit hook for fast local feedback, and again in CI on every pull request with the build failing on Bandit High/Medium findings and on a Pylint score below a threshold. Pin tool versions and keep a config file so results are reproducible. Suppress a warning only with a comment explaining why.

**4. What improvements did you see in quality and security?**
Pylint went from 3.86 to 10.00, Bandit from 5 issues (2 High) to 0, Flake8 from 7 to 0. Beyond the numbers: command injection and arbitrary code execution paths are gone, the shared-list bug is fixed, errors are no longer silently swallowed, and the code is documented, consistently named and safe to import. Static analysis does not replace testing or code review, since it missed the two issues above, but it catches a large class of problems cheaply.
