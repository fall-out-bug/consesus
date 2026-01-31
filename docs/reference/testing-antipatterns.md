# Testing Anti-Patterns — Common Mistakes to Avoid

**Purpose:** Prevent common testing mistakes that lead to false confidence and maintenance burden.

**Core Principle:** Tests verify behavior, not implementation. Tests must be reliable and meaningful.

---

## Anti-Pattern 1: Mocking What You're Testing

**Problem:** Testing the mock, not the real code.

### ❌ Bad Example
```python
with patch('module.calculate_total') as mock:
    mock.return_value = 100
    result = calculate_total([1, 2, 3])  # Tests mock!
```

### ✅ Good Example
```python
def test_calculate_total():
    result = calculate_total([1, 2, 3])
    assert result == 6  # Real function
```

---

## Anti-Pattern 2: Test-Only Code Paths

**Problem:** Code that only exists for tests.

### ❌ Bad Example
```python
def process_data(data, test_mode=False):
    if test_mode: return {"test": "data"}
```

### ✅ Good Example
```python
def process_data(data):
    if not data: return {}  # Real edge case
    return process_real_data(data)
```

---

## Anti-Pattern 3: Incomplete Mocks

**Problem:** Mocks don't match real behavior.

### ❌ Bad Example
```python
mock_api.get.return_value = {"name": "John"}  # Missing fields!
```

### ✅ Good Example
```python
mock_api.get.return_value = {"name": "John", "email": "...", "id": 123}
```

---

## Anti-Pattern 4: Testing Implementation Details

**Problem:** Tests break on refactor.

### ❌ Bad Example
```python
assert calculator._cache == {6: True}  # Private state
```

### ✅ Good Example
```python
assert calculator.calculate([1, 2, 3]) == 6  # Public behavior
```

---

## Anti-Pattern 5: Flaky Tests with Timeouts

**Problem:** Tests depend on timing, fail randomly.

### ❌ Bad Example
```python
elapsed = time.time() - start
assert elapsed < 0.1  # Flaky!
```

### ✅ Good Example
```python
with patch('time.time', return_value=1000):
    result = scheduled_task()
    assert result == expected
```

---

## Anti-Pattern 6: Testing Multiple Things

**Problem:** When test fails, unclear what broke.

### ❌ Bad Example
```python
def test_user_operations():
    user = create_user("John")
    assert user.name == "John"
    user.update_email("john@example.com")
    assert user.email == "john@example.com"
```

### ✅ Good Example
```python
def test_create_user():
    assert create_user("John").name == "John"

def test_update_email():
    user = create_user("John")
    user.update_email("john@example.com")
    assert user.email == "john@example.com"
```

---

## Anti-Pattern 7: Tests Without Assertions

**Problem:** Tests that don't verify anything.

### ❌ Bad Example
```python
def test_process_data():
    result = process_data([1, 2, 3])  # No assert!
```

### ✅ Good Example
```python
def test_process_data():
    result = process_data([1, 2, 3])
    assert result == {"sum": 6, "count": 3}
```

---

## Detection Rules Summary

```python
ANTIPATTERN_MOCK_UNDER_TEST = "T001"  # Mocking code under test
ANTIPATTERN_TEST_ONLY_PARAM = "T002"  # test_mode parameters
ANTIPATTERN_INCOMPLETE_MOCK = "T003"  # Mock with < 3 fields
ANTIPATTERN_IMPL_DETAILS = "T004"     # obj._attribute in tests
ANTIPATTERN_TIME_BASED = "T005"       # time.sleep/time.time asserts
ANTIPATTERN_NO_ASSERT = "T006"        # Tests without assertions
```

---

## Quick Reference Checklist

- [ ] Not mocking code under test
- [ ] No test-only code paths
- [ ] Mocks match real behavior
- [ ] Testing behavior, not implementation
- [ ] No time-based assertions
- [ ] One behavior per test
- [ ] Every test has assertions

---

**Version:** 2.0.0  
**Related:** `/test`, `/build`, `@review`
