# Set your appropriate custom paths if needed

PYTHON = python3
PIP = pip3

PROJECT_DIR = /
PROJECT_MAIN = main.py # change if needed
MAIN_FILENAME = Shoutout!
VERSION = v1.0

# made by leifadev on github

.DEFAULT_GOAL = help
.PHONY: help setup upgrade clean build

help:
	@echo "\n-----------HELP!!!! AHHHHH-----------\n"
	@echo "make help - display HELP AHHHHH WHYYYY I HATE THIS!!!"
	@echo "make setup - Sets up your project with the essential PyObj-C modules and files"
	@echo "make upgrade - updates all repository modules"
	@echo "make run - run the binary in your compiled .app quickly!"
	@echo "make clean - clean up files"
	@echo "make build - builds the repo into .app dist"
	@echo "make all - run all above functions except upgrade"
	@echo "\n-------------------------------------"
	@echo "	          ${VERSION}  "
	@echo "PyObj-C Makefile by leifadev\nhttps://github.com/leifadev/shoutout\n"
	@echo "Your Variables:  ${PYTHON}, ${PIP}  ${PROJECT_MAIN}, ${MAIN_FILENAME}"


setup:
	@echo Setting up your directory with py2app and pyobjc!
	@${PIP} install py2app pyobjc
	@echo "Trying to make a setup.py for: PROJECT_MAIN=${PROJECT_MAIN}"


upgrade:
	@echo Updating all modules!
	@echo "\n\nInstalling pip-upgrade\n"
	@${PIP} install pip-upgrade
	rm requirements.txt
	@${PIP} freeze >> requirements.txt
	@pip-upgrade requirements.txt

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
	@echo "\nFreezing your project! Updated requirements.txt"
	@echo "\n--------------------------"


build:
	@echo "Building standalone application with py2app"
	@echo "Change your PYTHON path in Makefile accordingly if I fail!"
	@echo "\nBuilding in alias mode! For standalone build remove -A in this Makefile"
	@${PYTHON} setup.py py2app -A
	@echo "You did it!"


all:
	@echo Cleaning building, and running your app!
	@make clean
	@make build
	@make run
