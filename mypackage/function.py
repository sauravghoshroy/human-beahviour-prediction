#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Name of the project: Individual Programming Exercise: (IPE)
# Description: A program that "predicts" human behavior using a simple game.
# File Name: function.py
# File Description: Python code of the function that generates random numbers for the IPE program.
# Author: Saurav Ghosh Roy
# Last Updated: Thu 7 Feb, 2021
"""
def rand_num_gen(x) :
    """generates a random number using the linear congruence method."""
    y = ((22695477*int(x))+1) % (2**32)
    return y