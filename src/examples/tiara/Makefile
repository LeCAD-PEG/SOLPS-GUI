# Extracts and shows some meshing examples from ITER, AUG and COMPASS

EXAMPLES = traduit.out.b2us.standard b2fgmtry_st b2fgmtry traduit.out.b2us_iter traduit.out.b2us.target
TARGETS = $(EXAMPLES:%=${HOME}/Downloads/%)
NOTEBOOK = plot_traduit_out_b2us_or_b2fgmtry.ipynb

all: $(TARGETS) local ## Unpacks example files under $HOME/Downloads and creates local environment

query-%: ## For Makefile debugging. Example: make query-TARGETS
	@echo $($(*))

$(TARGETS) &: plot_traduit_out_b2us_or_b2fgmtry_examples.tar.gz
	tar xvmz -C ${HOME}/Downloads/ -f $^

local: ## Use: source local/bin/activate or local/bin/jupyter-notebook plot_traduit_out_b2us_or_b2fgmtry.ipynb
	python3 -m venv local
	python3 -m pip install --upgrade pip
	python3 -m pip install matplotlib>=3.5.0 jupyter numpy pyside6
	local/bin/jupyter-notebook $(NOTEBOOK)

run: $(TARGETS) local ## Unpacks and runs notebook example
	local/bin/jupyter-notebook $(NOTEBOOK)


clean: ## Removes example files from Downloads and local environment
	mv local local.old
	rm -fr $(TARGETS) local.old local
	 

help : # https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -Eh '^[a-zA-Z0-9_%\./-]+[ ]*:.*?## .*$$' $(MAKEFILE_LIST) |sort|awk \
	'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

