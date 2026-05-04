credit_risk_db=# select count(id) from loan_data where person_age not between 18 and 75;

 count
-------
     0
(1 row)


credit_risk_db=# select person_gender, count(id) from loan_data group by person_gender;
 person_gender | count
---------------+-------
 male          | 24832
 female        | 20156
(2 rows)


credit_risk_db=# select person_education, count(id) from loan_data group by person_education;
 person_education | count
------------------+-------
 Doctorate        |   621
 High School      | 11967
 Associate        | 12025
 Bachelor         | 13395
 Master           |  6980
(5 rows)


credit_risk_db=# select person_home_ownership, count(id) from loan_data group by person_home_ownership;
 person_home_ownership | count
-----------------------+-------
 MORTGAGE              | 18484
 RENT                  | 23436
 OTHER                 |   117
 OWN                   |  2951
(4 rows)


credit_risk_db=# select loan_intent, count(id) from loan_data group by loan_intent;
    loan_intent    | count
-------------------+-------
 VENTURE           |  7815
 PERSONAL          |  7550
 DEBTCONSOLIDATION |  7145
 MEDICAL           |  8544
 HOMEIMPROVEMENT   |  4783
 EDUCATION         |  9151
(6 rows)


credit_risk_db=# select previous_loan_defaults_on_file, count(id) from loan_data group by previous_loan_defaults_on_file;
 previous_loan_defaults_on_file | count
--------------------------------+-------
 No                             | 22133
 Yes                            | 22855
(2 rows)


credit_risk_db=# select loan_status, count(id) from loan_data group by loan_status;
 loan_status | count
-------------+-------
           0 | 34988
           1 | 10000
(2 rows)


credit_risk_db=# SELECT loan_status, AVG(credit_score) AS avg_score
credit_risk_db-# FROM loan_data
credit_risk_db-# GROUP BY loan_status;
 loan_status |      avg_score
-------------+----------------------
           0 | 632.7694066537098434
           1 | 631.8872000000000000
(2 rows)


credit_risk_db=# SELECT loan_status, AVG(loan_percent_income) AS avg_ratio
credit_risk_db-# FROM loan_data
credit_risk_db-# GROUP BY loan_status;
 loan_status |       avg_ratio
-------------+------------------------
           0 | 0.12182062884591026675
           1 | 0.20253200902113999492
(2 rows)


credit_risk_db=# SELECT previous_loan_defaults_on_file, loan_status, COUNT(*)
credit_risk_db-# FROM loan_data
credit_risk_db-# GROUP BY previous_loan_defaults_on_file, loan_status;
 previous_loan_defaults_on_file | loan_status | count
--------------------------------+-------------+-------
 No                             |           1 | 10000
 No                             |           0 | 12133
 Yes                            |           0 | 22855
(3 rows)


credit_risk_db=# SELECT
credit_risk_db-#     CASE
credit_risk_db-#         WHEN person_income < 50000 THEN 'Low'
credit_risk_db-#         WHEN person_income < 100000 THEN 'Medium'
credit_risk_db-#         ELSE 'High'
credit_risk_db-#     END AS income_group,
credit_risk_db-#     AVG(loan_status) AS default_rate
credit_risk_db-# FROM loan_data
credit_risk_db-# GROUP BY income_group;
 income_group |      default_rate
--------------+------------------------
 Low          | 0.37957994787674382953
 Medium       | 0.18710089399744572158
 High         | 0.09443002595328408864
(3 rows)


credit_risk_db=# SELECT loan_status, COUNT(*)
credit_risk_db-# FROM loan_data
credit_risk_db-# GROUP BY loan_status;
 loan_status | count
-------------+-------
           0 | 34988
           1 | 10000
(2 rows)


credit_risk_db=# SELECT
credit_risk_db-#     CASE
credit_risk_db-#         WHEN person_age < 25 THEN 'Young'
credit_risk_db-#         WHEN person_age < 40 THEN 'Mid'
credit_risk_db-#         ELSE 'Senior'
credit_risk_db-#     END AS age_group,
credit_risk_db-#     AVG(loan_status) AS default_rate
credit_risk_db-# FROM loan_data
credit_risk_db-# GROUP BY age_group;
 age_group |      default_rate
-----------+------------------------
 Mid       | 0.21500855718431430910
 Senior    | 0.21461397058823529412
 Young     | 0.23559683695242876867