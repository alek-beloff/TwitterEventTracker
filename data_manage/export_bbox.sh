#!/bin/bash
test -d ~/.linuxbrew && PATH="$HOME/.linuxbrew/bin:$HOME/.linuxbrew/sbin:$PATH"
mongoexport --db twitterdb --collection stream_boundingBox --out bbox.json
gdrive upload -p 1jprTiCsH6XfCwUc83GO9eIZDjcsiPri8 bbox.json
mv bbox.json ../actual_data/
