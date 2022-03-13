VERSION			:= $(shell git describe --always --dirty)


install:
	poetry install

package:
	poetry version ${VERSION}
	poetry build

publish:
	poetry publish
