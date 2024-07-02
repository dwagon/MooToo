test:
	pytest -n auto --no-cov-on-fail --cov=MooToo --cov-report term-missing

coverage: test
