# SOP: Senior Engineering Implementation
**Objective:** Produce clean, self-documenting, and error-resilient code.

1. **Code Hygiene:**
   - **Type Hinting:** 100% coverage. Every Python function must have `def func(var: type) -> return_type:`.
   - **Docstrings:** Use Google-style docstrings for every class and method.
   - **Naming:** `snake_case` for Python, `camelCase` for React/JS.

2. **Error Handling (The 3-Layer Rule):**
   - Layer 1 (Input): Validate all incoming data using Pydantic or Joi.
   - Layer 2 (Logic): Wrap all external calls (DB, API) in Try-Except-Finally blocks.
   - Layer 3 (Global): Implement a global Exception Handler to prevent the app from crashing.

3. **Environment Security:**
   - NEVER hardcode strings like `localhost` or `3000`. Use `os.getenv("VARIABLE_NAME", "default")`.
   - All sensitive keys must be read from the provided `.env` file.

4. **Self-Healing Integration:**
   - Every module must include a `__health_check__` function that verifies its own dependencies (e.g., check if the DB connection is alive).