# Set your appropriate custom paths if needed

PYTHON = python3
PIP = pip3

PROJECT_DIR = /
PROJECT_MAIN = main.py # change if needed
MAIN_FILENAME = main
VERSION = v1.0

# made by leifadev on github

.DEFAULT_GOAL = help
.PHONY: help setup clean build


help:
	@echo "\n---------------HELP-----------------"
	@echo "make help - display this message"
	@echo "make setup - setup and update the repo"
	@echo "make run - run the binary in your compiled .app quickly!"
	@echo "make clean - clean up files"
	@echo "make build - builds the repo into .app dist"
	@echo "-------------------------------------"
	@echo "\nCoded by leifadev\nhttps://github.com/leifadev/shoutout\n"

setup:
	@echo "Option not supported yet"


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
