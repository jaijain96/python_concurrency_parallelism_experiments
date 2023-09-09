#!/usr/bin/env bash

export PATH="$HOME/.pyenv/bin:$PATH"
# echo $PATH
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
# exec "$SHELL"
/root/.pyenv/bin/pyenv install 3.9.16
/root/.pyenv/bin/pyenv global 3.9.16
python -V
which python
pip --version
pip install -r requirements.txt
# python -m flask run --host=0.0.0.0
