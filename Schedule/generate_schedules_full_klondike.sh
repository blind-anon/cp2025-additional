#!/bin/bash

usage() {
    echo "Usage: $0 <eprime_location> <data_directory> <output_csv>"
}

isnumber() {
    [[ "$1" == ?(-)+([0-9]) ]]
}

if [ $# -lt 3 ]; then
    echo "Incorrect number of arguments supplied" && usage
    exit 1
fi

model=$1
data_directory=$2
csv=$3
seeds=1000
total_seeds=10000
granularity=10

echo "timeout,files,order,time_portion,test_par10_optimal,test_fraction_optimal,test_par10_solvitaire_no_streamliner,test_fraction_solvitaire_no_streamliner,test_par10_model,test_fraction_model,test_par10_relaxed,test_fraction_relaxed,test_par10_strict,test_fraction_strict,test_par10_relaxed-solvitaire_no_streamliner,test_fraction_relaxed-solvitaire_no_streamliner,test_par10_strict-solvitaire_no_streamliner,test_fraction_strict-solvitaire_no_streamliner,test_par10_relaxed-model-solvitaire_no_streamliner,test_fraction_relaxed-model-solvitaire_no_streamliner,test_par10_strict-model-solvitaire_no_streamliner,test_fraction_strict-model-solvitaire_no_streamliner,test_par10_smart_solvitaire,test_fraction_smart_solvitaire" > $csv

for i in $(seq 1 10); do
    echo "Processing timeout $i"
    echo -n "$i," >> $csv
    ./parse_streamlined_results.sh $model $data_directory $seeds $total_seeds $i $granularity >> $csv
done

for i in $(seq 12 4 28); do
    echo "Processing timeout $i"
    echo -n "$i," >> $csv
    ./parse_streamlined_results.sh $model $data_directory $seeds $total_seeds $i $granularity >> $csv
done

for i in $(seq 30 20 170); do
    echo "Processing timeout $i"
    echo -n "$i," >> $csv
    ./parse_streamlined_results.sh $model $data_directory $seeds $total_seeds $i $granularity >> $csv
done

for i in $(seq 180 180 3600); do
    echo "Processing timeout $i"
    echo -n "$i," >> $csv
    ./parse_streamlined_results.sh $model $data_directory $seeds $total_seeds $i $granularity >> $csv
done
