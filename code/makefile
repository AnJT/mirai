.PHONY: help run

SOURCE=main.py
PYTHON=python3
OUT=main.log

run: ${SOURCE}
	nohup ${PYTHON} ${SOURCE}>${OUT} 2>&1 &

help:
	@echo "make run"
	@echo "       run project"
	@echo "make clean"
	@echo "       clean python cache files"

clean-pyc:
	@find . -name '*.pyc' -delete

clean:clean-pyc
	@echo "## Clean all data."