#!/usr/bin/env python3
# File: start.py
# Author: Oluwatobiloba Light
"""Application startup script"""


import uvicorn


if __name__ == "__main__":
    uvicorn.run('app.main:app',
                host="0.0.0.0", port=8000, reload=True)
