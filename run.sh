#!/bin/bash
python3 web.py > web.log &
python3 logger.py > logger.log &