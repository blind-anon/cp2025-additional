# Solving Klondike

This repo provides three constraint models our constraint-based scheduling approach for solving Klondike games.

## Dependencies

- [savilerow](https://www-users.york.ac.uk/peter.nightingale/savilerow/)
- python3

## Constraint models

The three constraint models are in folder `Models/`:
- `Models/unblocked_artifact_relaxed_stock_v1.0.eprime` and `Models/unblocked_artifact_full_stock_v1.2.eprime`: two constraint models for the relaxed version of Klondike, can quickly solve unwinnable Klondike games but cannot prove winnability.
- `Models/noworryback_fullmodel_v0.3.eprime`: a complete constraint model for Klondike without worrying-back. This model cannot prove unwinnability in full Klondike when worrying-back is allowed.

## Solving schedules:

The `Schedule/` folder provides all scripts, data and results for combining the three constraint models and Solvitaire in a schedule. To re-generate the optimal schedules for each Klondike game version, run the following command:

For Klondike games:
```
cd Schedule/
chmod +x generate_schedules_klondike.sh
./generate_schedules_klondike.sh model/schedule.eprime klondike_data/ schedules-klondike.csv
```

For full Klondike games (worrying-back allowed):
```
cd Schedule/
chmod +x generate_schedules_klondike.sh
./generate_schedules_full_klondike.sh model/schedule.eprime full_klondike_data/ schedules-full-klondike.csv
```

The script will compute the optimal schedules for a range of cutoff times from 1s to 3600s and compare them with various baselines. 

We also provide the pre-computed schedules in `results/`. 
