setup:
	python3 -m venv ~/.fx_rl_repo


install:
	(\
	source ~/.fx_rl_repo/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt; \
	)

test:
	(\
	source ~/.fx_rl_repo/bin/activate; \
	python -m pytest -vv --cov=app tests/*.py; \
	python -m pytest --nbval Demo_Notebook.ipynb; \
	)

lint:
	(\
	pylint --disable=R,C app; \
	)

all: install lint test
