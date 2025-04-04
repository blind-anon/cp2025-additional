#!/bin/bash

usage() {
    echo "Usage: $0 <eprime_location> <data_directory> <train_seeds> <total_seeds> <timeout_seconds>"
}

isnumber() {
    [[ "$1" == ?(-)+([0-9]) ]]
}

if [ $# -lt 5 ]; then
    echo "Incorrect number of arguments supplied" && usage
    exit 1
fi

model=$1
data_directory=$2
seeds=$3
total_seeds=$4
timeout=$5
granularity=10

let "seeds++"

temp_directory="temp"

test -d $data_directory/$temp_directory || mkdir $data_directory/$temp_directory

(
    cd $data_directory; 
    for f in ./*.csv; do
        cat $f | head -n $seeds > "$temp_directory/$f"
    done
)

param_name="temp.param"
order_file="temp.order"
timeout_file="temp.timeout"

./create_param_from_csv.py $data_directory/$temp_directory $param_name $granularity $timeout | tr -d '\n'
echo -n ','

savilerow $model $param_name -run-solver -chuffed -O1 &> /dev/null 

cat $param_name.solution | grep "letting order be" > $order_file
cat $param_name.solution | grep "letting timePortion be" > $timeout_file

rm $param_name*
rm -rf $data_directory/$temp_directory

./square_brakets_to_list.py $order_file | tr -d '\n'
echo -n ','

./square_brakets_to_list.py $timeout_file | tr -d '\n'
echo -n ','

./parse_to_suspended_par10.py $data_directory $order_file $timeout_file $seeds $total_seeds $granularity | tr -d '\n'
echo -n ','
./parse_to_suspended_fraction_certain.py $data_directory $order_file $timeout_file $seeds $total_seeds $granularity | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/1_solvitaire_no_streamliner.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/1_solvitaire_no_streamliner.csv $timeout $3 | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/7_full_model_noworryback.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/7_full_model_noworryback.csv $timeout $3 | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/4_unblocked_relaxed_stock.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/4_unblocked_relaxed_stock.csv $timeout $3 | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/3_unblocked_full_stock.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/3_unblocked_full_stock.csv $timeout $3 | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/4_unblocked_relaxed_stock.csv,data/1_solvitaire_no_streamliner.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/4_unblocked_relaxed_stock.csv,data/1_solvitaire_no_streamliner.csv $timeout $3 | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/3_unblocked_full_stock.csv,data/1_solvitaire_no_streamliner.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/3_unblocked_full_stock.csv,data/1_solvitaire_no_streamliner.csv $timeout $3 | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/4_unblocked_relaxed_stock.csv,data/7_full_model_noworryback.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/4_unblocked_relaxed_stock.csv,data/7_full_model_noworryback.csv $timeout $3 | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/3_unblocked_full_stock.csv,data/7_full_model_noworryback.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/3_unblocked_full_stock.csv,data/7_full_model_noworryback.csv $timeout $3 | tr -d '\n'
echo -n ','

./calculate_suspended_par10.py data/5_solvitaire_smart.csv $timeout $3 | tr -d '\n'
echo -n ','
./calculate_suspended_fraction_certain.py data/5_solvitaire_smart.csv $timeout $3

rm $order_file
rm $timeout_file
