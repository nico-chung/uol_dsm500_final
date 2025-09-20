## Pairwise Mann-Whitney on num_rois (Holm-Bonferroni-corrected)

| cat1           | cat2           |      U |    p_raw |   p_corrected | significant   |
|:---------------|:---------------|-------:|---------:|--------------:|:--------------|
| Action         | Affective      | 5549.5 | 0.159    |      0.635    | False         |
| Action         | Social         | 2840.5 | 4.91e-08 |      5.9e-07  | True          |
| Action         | Indoor         | 4775   | 0.566    |      1        | False         |
| Action         | OutdoorManMade | 5516.5 | 0.184    |      0.635    | False         |
| Action         | OutdoorNatural | 6414.5 | 0.000236 |      0.002    | True          |
| Affective      | Social         | 2392.5 | 4.79e-11 |      6.23e-10 | True          |
| Affective      | Indoor         | 4222   | 0.046    |      0.278    | False         |
| Affective      | OutdoorManMade | 4934   | 0.865    |      1        | False         |
| Affective      | OutdoorNatural | 5855.5 | 0.024    |      0.171    | False         |
| Social         | Indoor         | 6984.5 | 5.13e-07 |      5.65e-06 | True          |
| Social         | OutdoorManMade | 7676   | 1.28e-11 |      1.79e-10 | True          |
| Social         | OutdoorNatural | 8346   | 2.65e-17 |      3.98e-16 | True          |
| Indoor         | OutdoorManMade | 5761   | 0.05     |      0.278    | False         |
| Indoor         | OutdoorNatural | 6652   | 1.88e-05 |      0.000188 | True          |
| OutdoorManMade | OutdoorNatural | 5972.5 | 0.01     |      0.084    | False         |