setup:
	python3 -m venv ~/.fx_rl_repo

install:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	pip install --upgrade -q pip && pip install -r requirements.txt -q --progress-bar off; \
	)

test:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	python -m pytest -vv --cov=app tests/*.py; \
	python -m pytest --nbval Demo_Notebook.ipynb; \
	)

lint:
	(\
	export PATH=$PATH:/home/circleci/.local/lib/python3.8/bin/; \
	pylint --disable=R,C app; \
	)

all: setup install lint test
