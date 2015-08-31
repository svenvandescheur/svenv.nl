#!/bin/bash
date
source /usr/local/bin/virtualenvwrapper.sh
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

workon svenv.nl-ansible
cd $DIR/../svenv.nl-ansible
ansible-playbook site.yml -i $1
date
