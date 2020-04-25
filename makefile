DIR_CHECK := log pipe

.PHONY: prepare prepare-python3-env
prepare: $(DIR_CHECK) prepare-python3-env
	@echo "ok"

$(DIR_CHECK):
	@mkdir -p $(DIR_CHECK)

prepare-python3-env:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
