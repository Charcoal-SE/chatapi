src = chatapi/core.py chatapi/__init__.py
test = test/test_chatapi.py
.PHONY: check
check: $(src) $(test)
	ruff format --check $(src) $(test)
	ruff check $(src) $(test)
	mypy --strict $(src)
	pytest --quiet $(test)
