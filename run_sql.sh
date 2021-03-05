#!/bin/bash
docker-compose up -d
docker-compose exec work-env python sql.py
