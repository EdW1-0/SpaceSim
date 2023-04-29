#! /bin/bash

coverage run -m unittest discover
coverage lcov
coverage report