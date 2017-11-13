#!/bin/bash
test -d ~/.linuxbrew && PATH="$HOME/.linuxbrew/bin:$HOME/.linuxbrew/sbin:$PATH"
mongoexport --db twitterdb --collection hist_glasgow_bounding_box --out bbox.json
gdrive upload -p 1jprTiCsH6XfCwUc83GO9eIZDjcsiPri8 bbox.json