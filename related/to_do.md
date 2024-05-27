# To-Do List

1. Fill the tables with info, DONE
2. Code backend
3. Code frontend 
4. Check that we are following guidelines for the project


order bus and make the population of bus rides use train pop as the template.



location: kna
destination:khm
pref:train
scale for pref: x (x*5) min wait to get pref
input funds/amount willing: x
age:if under 12 ticket free else get price

ta fram vägen med preference och pengar i behåll.
ge tillbaka den snabbaste vägen, den billigaste, och den som följer preference.




exempel på procedures: kolla alla available tåg/bussar

function:sum all cost to trip

trigger:age or pengar

join:kolla mellan resor med schedule


General guidelines for queries:
1. At least two of the five queries should deal with data from more than one table, i.e., you should use at least two multirelation queries
2. You should make use of SQL JOIN
3. You should make use of Aggregation and/or Grouping
4. You should make use of at least two of the following:
    a. Triggers
    b. Procedures
    c. Functions