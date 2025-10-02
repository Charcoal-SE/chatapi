# Chat API

This is a Python wrapper library for [the new API for chat](https://meta.stackexchange.com/q/412907/).

## Getting started

Here's what to know:
* It should work with [the currently-supported Python releases](https://devguide.python.org/versions/#supported-versions).
* This library is under active development, meaning it's not necessarily stable and may change

## Developer information

Currently, this is the general approach:
* Type hints to provide clarity using [mypy](https://github.com/python/mypy)
* Code formatted + checked with [Ruff](https://github.com/astral-sh/ruff)
* Tested with [pytest](https://docs.pytest.org/en/stable/), incorporating some ChatExchange tests for compatibility verification
* And a `Makefile` to run Ruff, mypy, and pytest with `make check`
