PYTHON = python
SCRIPT = mel_spectogram.py
AUDIO ?= example.wav
MODE ?=grunt

.PHONY: create run reset clear_result clear_sound

create:
	$(PYTHON) -m venv venv
	venv/Scripts/pip install -r requirements.txt || venv/bin/pip install -r requirements.txt
	@echo "Virtual environment is ready."
	@echo "To activate it manually:"
	@echo "  Windows: . venv/Scripts/activate"
	@echo "  Linux/Mac: source venv/bin/activate"

run: 
	python $(SCRIPT) ./sounds/$(AUDIO) $(MODE)

reset:
	find . -type d -name "__pycache__" -exec rm -rf {} + || true
	find . -type d -name "result" -exec sh -c 'cd "$$1" && find . -type f ! -name ".gitkeep" -delete' sh {} \; || true
	find . -type d -name "sounds" -exec sh -c 'cd "$$1" && find . -type f ! -name ".gitkeep" -delete' sh {} \; || true
	rm -rf venv

clear_result:
	find ./result -type f ! -name ".gitkeep" -delete

clear_sound:
	find ./sounds -type f ! -name ".gitkeep" -delete