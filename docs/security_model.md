# Kira Calculator: Security Model & Threat Assessment

## 1. Threat Model & Design Goals

Desktop calculators frequently accept untrusted strings from user keyboards, external scripts, and clipboard paste actions. In traditional implementations, evaluating expressions using Python's `eval()` or unconstrained interpreters exposes the host operating system to arbitrary code execution, file system tampering, network exfiltration, and local denial-of-service.

Kira Calculator adheres to a **Zero Arbitrary Execution** policy:

1. **No Code Evaluation:** Neither Python's `eval()`, `exec()`, `compile()`, nor third-party AST eval libraries like `asteval` are employed.
2. **Explicit Allowlisting:** Only tokens and operations explicitly enumerated in the lexer and parser grammar are capable of being parsed.
3. **Strict Visitor Isolation:** The evaluator uses a visitor pattern that only inspects 6 safe immutable AST node types (`NumberNode`, `ConstantNode`, `UnaryOpNode`, `BinaryOpNode`, `PostfixOpNode`, `FunctionCallNode`). Any unexpected node triggers a fatal `SecurityError`.
4. **Denial-of-Service Defense:** All resource dimensions (string length, AST depth, node count, exponent magnitude, factorial size) are strictly bounded.

---

## 2. In-Depth Defense Matrix

| Attack Vector | Vulnerability Scenario | Kira Calculator Defense | Tested Verification |
| :--- | :--- | :--- | :--- |
| **Arbitrary Code Execution** | `__import__('os').system('...')` | Tokenizer rejects identifiers not present in `KNOWN_FUNCTIONS` or `KNOWN_CONSTANTS`. | `test_reject_imports` |
| **Attribute Traversal** | `(1).__class__.__base__.__subclasses__()` | Dot operator `.` is only permitted within numeric literals. Any dot outside a number raises `InvalidNumberError`. | `test_reject_attribute_access` |
| **Object Instantiation / Call** | `open('/etc/passwd')`, `eval(...)` | Parser only permits function calls from an allowlisted set of mathematical routines. | `test_reject_arbitrary_function_calls` |
| **Stack Overflow / Memory DoS** | Deep nesting: `(((((...1...)))))` | Parser enforces `MAX_DEPTH = 100`. Exceeding this limit raises `SecurityError`. | `test_bound_nesting_depth` |
| **AST Explosion** | Unusually long expressions: `1+1+1...` | Tokenizer enforces `MAX_EXPRESSION_LENGTH = 2000`, and parser enforces `MAX_NODES = 1000`. | `test_bound_excessive_expression_length` |
| **CPU Lockup via Exponents** | Huge powers: `10 ^ 99999999` | Evaluator rejects exponents with $|exp| > 10000$ before calculating. | `test_bound_excessive_exponents` |
| **CPU Lockup via Factorials** | `1000000!` | Evaluator caps factorials at $n \le 170$ ($171! > 1.79 \times 10^{308}$). | `test_bound_excessive_factorials` |
| **Corrupted State Recovery** | Malformed history/settings JSON | JSON loaders catch decode errors and fallback to safe defaults without crashing. | `test_history_corrupt_file_recovery`, `test_settings_corrupt_file_recovery` |
| **Filesystem Race Conditions** | Partial write on sudden system shutdown | All persistent writes use temporary files, `flush()`, `os.fsync()`, and atomic `os.replace()`. | Verified in `HistoryService` and `SettingsService` |

