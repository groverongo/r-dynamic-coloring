environment.yml:
	conda env export | grep -v "^prefix: " > environment.yml

.PHONY: environment.yml