# Dart Fundamentals & Core Syntax Reference 🎯

> **Status:** Approved Reference (Synchronized with `notes/LEARNING_FLUTTER_NOTES.pdf`)  
> **Module:** Week 01 — Part 1

---

## 1. Program Structure & Entry Point

```dart
void main(List<String> args) {
  // Application entry point. args holds optional command-line arguments.
  print('Dart application initialized.');
}
```

---

## 2. Variables & Mutability

| Keyword | Type Inferred? | Reassignable? | Evaluation Time | Production Memory & Usage Rule |
|:---:|:---:|:---:|:---:|:---|
| **`var`** | Yes (static) | Yes (same type) | Runtime | Inferred local variables. Once set, type is locked. |
| **`dynamic`** | No | Yes (any type) | Runtime | **Bypasses compiler type checking.** Avoid in production except raw untyped JSON payloads. |
| **`final`** | Optional | No (single assign) | Runtime | Immutable reference initialized at runtime (e.g., API responses, `DateTime.now()`). |
| **`const`** | Optional | No (compile-time) | Compile-time | **Canonicalized in memory.** Identical instances reuse identical memory addresses. Essential for Flutter widgets. |

---

## 3. Data Types, Parsing & Type Casting

```dart
// 1. Safe Number Parsing
final int? count = int.tryParse(rawInput); // Returns null on invalid input instead of throwing
final double price = double.tryParse(priceStr) ?? 0.0; // Safe fallback idiom
final String formattedPrice = price.toStringAsFixed(2); // '19.99' (essential for currency)

// 2. Type Checking (is) vs Unsafe Casting (as)
final Object response = fetchApiResponse();

if (response is Map<String, dynamic>) {
  // Dart auto-promotes 'response' to Map inside this scope
  final String title = response['title'] as String? ?? 'Untitled';
}

// final int bad = response as int; // DANGER: Throws TypeError if response is not an int
```

---

## 4. Strings & Interpolation

```dart
final String user = 'Alice';
final String greeting = 'Hello, $user! Item count: ${user.length}'; // ${} required for expressions

// Multiline String: Preserves formatting and line breaks (ideal for SQL/GraphQL)
final String query = '''
  SELECT id, email, created_at 
  FROM users 
  WHERE is_active = true;
''';

// Raw String: Disables escape interpretation (prefixed with 'r')
final RegExp emailPattern = RegExp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
```

---

## 5. Operators Cheat Sheet

- **Null-Coalescing (`??`):** `final name = inputName ?? 'Guest';`
- **Null-Aware Assignment (`??=`):** `cachedToken ??= await fetchNewToken();`
- **Conditional Member Access (`?.`):** `final int? len = user?.profile?.bio?.length;`
- **Cascade Operator (`..` / `?..`):**
  ```dart
  final paint = Paint()
    ..color = Colors.blue
    ..strokeWidth = 2.0;
  ```

---

## 6. Modern Control Flow: Dart 3 Pattern Matching

```dart
String mapHttpStatus(int statusCode) => switch (statusCode) {
  200 || 201 => 'Success: Request Processed',
  400 => 'Bad Request: Verify Input',
  401 || 403 => 'Unauthorized: Invalid Credentials',
  >= 500 && <= 599 => 'Server Error: Try Again Later',
  _ => 'Unknown Error State', // Exhaustive default fallback
};
```

---

## 7. Production Pitfalls & Anti-Patterns

| Faulty / Fragile Pattern | Production Recommended Pattern | Impact in Production |
|:---|:---|:---|
| `int.parse(untrustedInput)` | `int.tryParse(input) ?? 0` | Avoids unhandled `FormatException` runtime crashes. |
| `list.forEach((e) async { ... })` | `for (final e in list) { await ... }` | `forEach` ignores `await`; `for-in` guarantees sequential execution. |
| `/** C-Style doc comment */` | `/// Markdown doc comment` | Effective Dart standard; powers VS Code / IDE tooltips. |
| `var widget = Container(...)` | `const widget = Container(...)` | `const` widgets eliminate redundant widget rebuild churn. |
