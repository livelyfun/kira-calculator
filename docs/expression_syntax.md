# Kira Calculator: Expression Syntax & Reference

## 1. Supported Operators & Precedence

| Precedence | Operator / Syntax | Description | Associativity | Example |
| :--- | :--- | :--- | :--- | :--- |
| **1 (Highest)** | `( )` | Parentheses / grouping | Non-associative | `(2 + 3) * 4 = 20` |
| **2** | `f(x)` | Function call | Right-to-left | `sin(30) = 0.5` |
| **3** | `!` | Factorial (postfix) | Left-to-right | `5! = 120` |
| **3** | `%` | Percentage (postfix) | Left-to-right | `50% = 0.5` |
| **4** | `^` | Exponentiation | **Right-to-left** | `2 ^ 3 ^ 2 = 512` |
| **5** | `+`, `-` | Unary prefix sign | Right-to-left | `-2^2 = -4`, `2^-2 = 0.25` |
| **6** | `*`, `×`, `/`, `÷`, `%` | Multiplication, Division, Modulo | Left-to-right | `20 / 4 = 5`, `10 % 3 = 1` |
| **6** | `2(3)`, `2pi`, `2sin(x)` | Implicit multiplication | Left-to-right | `2(3 + 4) = 14`, `2pi ≈ 6.283` |
| **7 (Lowest)** | `+`, `-` | Addition, Subtraction | Left-to-right | `10 - 4 + 2 = 8` |

---

## 2. Built-in Mathematical Functions

| Function | Name | Description | Constraints |
| :--- | :--- | :--- | :--- |
| `sin(x)` | Sine | Trigonometric sine | Normalized by angle mode (DEG/RAD/GRAD) |
| `cos(x)` | Cosine | Trigonometric cosine | Normalized by angle mode |
| `tan(x)` | Tangent | Trigonometric tangent | Undefined at $90^\circ + 180^\circ k$ |
| `asin(x)` | Arc sine | Inverse trigonometric sine | $-1 \le x \le 1$ |
| `acos(x)` | Arc cosine | Inverse trigonometric cosine | $-1 \le x \le 1$ |
| `atan(x)` | Arc tangent | Inverse trigonometric tangent | Continuous on $\mathbb{R}$ |
| `sinh(x)` | Hyperbolic sine | Hyperbolic sine | Continuous on $\mathbb{R}$ |
| `cosh(x)` | Hyperbolic cosine | Hyperbolic cosine | Continuous on $\mathbb{R}$ |
| `tanh(x)` | Hyperbolic tangent | Hyperbolic tangent | Continuous on $\mathbb{R}$ |
| `log(x)` | Common log | **Base 10 logarithm** | $x > 0$ |
| `log10(x)` | Common log | Base 10 logarithm | $x > 0$ |
| `ln(x)` | Natural log | Natural logarithm (base $e$) | $x > 0$ |
| `sqrt(x)` / `√x` | Square root | Principal square root | $x \ge 0$ |
| `cbrt(x)` | Cube root | Cube root | Valid for all real numbers |
| `exp(x)` | Exponential | Natural exponent $e^x$ | Overflows if $x > 709$ |
| `abs(x)` | Absolute value | Absolute magnitude $|x|$ | Continuous on $\mathbb{R}$ |
| `factorial(n)` / `n!` | Factorial | Product of integers $1 \dots n$ | $n \in \mathbb{N}_0$, $n \le 170$ |
| `ceil(x)` | Ceiling | Smallest integer $\ge x$ | Continuous on $\mathbb{R}$ |
| `floor(x)` | Floor | Largest integer $\le x$ | Continuous on $\mathbb{R}$ |

---

## 3. Mathematical Constants

| Symbol / Name | Value | Description |
| :--- | :--- | :--- |
| `pi` / `π` | $3.141592653589793$ | Ratio of a circle's circumference to its diameter |
| `e` | $2.718281828459045$ | Euler's number (base of natural logarithms) |
| `phi` / `φ` | $1.618033988749895$ | Golden ratio: $\frac{1 + \sqrt{5}}{2}$ |
| `tau` / `τ` | $6.283185307179586$ | Circle constant: $2\pi$ |

