#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 17:03:03 2021

@author: edneideramalho
"""

import numpy as np
import pandas as pd
import seaborn as sns



a = np.zeros(10)

print(a)

name = "neidinha"

type(name)

x = np.linspace(0, 100, 100)

y = np.linspace(0, 100, 100)

sns.lineplot(x = x, y = y**2)