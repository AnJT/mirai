.PHONY: help run

OUT=mcl.log

run: mcl
	nohup ./mcl >mcl.log 2>&1 &

help:
	@echo "make run"
	@echo "       run project"
