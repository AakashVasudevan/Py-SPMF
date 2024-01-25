MAGENTA='tput setaf 5'
RESET='tput sgr0'

setup-environment:
	@echo "Setup Environment"
	@conda env create -f environment.yaml
	@echo "Remember to activate the environment with these instructions ^"

format:
	@echo "Running autopep8 and isort to fix any formatting issues in the code"
	@autopep8 --in-place --recursive .
	@isort .
	@echo "Running flak8 to check for any formatting issues"
	@flak8 .
