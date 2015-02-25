#!/usr/bin/env python

import titp_write

titp_write.generate()

import os

if os.path.exists('now.list'):
    os.remove('now.list')
