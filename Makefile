setup:
	python3 -m venv ~/.fx_rl_repo

install:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	pip install --upgrade -q pip && pip install -r app/requirements.txt -q --progress-bar off; \
	)

lint:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	pylint --disable=R,C app; \
	)

test:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	pip install pytest; \
	python -m pytest tests/*.py; \
	)

all: setup install test
