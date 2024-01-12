SemVer Formatter Plugin for Seano
=================================

This project provides a Seano formatter named `semver` which, given a query of a
Seano database, will tell you what version the current version of your product
should be, assuming you're following [SemVer](https://semver.org) conventions.

Testing Locally
---------------

Starting from scratch, this is how to set up local unit testing:

```sh
# Create and enter a virtual environment:
virtualenv .venv
. .venv/bin/activate

# Install this Seano formatter plugin in the virtual environment in "editable mode"
pip install -e .

# Install extra dependencies needed by the unit tests:
pip install -r ci_utest_requirements.txt
```

Then, going forward, you can run unit tests like this:

```sh
pytest
```
