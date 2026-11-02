#!/usr/bin/env bash

# ==========================================================
# MJ Shell Framework Bootstrap
# ==========================================================

set +e

MJ_BASH_HOME="${MJ_BASH_HOME:-$HOME/.bash}"

for dir in \
"$MJ_BASH_HOME"/01-* \
"$MJ_BASH_HOME"/02-* \
"$MJ_BASH_HOME"/03-* \
"$MJ_BASH_HOME"/04-* \
"$MJ_BASH_HOME"/05-* \
"$MJ_BASH_HOME"/06-* \
"$MJ_BASH_HOME"/07-* \
"$MJ_BASH_HOME"/08-* \
"$MJ_BASH_HOME"/09-* \
"$MJ_BASH_HOME"/10-* \
"$MJ_BASH_HOME"/11-* \
"$MJ_BASH_HOME"/12-* \
"$MJ_BASH_HOME"/13-* \
"$MJ_BASH_HOME"/14-* \
"$MJ_BASH_HOME"/15-* \
"$MJ_BASH_HOME"/16-* \
"$MJ_BASH_HOME"/17-* \
"$MJ_BASH_HOME"/18-* \
"$MJ_BASH_HOME"/19-* \
"$MJ_BASH_HOME"/20-* \
"$MJ_BASH_HOME"/21-* \
"$MJ_BASH_HOME"/22-* \
"$MJ_BASH_HOME"/23-* \
"$MJ_BASH_HOME"/24-* \
"$MJ_BASH_HOME"/25-* \
"$MJ_BASH_HOME"/26-* \
"$MJ_BASH_HOME"/27-* \
"$MJ_BASH_HOME"/28-* \
"$MJ_BASH_HOME"/29-* \
"$MJ_BASH_HOME"/30-* \
"$MJ_BASH_HOME"/31-* \
"$MJ_BASH_HOME"/32-* \
"$MJ_BASH_HOME"/33-* \
"$MJ_BASH_HOME"/34-* \
"$MJ_BASH_HOME"/35-* \
"$MJ_BASH_HOME"/36-* \
"$MJ_BASH_HOME"/37-* \
"$MJ_BASH_HOME"/38-* \
"$MJ_BASH_HOME"/39-* \
"$MJ_BASH_HOME"/40-* \
"$MJ_BASH_HOME"/41-* \
"$MJ_BASH_HOME"/42-* \
"$MJ_BASH_HOME"/43-* \
"$MJ_BASH_HOME"/44-* \
"$MJ_BASH_HOME"/45-* \
"$MJ_BASH_HOME"/46-* \
"$MJ_BASH_HOME"/47-* \
"$MJ_BASH_HOME"/48-* \
"$MJ_BASH_HOME"/49-* \
"$MJ_BASH_HOME"/50-* \
"$MJ_BASH_HOME"/51-* \
"$MJ_BASH_HOME"/52-* \
"$MJ_BASH_HOME"/53-* \
"$MJ_BASH_HOME"/54-* \
"$MJ_BASH_HOME"/55-* \
"$MJ_BASH_HOME"/56-* \
"$MJ_BASH_HOME"/57-* \
"$MJ_BASH_HOME"/58-* \
"$MJ_BASH_HOME"/59-* \
"$MJ_BASH_HOME"/60-* \
"$MJ_BASH_HOME"/61-* \
"$MJ_BASH_HOME"/62-* \
"$MJ_BASH_HOME"/63-* \
"$MJ_BASH_HOME"/64-* \
"$MJ_BASH_HOME"/65-* \
"$MJ_BASH_HOME"/66-* \
"$MJ_BASH_HOME"/67-* \
"$MJ_BASH_HOME"/68-* \
"$MJ_BASH_HOME"/69-* \
"$MJ_BASH_HOME"/70-* \
"$MJ_BASH_HOME"/71-* \
"$MJ_BASH_HOME"/72-* \
"$MJ_BASH_HOME"/73-* \
"$MJ_BASH_HOME"/74-* \
"$MJ_BASH_HOME"/75-* \
"$MJ_BASH_HOME"/76-* \
"$MJ_BASH_HOME"/77-* \
"$MJ_BASH_HOME"/78-* \
"$MJ_BASH_HOME"/79-* \
"$MJ_BASH_HOME"/80-* \
"$MJ_BASH_HOME"/81-* \
"$MJ_BASH_HOME"/82-* \
"$MJ_BASH_HOME"/83-* \
"$MJ_BASH_HOME"/84-* \
"$MJ_BASH_HOME"/85-* \
"$MJ_BASH_HOME"/86-* \
"$MJ_BASH_HOME"/87-* \
"$MJ_BASH_HOME"/88-* \
"$MJ_BASH_HOME"/89-* \
"$MJ_BASH_HOME"/90-* \
"$MJ_BASH_HOME"/91-* \
"$MJ_BASH_HOME"/92-* \
"$MJ_BASH_HOME"/93-* \
"$MJ_BASH_HOME"/94-* \
"$MJ_BASH_HOME"/95-* \
"$MJ_BASH_HOME"/96-* \
"$MJ_BASH_HOME"/97-* \
"$MJ_BASH_HOME"/98-* \
"$MJ_BASH_HOME"/99-*
do

    [[ -d "$dir" ]] || continue

    for file in "$dir"/*.sh
    do
        [[ -f "$file" ]] || continue
        source "$file"
    done

done
