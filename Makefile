src = chatapi.py
test = test_chatapi.py
.PHONY: check
check: $(src)
	ruff format --check $(src) $(test)
	ruff check $(src) $(test)
	mypy --strict $(src)
	pytest --quiet $(test)
