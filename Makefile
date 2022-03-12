dev:
	@pipenv install --dev --pre
	@pipenv run pre-commit install

release: clear-builds build distribute

clear-builds:
	@rm -rf dist

build: clear-builds
	@pipenv run python -m build

distribute:
	@pipenv run python -m twine upload dist/*

distribute-test:
	@pipenv run python -m twine upload --repository testpypi dist/*
