#!/bin/bash
test -d ~/.linuxbrew && PATH="$HOME/.linuxbrew/bin:$HOME/.linuxbrew/sbin:$PATH"
mongoexport --db twitterdb --collection hist_glasgow_nogeolocation --out nogeo.json
gdrive upload -p 1jprTiCsH6XfCwUc83GO9eIZDjcsiPri8 nogeo.json
rm nogeo.json