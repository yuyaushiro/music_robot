#!/bin/sh

julius -C etc/command.jconf -module > /dev/null &
echo $! #プロセスIDを出力
sleep 1 #2秒間スリープ
