setup:
	python3 -m venv ~/.fx_rl_repo

install:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	pip install --upgrade -q pip && pip install -r requirements.txt -q --progress-bar off; \
	)

lint:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	export PATH=$$HOME/.local/bin:$$PATH;\
	pylint --disable=R,C app; \
	)

test:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	python -m pytest -vv --cov=app tests/*.py; \
	)

all: setup install lint test
