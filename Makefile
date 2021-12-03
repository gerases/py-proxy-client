env_dir := env

$(env_dir): env-clean env-create env-update
	@echo -e "\n===> Done! Activate environment by executing 'source $(env_dir)/bin/activate'"

.PHONY: env-create
env-create:
	@echo "Building virtual env"
	python3 -m venv --clear $(env_dir)
	$(env_dir)/bin/pip install --upgrade --no-cache-dir pip setuptools wheel pylint

.PHONY: env-update
env-update:
	$(env_dir)/bin/pip install --editable .[test]

.PHONY: nopyc
nopyc:
	find . -iname '*.pyc' | xargs rm

.PHONY: env-clean
# I'm not using the env_dir variable on purpose and hardcode the name
# as 'env' to guard against accidents whereby env_dir is set to '/' for
# example
env-clean: nopyc
	rm -rf env

.PHONY: lint-test
lint-test:
	$(env_dir)/bin/python -m unittest tests/test_syntax.py

.PHONY: unit-test
unit-test: nopyc
	$(env_dir)/bin/python -m unittest discover -s tests/unit

.PHONY: integration-test
integration-test: nopyc
	$(env_dir)/bin/python -m unittest discover -s tests/integration

.PHONY: test
test: unit-test integration-test lint-test

.PHONY: test-server
test-server:
	sudo pkill nginx
	sudo nginx -c $(pwd)/nginx.conf
