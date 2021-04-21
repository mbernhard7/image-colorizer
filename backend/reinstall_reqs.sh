#!/bin/bash
ENV=ic-backend
source $WORKON_HOME/$ENV/bin/activate
pip uninstall -y -r <(pip freeze)
pip install -r requirements.txt