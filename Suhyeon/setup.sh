#!/bin/bash

# 필수 라이브러리 설치
sudo apt-get update && sudo apt-get install -y \
  libnss3 \
  libxss1 \
  fonts-liberation \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libcups2 \
  libdbus-1-3 \
  libgdk-pixbuf2.0-0 \
  libnspr4 \
  libx11-xcb1 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  xdg-utils \
  wget

# Google Chrome 설치
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# WebDriver 설치 (옵션)
pip install webdriver-manager

export CHROME_BIN="/usr/bin/google-chrome"
export PATH="$PATH:/usr/bin"