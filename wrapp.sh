#!/bin/bash

gcc -o wrapper wrapper.c
chown root:pi wrapper
chmod 4755 wrapper
