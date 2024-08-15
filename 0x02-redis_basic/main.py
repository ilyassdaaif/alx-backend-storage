#!/usr/bin/env python3
""" Main file """

# Import the exercise module
import exercise

# Import the Cache class and replay function
Cache = exercise.Cache
replay = exercise.replay

# Create an instance of Cache
cache = Cache()

# Store some values
cache.store("foo")
cache.store("bar")
cache.store(42)

# Replay the history of the store method
replay(cache.store)
