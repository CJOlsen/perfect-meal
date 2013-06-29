Perfect Meal
Author: Christopher Olsen
License: GNU GPL v3 (only applies to my work which will have my name on it, the
                     rest should point back to the original author/owner.)


Background/About:

The USDA maintains a huge dataset of foods and their nutrients, I was able to
find a JSON version of this data.  While a brute force search through the
data problem space to find a "perfect meal" (a combination of foods that meets a
full set of nutritional constraints) is NP-Hard, and a search to find *if*
a solution exists is NP-Complete, the problem can be approached through other
strategies - such as greedy algorithms and only searching a subset of the entire
database.  

The class of problem is called the "Multiple Objective Knapsack Problem" and in
the case of this program the number of objectives is not necessarily known;
one can use the constraints on Elements, or Vitamins, or both at this time.
Element and Vitamin constraints come from the USDA's nutritional guidelines, 
they are in 'mg per day' for now as the program is still in the Proof Of Concept
phase.  If one had desired nutritional values for Amino Acids or Fats, those
could be added as well.  

Constraints in this program have both lower and upper bounds, which complicates 
things because in the effort to increase a lagging value, a value which has 
already met its minimum constraint may get pushed over its maximum constraint.
For this reason the most promising algorithm is a "Greedy Balance" algorithm 
that focuses on balancing progress across the entire nutrient profile.  The 
Greedy Balance algorithm is the only one that has produced a valid result thus
far, although the resulting meal would make little sense in the real world.

Problems:

- loading from the modified JSON database is *slow*
- checking the data is difficult and time-consuming, and the solutions are only
  as good as the data
- needs more algorithms, brute-force on a small subset of data, ant-colony,
  and dynamic 
- the algorithm section needs to be refactored in order to facilitate easy 
  expression of algorithmic ideas (it's not at all clear right now)
