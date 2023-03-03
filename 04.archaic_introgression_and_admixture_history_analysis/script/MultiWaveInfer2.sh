for Source in $(cat Source.list)
do
nohup ~/software/MultiWaver2.0-master/src/MultiWaveInfer2 -i TMP_Bed/${Source}_Source_Fragmet_Length -o  ${Source}_Source -t 1 -g ${Source}_Source.log -M DMode --bootstrap 1000 &
done
