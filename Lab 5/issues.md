# Issue Documentation — flight_reservation_system.py

Line numbers refer to the original file. Before reports: Pylint 4.00/10, Bandit 6 issues (2 High, 1 Medium, 3 Low), Flake8 10 issues. After: Pylint 10.00/10, Bandit 0, Flake8 0.

| # | Issue | Type | Tool / Severity | Line(s) | Description | Fix Approach |
|---|-------|------|-----------------|---------|-------------|--------------|
| 1 | Shell command injection | Security | Bandit B605 — High | 63 | `os.system("echo ... " + filename)` passes a user-controllable filename to a shell, so a crafted filename could run arbitrary commands. | Replaced the shell call with a plain `print()`. |
| 2 | Weak hash (MD5) | Security | Bandit B324 — High | 52 | MD5 is broken and unsuitable for hashing identifiers such as passport numbers. | Switched to `hashlib.sha256`. |
| 3 | Use of `eval()` | Security | Bandit B307 — Medium | 47 | `eval(surcharge_expr)` executes any string passed in, which allows arbitrary code execution. | Function now takes a numeric `surcharge_rate`, and the fee is `base_fare * float(rate)`. |
| 4 | Hardcoded secret, printed to stdout | Security | Bandit B105 — Low | 75, 84 | The API token is a string literal in source and is printed in plain text. | Read from the `AIRLINE_API_SECRET` env variable. Only whether it is configured gets printed. |
| 5 | Insecure random for PIN | Security | Bandit B311 — Low | 56 | `random` is predictable and not suitable for security values such as boarding PINs. | Used `secrets.randbelow`. |
| 6 | Bare `except: pass` | Bug | Bandit B110 — Low, Flake8 E722, Pylint W0702 | 31–32 | Silently swallows every error, including unrelated ones such as `KeyboardInterrupt`. | Catch only the expected missing-flight case and return `False`. |
| 7 | Mutable default argument | Bug | Pylint W0102 | 15 | `baggage_tags=[]` is shared across calls, so tags leak between bookings. | Default to `None` and create a new list inside the function. |
| 8 | Global statement | Quality | Pylint W0603 | 16 | `global total_revenue` makes state hard to track and test. | Revenue is kept in a module-level `REVENUE` dict. |
| 9 | File opened without `with` / encoding | Bug | Pylint R1732, W1514 | 60–62 | The file is not closed if `write` raises, and the encoding depends on the platform. | `with open(filename, "w", encoding="utf-8")`. |
| 10 | Unused imports/variables | Style | Flake8 F401, F841; Pylint W0611, W0612 | 4, 36, 46, 68 | `math`, `airport_fee` and loop variable `f` are unused. | Removed them. |
| 11 | `== None` comparison | Style | Flake8 E711, Pylint C0121 | 37 | Identity check written as an equality check. | `is None`. |
| 12 | Non-snake_case names | Style | Pylint C0103 | 15–66 | camelCase function names violate PEP 8. | Renamed (e.g. `bookFlightSeat` → `book_flight_seat`). |
| 13 | Redefined outer name | Quality | Pylint W0621 | 66 | Parameter `flights` shadows the global. | Renamed to `flight_data`. |
| 14 | Line length / missing final newline | Style | Flake8 E501, W292 | 7–9, 23, 87 | Lines over 79 characters, and no newline at EOF. | Wrapped the lines and added a trailing newline. |
| 15 | Missing docstrings, simplifiable if, %-format | Style | Pylint C0114, C0116, R1703, R1705, C0209 | various | No module or function docs, redundant if/else, old-style formatting. | Added docstrings, `return not ...`, f-string. |
| 16 | Cancel adds seats beyond capacity | Logic bug | Not detected by any tool | 27–30 | `cancelBooking("BA202")` reopened a flight that had no bookings (0 → 1 seat), which is why the output showed "Available flights: 3". Revenue was also never refunded. | Added a `capacity` field. Cancel is rejected when no seats are booked, and the fare is refunded on a valid cancel. |
