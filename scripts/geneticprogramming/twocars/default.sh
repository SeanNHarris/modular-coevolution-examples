#!/bin/bash
cd "$(dirname "$0")"
cd ../../..
python -m modularcoevolution.drivers.coevolutiondriver geneticprogramming/twocars/default.toml --exhibition-rate 50