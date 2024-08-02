all: test

server:
	fastapi dev MooToo/server/main.py &

test:
	PYTHONPATH=. pytest -n auto

coverage:
	PYTHONPATH=. pytest -n auto --no-cov-on-fail --cov=MooToo --cov-report term-missing

game: server
	python MooToo/ui/game.py
