#!/bin/bash
cd "$(dirname "$0")"
cd ../../..
python -m geneticprogramming.twocars.twocarsexperiment config/geneticprogramming/twocars/default.toml --exhibition-rate 50