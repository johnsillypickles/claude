#!/bin/bash
# usage: wl_take.sh <tool-result-file> : append product_title/date to waitlist.tsv, delete raw file (contains emails), print next cursor and last date
F="$1"
jq -r '.result.data[]|[.attributes.event_properties.product_title, .attributes.datetime, .attributes.event_properties["$event_id"]]|@tsv' "$F" >> waitlist.tsv
echo "last: $(jq -r '.result.data[-1].attributes.datetime' "$F")  rows: $(jq '.result.data|length' "$F")  total: $(wc -l < waitlist.tsv)"
jq -r '.result.links.next // ""' "$F" | grep -o 'page%5Bcursor%5D=[^&]*' | sed 's/page%5Bcursor%5D=//' | python3 -c "import sys,urllib.parse;print('cursor:',urllib.parse.unquote(sys.stdin.read().strip()))"
rm -f "$F"
