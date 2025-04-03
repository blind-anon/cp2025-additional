
.install:
	pip install black isort
	touch .install

format: .install
	black .
	isort . --profile black

clean:
	- rm .install