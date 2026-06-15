# Agent Config Validator

A small Python project for practicing descriptors in an Agentic AI context.

## Goal

This project shows how descriptors can control and validate attributes in an AI agent configuration system.

## Concepts Practiced

- `__get__`
- `__set__`
- `__set_name__`
- Data descriptors
- Non-data descriptors
- `@property`
- Cached attributes
- Attribute validation
- Agent configuration design

## Why This Matters

In backend and agentic AI systems, configuration values must be controlled:

- temperature must stay within a safe range
- top_k must be positive
- retries must not be negative
- model names should come from allowed choices
- prompts should not be empty

This project builds a mini validation layer similar to the ideas behind framework-controlled fields in tools like Pydantic, ORMs, and backend frameworks.

## Run

```bash
python main.py
