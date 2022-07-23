# Set your appropriate custom paths if needed

PYTHON = python3
PIP = pip3

PROJECT_DIR = /
PROJECT_MAIN = WindowController.py # change if needed
MAIN_FILENAME = WindowController
VERSION = v1.0

# made by leifadev on github

.DEFAULT_GOAL = help
.PHONY: help upgrade clean build

help:
	@echo "\n---------------HELP-----------------\n"
	@echo "make help - display this message"
	@echo "make upgrade - updates repository modules"
	@echo "make run - run the binary in your compiled .app quickly!"
	@echo "make clean - clean up files"
	@echo "make build - builds the repo into .app dist"
	@echo "\n-------------------------------------\n"
	@echo "\nCoded by leifadev\nhttps://github.com/leifadev/shoutout\n"

upgrade:
	@echo Updating all modules!
	@echo "\n\nInstalling pip-upgrade\n"
	@${PIP} install pip-upgrade
	@${PIP} freeze >> requirements.txt
	@pip-upgrade requirements.txt --skip-virtualenv-check

	# Install PyObj-C if not installed for first time
	@echo "\n\n**Installing/Updating PyObj-C!**\n\n"
	@${PIP} install -U pyobjc
	@echo "\n Done!\n"

run:
	@echo Running the apps python binary!
	@./dist/${MAIN_FILENAME}.app/Contents/MacOS/${MAIN_FILENAME}


clean:
	@echo "Cleaning project\n\n--------------------------\n"
	rm -rf *.pyc
	rm -rf *.pyo
	rm -rf build/
	rm -rf dist/
	rm -rf *.build/
	rm -rf *.dist/
	rm -rf __pycache__/
	rm -rf requirements.txt
	@echo "\nFreezing your project! Updated requirements.txt"
	@echo "\n--------------------------"


build:
	@echo "Building standalone application with py2app"
	@echo "Change your PYTHON path in Makefile accordingly if I fail!"
	@${PYTHON} setup.py py2app -A
	@echo "You did it!"


all:
	@make clean
	@${PYTHON} setup.py py2app -A
	@make run
