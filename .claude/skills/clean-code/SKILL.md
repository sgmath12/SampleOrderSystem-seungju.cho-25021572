---
name: clean-code
description: Refactors code to clean up clutter, enforce simplicity, fix technical debt, and ensure Karpathy style guardrails. Call this whenever the user wants to polish, refactor, or optimize existing code blocks or files.
---

# Clean Code and Refactoring Protocol

When this skill is invoked, you must systematically refactor the target code following the four core pillars of high-utility, robust software development.

## 1. Execution Steps

1. **Analyze Context**: Read the targeted file or code block. Identify redundant logic, dead code, and naming ambiguities.
2. **State Assumptions**: Before modifying anything, explicitly output a brief 2-sentence summary of *what* you intend to change and *why*.
3. **Surgical Refactoring**: Apply minimal, highly targeted changes. Do not refactor unrelated neighboring code.
4. **Verification**: Run local tests, compilers, or linters if available in the environment to verify nothing was broken.

## 2. Core Guardrails (Karpathy Rules)

* **Think First**: If the user's refactoring request is ambiguous, stop and ask for clarification. Never guess the architectural intent.
* **Simplicity First**: Write the absolute minimum code required. Reject speculative abstractions, over-engineering, or creating "flexible" structures for unrequested features.
* **Surgical Precision**: Touch only the lines required for the clean-up. No sprawling, multi-file refactors unless explicitly ordered.
* **Goal-Driven Logic**: Turn vague cleanup tasks into clear, verifiable targets (e.g., "Reduce cognitive complexity of function X under 10 lines").

## 3. Style and Readability Rules

* **Descriptive Naming**: Rename variables like `data` or `temp` to explicit, clear alternatives indicating their precise contents.
* **Pure Functions**: Extract deeply nested loops or complex logic blocks into small, single-purpose helper functions.
* **Fail Early**: Restructure nested `if` statements into guard clauses that return early.
* **Comment Removal**: Delete commented-out dead code blocks. Replace inline comments describing "what" the code does with clean, self-documenting code; only comment on "why" a complex edge case exists.

## 4. Output Format

* Present a unified **Before vs After** code comparison layout or use targeted diffs.
* Provide a brief bulleted list of the exact technical improvements made.
