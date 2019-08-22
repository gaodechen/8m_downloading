#!/bin/bash
# Usage: change the chunk name and then run in shell
# it will generate server processes to run the donwload script

for (( i=0; i<24; i++ ))
do
{
    nohup bash download_id_list.sh "mv_ids_$i.txt" > "nohup_$i.out" 2>&1 &
}
done
