import os

import yaml

from src.core.config.utils import unify_name

root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../'))

with open(os.path.join(root_dir, 'project.yaml')) as stream:
    project_metadata = yaml.safe_load(stream)

project_name = unify_name(project_metadata['name'])
