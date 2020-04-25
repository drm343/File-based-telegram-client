#!/usr/bin/env bash
source ./is.sh

id=$(basename "$(find log/* | fzf)")

IFS='+' read -ra ID <<< "$id"

log=$(find log -name "${ID[0]}*")
pipe=$(find pipe -name "${ID[0]}*")

if is not existing "${pipe}"; then
    pipe="pipe/${ID[0]}-${ID[1]}"
    touch $pipe
fi

vim "+open ${pipe}" "+spl ${log}" "+ set noma"
