#Get the bed files of different introgression sources on each individual haplotype assembly
sh ./script/Get_SampleHap_Different_Introgressed_Source_Bed.sh

#Get the complementary interval of the introgressed interval in the previous step
sh ./script/Get_SampleHap_Different_Introgressed_Source_Complement_Bed.sh

#Take the input file of MultiWaveInfer, and use MultiWaveInfer to infer the mixing time of different introgressed sources
sh ./script/Get_SampleHap_Different_Source_AutoChromLength.sh
sh ./script/Get_Different_Source_AutoChromLength.sh
sh MultiWaveInfer2.sh
