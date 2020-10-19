PYTHON	= python3
PYDOC	= pydoc
PYCS	= $(shell find . -name "*.pyc")
BASE	= Example
EXT		= py
FLASK_APP = src/app.py
FLASK_ENV = development
WORKDIR	= ./
PYLINT	= pylint
LINTRCF	= pylintrc.txt
LINTRST	= pylintresult.txt


all:
	@:

clean:
	@for each in ${PYCS} ; do echo "rm -f $${each}" ; rm -f $${each} ; done
	@if [ -e $(LINTRST) ] ; then echo "rm -f $(LINTRST)" ; rm -f $(LINTRST) ; fi
	@find . -name ".DS_Store" -exec rm {} ";" -exec echo rm -f {} ";"

wipe: clean
	@find . -name ".DS_Store" -exec rm {} ";" -exec echo rm -f {} ";"

test: all target
	export FLASK_APP=$(FLASK_APP) \
	export FLASK_ENV=$(FLASK_ENV) \
	export PYTHONPATH=`lldb -P`; \
	$(PYTHON) -m flask run

target: target/main.c
	(cd target; clang -g -O0 main.c)

lint: pylint clean
	@if [ ! -e $(LINTRCF) ] ; then $(PYLINT) --generate-rcfile > $(LINTRCF)  ; fi
	$(PYLINT) --rcfile=$(LINTRCF) `find ./src -name "*.py"` > $(LINTRST) ; less $(LINTRST)

# 
# pip is the PyPA recommended tool for installing Python packages.
# 
pip:
	@if [ -z `which pip` ]; \
	then \
		(cd $(WORKDIR); curl -O https://bootstrap.pypa.io/get-pip.py); \
		(cd $(WORKDIR); sudo -H python get-pip.py); \
		(cd $(WORKDIR); rm -r get-pip.py); \
	else \
		(cd $(WORKDIR); pip install -U pip); \
	fi

# 
# Pylint is a tool that checks for errors in Python code,
# tries to enforce a coding standard and looks for code smells.
# 
pylint:
	@if [ -z `pip list --format=freeze | grep pylint` ]; \
	then \
		(cd $(WORKDIR); pip install pylint); \
	fi

flask:
	@if [ -z `pip list --format=freeze | grep Flask` ]; \
	then \
		(cd $(WORKDIR); pip install Flask); \
	fi

# 
# List of the required packages
# 
list: pip
	@(pip list --format=freeze | grep pip)
	@(pip list --format=freeze | grep pylint)
	@(pip list --format=freeze | grep Flask)

prepare: pip pylint flask

update: pip pylint
