#!/bin/bash

ps aux | grep python | grep main | grep -v grep | awk '{print $2}' | xargs kill