#!/bin/zsh
cd ~/memorious/
conda --version
# conda init zsh
/bin/date
. activate memorious
conda env list
echo "Operation is finished"
memorious list
memorious run kg_super
	
