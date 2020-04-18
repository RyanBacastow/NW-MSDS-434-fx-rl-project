setup:
	python3 -m venv ~/.fx_rl_repo

install:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt; \
	)

test:
	(\
	. ~/.fx_rl_repo/bin/activate; \
	python -m pytest -vv --cov=app tests/*.py; \
	python -m pytest --nbval Demo_Notebook.ipynb; \
	)

lint:
	pip3 show -f pylint
	pip3 install pylint
	pylint --disable=R,C app

all: setup install lint test
