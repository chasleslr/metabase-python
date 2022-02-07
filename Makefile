dev:
	@pipenv install --dev --pre
	@pipenv run pre-commit install

release: clear-builds build distribute

clear-builds:
	@rm -rf dist

build:
	@pipenv run python -m pip install --upgrade build
	@pipenv run python -m build

distribute:
	@pipenv run python -m pip install --upgrade twine
	@pipenv run python -m twine upload dist/*
