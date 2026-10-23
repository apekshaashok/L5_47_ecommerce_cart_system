# Issues found in `ecommerce_cart_system.py`

Before: Pylint 3.86/10, Bandit 5 issues (2 High, 1 Medium, 2 Low), Flake8 7 issues.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `os.system` with string concatenation (B605, High) | Security | 60 | `filename` is concatenated into a shell command, so a filename like `x; rm -rf ~` runs arbitrary commands (command injection). The shell was only used to `echo`. | Removed the shell call and used `print("Receipt saved to:", filename)`. |
| Weak MD5 hash (B324, High) | Security | 49 | MD5 is broken and flagged for security use. | Switched to `hashlib.sha256`. |
| `eval` on caller-supplied string (B307 / W0123, Medium) | Security | 44 | `calculateDiscountedTotal` evaluates `discount_expr` with `eval`, so any string passed in executes as Python code. | Replaced the expression string with a numeric `discount_rate` (0 to 1), validated, and compute `price * (1 - rate)`. |
| Hardcoded live payment secret, printed to stdout (not flagged by any tool) | Security | 72, 81 | A live-looking key is committed in source and printed on every run. Bandit missed it because the variable name `payment_gateway_key` does not match its secret-name patterns. | Read it from the `PAYMENT_GATEWAY_KEY` environment variable and print only whether it is configured. |
| `random` used for checkout PIN (B311, Low) | Security | 53 | `random` is predictable, not suitable for security values. | Used `secrets.randbelow` (`1000 + secrets.randbelow(9000)`). |
| Mutable default argument `audit_log=[]` (W0102) | Bug | 15 | The same list is shared across all calls, so state leaks between callers. | Default to `None`; fall back to a module-level `AUDIT_LOG` list. |
| Bare `except: pass` (B110, E722, W0702) | Bug | 26-29 | Swallows every exception, including `KeyboardInterrupt`, and hides failures. | Replaced with `cart_items.pop(item_id, None)`; function now returns whether the item existed. |
| Wrong log format: `%d` on a float price | Bug (not tool-flagged) | 21 | `"%d" % 35.5` prints `35`, silently dropping cents in the audit log. | Used an f-string with `{price:.2f}`. |
| `global total_sales` (W0603), never read and never reduced on removal | Design | 12, 16, 20 | Global mutable state that goes out of sync with the cart. | Removed it; added `calculate_cart_total()` that computes the total from `cart_items`. |
| File opened without `with` or encoding (R1732, W1514) | Quality | 57-59 | File not closed if `write` raises; platform-dependent encoding. | `with open(filename, "w", encoding="utf-8")`. |
| Comparison to `None` with `==` (E711, C0121) | Style | 34 | Should use identity. | `item is None`. |
| Unused import `math`, unused variables `handling_fee`, `base_price`, `k` (F401, F841, W0611, W0612) | Style | 4, 33, 43, 65 | Dead code. | Removed the import and the unused variables; `base_price` is now actually used. |
| Unnecessary `else` after `return`, simplifiable `if` (R1703, R1705) | Quality | 36-39 | Verbose boolean return. | `return item["qty"] > 0`. |
| Parameter `cart_items` shadows module-level name (W0621) | Quality | 63 | Easy to mix up the global and the argument. | Renamed parameter to `items`. |
| camelCase function names (C0103) | Style | 15, 25, 32, 42, 48, 52, 56, 63 | Violates PEP 8 snake_case. | Renamed all functions and updated every call. |
| Missing module and function docstrings (C0114, C0116) | Style | all | No documentation. | Added docstrings. |
| `main()` runs on import | Quality | 84 | Importing the module executes the demo. | Added `if __name__ == "__main__":` guard. |
| Line too long (E501), no final newline (W292, C0304) | Style | 76, 84 | PEP 8 formatting. | Wrapped the long line; added trailing newline. |
