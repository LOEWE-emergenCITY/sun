#!/bin/env python3
import os

# save output to array

stats = {}

output = os.popen("docker exec sun_core_1 dump_xy.sh").read().splitlines()
for line in output:
    # print(line)
    node, x, y = line.strip().split()
    stats[node] = {"pos": "%s,%s" % (x, y)}
# print(stats)

peers = (
    os.popen(
        "docker exec -it sun_core_1 cea 'dtnquery peers | grep addr | wc -l' | grep -E '\S' | sed -e 's/# HOST: //' | tr -d '\r' | sed 'N;s/\\n/,/'"
    )
    .read()
    .splitlines()
)

for line in peers:
    # print(line)
    node, peers = line.strip().split(",")
    stats[node]["peers"] = peers

bundles = (
    os.popen(
        "docker exec -it sun_core_1 cea 'dtnquery bundles | grep -e dtn: -e ipn: | wc -l' | grep -E '\S' | sed -e 's/# HOST: //' | tr -d '\r' | sed 'N;s/\\n/,/'"
    )
    .read()
    .splitlines()
)
for line in bundles:
    # print(line)
    node, bundles = line.strip().split(",")
    stats[node]["bundles"] = bundles

for k, v in stats.items():
    if not "peers" in v:
        v["peers"] = "0"
    if not "bundles" in v:
        v["bundles"] = "0"

    print("%s %s %s %s" % (k, v["pos"], v["peers"], v["bundles"]))

# append peer lines to output array
# for ((i=0; i<${#peers[@]}; i++)); do
# append peer line to output array at position i
# echo ${output[$i]} ${peers[$i]}
# done

# docker exec -it sun_core_1 cea 'dtnquery bundles | grep -e dtn: -e ipn: | wc -l' | grep -v '#' | grep -E '\S'


# echo $output
