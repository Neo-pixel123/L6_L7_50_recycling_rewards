# Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues and the trivial Pylint warnings: the unused `math` import, the unused `airport_fee` variable, `== None` → `is None`, and the missing newline. Each one has a single obvious mechanical fix. Swapping MD5 for SHA-256 and `random` for `secrets` was just as easy.

The hardest was the `eval()` call, because removing it changes the function's interface. Callers now pass a numeric rate instead of an expression string, so `main()` had to change too. Removing the `global` statement and renaming every function to snake_case also took care, since every call site had to be updated without breaking the program. The cancellation bug was the hardest of all, because no tool reported it. I only found it by noticing that the output said 3 flights were available when BA202 should still have been full.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Bandit's B105 (hardcoded password) is a heuristic that fires on any string literal assigned to a variable whose name contains "secret", "token" or "password", so it can flag harmless values. In this file it was a true positive: a real token was hardcoded and then printed. Bandit's B311 on `random` is closer to a false positive in general, since `random` is fine for simulations or shuffling. It only matters here because the value is a boarding PIN, which is security-related. Some Pylint convention checks, such as requiring a docstring on every small helper, are stylistic preferences rather than defects.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- **Pre-commit hooks:** run Flake8 and Bandit through the `pre-commit` framework so style and security issues are caught before code is committed.
- **CI pipeline:** run all three tools in GitHub Actions on every push and pull request. The build fails on Bandit High/Medium findings, on Flake8 errors, or when the Pylint score drops below a threshold such as 9.5.
- **Editor integration:** enable Pylint and Flake8 in VS Code so problems appear while typing.
- **Shared configuration:** keep `.pylintrc`, `.flake8` and Bandit settings in the repo so every developer and CI run uses the same rules. Justified suppressions are documented inline with `# nosec` or `# pylint: disable=` plus a reason.

**4. What tangible improvements did you observe in code quality, readability, or potential robustness after applying the fixes?**

- **Security:** shell injection, arbitrary code execution through `eval`, the weak hash, the predictable PIN and the leaked API token are all gone. Bandit went from 6 issues (2 High) to 0.
- **Robustness:** the mutable default no longer leaks baggage tags between bookings, and the manifest file is always closed. Errors are no longer silently swallowed. A cancel on an unbooked flight now fails correctly instead of creating a seat out of nothing, and revenue is refunded on cancellation.
- **Readability:** PEP 8 names, docstrings, wrapped lines and a simplified availability check make the code easier to follow. Pylint went from 4.00/10 to 10.00/10, and Flake8 went from 10 issues to 0.
- I also learned that static analysis does not replace testing. The most visible logic bug in the output was invisible to all three tools.
