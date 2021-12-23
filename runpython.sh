#!/bin/zsh
for i in $(ls /mnt/c/Users/br3/Downloads/grafo_*.txt);
	do python3 parte1.py -i $i -k 1 | grep 'saida' | awk -F ':' '{print $2}' |tee `echo $i|awk -F '/' '{print $NF}'`-timingMatrix.txt  
done
for i in $(ls /mnt/c/Users/br3/Downloads/grafo_*.txt);
   do python3 parte1.py -i $i -k 2 | grep 'saida' | awk -F ':' '{print $2}' | tee `echo $i|awk -F '/' '{print $NF}'`-timingLista.txt;
done

