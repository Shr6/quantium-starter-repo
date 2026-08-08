#!/bin/bash

# Activate virtual environment
source .venv/Scripts/activate

# Run the test suite
pytest

# Return the correct exit code
if [ $? -eq 0 ]; then
    exit 0
else
    exit 1
fi