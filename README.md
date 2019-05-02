# Superhero Analysis

##  Mohit Gupta
### University of Illinois, Urbana-Champaign
### Final Project (Spring-2019)
### Programming for Analytics & Data Processing (IS 590 PR)

======
## Introduction

Marvel and DC are the most famous and prominent names for publishing superhero based movies and related media imprints. The fans have argued since decades about the superiority of characters from each of the comic house and which production house is better. Is it DC Comics or Marvels? 

The project is all about finding which one is better? 
#### Marvel or DC!


======

# Hypothesis:

I have assumed the below hypothesis to conduct the analysis:

1. Captain America and Iron Man are the most powerful duos in the superhero leagues from all the production houses.

2. Earnings of superhero movies are not affected by the eye color, height, weight and hair color of superheros.

3. Marvel is not popular than DC Comics.

4. Human superheros are not popular as compared to non-human superheros.

======

# Questions & Answers after analysis:

Que 1.

Top 12 superheros (6+6) from both the publishers on the basis of comic appearances:

| Superhero Name  | Publisher   | Appearances  |
|:---------------:|:-----------:|:------------:|
|   Batman        |  DC Comics  |       3093.0 |
|Superman         | DC Comics   |      2496.0  |
|  Wonder Woman   |  DC Comics  |       1231.0 |
|  Aquaman        |  DC Comics  |       1121.0 |
|  Alan Scott     |  DC Comics  |  969.0       |
|Alfred Pennyworth| DC Comics   | 930.0        |
|   Spider-Man    |Marvel Comics| 4043.0       |
|  Captain America|Marvel Comics| 3360.0       |
| Wolverine       |Marvel Comics|       3061.0 |
|  Iron Man       |Marvel Comics|       2961.0 |
|  Hulk           |Marvel Comics|      2017.0  |
|   Jean Grey     |Marvel Comics|  1107.0      |

1.a) Find six pairs of two characters who appeared most in comics(3 pairs Marvel + 3 Pairs DC)

1.b) Compare their combined power levels and check who wins.

| Superhero Pair Name  | Publisher   | Combined Power  |
|:---------------:|:-----------:|:------------:|
|         Superman & Alan Scott        |  DC Comics  |       965 |
| Spider-Man & Jean Grey          | Marvel Comics   |      937  |
|       Wonder Woman & Aquaman |  DC Comics  |       898 |
|    Wolverine & Iron Man  |  Marvel Comics  |       861 |
|   Captain America & Hulk |  Marvel Comics  |  780       |
|Batman & Alfred Pennyworth | DC Comics   | 486        |


### Also, the combined power of Captain America and Iron Man:	 811


Que 2. 

2.a) I will group the top 5 movies from Marvel and DC and check publishing house earned more.

| Publisher  | Earnings(Top 5 movies)($)  |
|:---:|:---:|
| Marvel Comics  |  $ 2,673,994,705 |
|  DC Comics | $ 2,061,358,541  |


2.b) I will group all the movies from respective publishing house and then check the total amount earned by both the publishing houses.

| Publisher  | Earnings(Top 5 movies)($)  |
|:---:|:---:|
| Marvel Comics  |  $ 10,096,393,849 |
|  DC Comics | $ 3,357,798,524  |

Que 3. Are non-human superheros not more popular as compared to mutant superheros.
3.a) The count of number of human and mutant superheros for both the publishers.

| Publisher  | Race   | Combined Power  |
|:---------------:|:-----------:|:------------:|
|         DC Comics        |  Human  |       13 |
|          | Mutant   |      50  |
|       Marvel Comics |  Human  |       25 |
|      |  Mutant  |       107 |

3.b) The count of number of human and mutant superheros no matter who was their publisher.

Total number of Humans and Mutants in the final dataframe:

| Race  | Count  |
|:---:|:---:|
| Human  |  38 |
|  Mutant | 157 |

Que 4. Find the statistics of characters with different hair color, eye color, height and weight.

| Publisher  | Eye Color   | Hair Color  |Count|
|:---------------:|:-----------:|:------------:|:-----:|
|   Marvel Comics        |  Brown  |       Black |775|
|Superman         |    |      Brown  |621|
|  Wonder Woman   |  Blue  |       Blond |599|
|  DC Comics        |  Brown  |       Black |429|
|   Marvel Comics     |  Blue  |  Black      |361|

Que 5. Superheros with what hair color and eye color are more prone to live and die?

| Alive  | Eye Color   | Hair Color  |Count|
|:---------------:|:-----------:|:------------:|:-----:|
|   Living        |  Brown  |       Black |932|
|         |  Blue  |      Blond  |689|
|     |  Brown  |       Brown |673|
|     |  Blue  |       Black |431|
|      |    |  Black      |361|
|           |    |       Brown |309|
|      Deceased     |  Brown  |       Brown |273|
|           |  Brown  |       Black |272|
|           |  Blue  |       Blond |241|
|           |  Blue  |       Black |183|


Que 6. What their race has to do with their Intelligence, Strength, Speed, Durability, Power, Combat, Total ?

Que 7. How are height and weight distributed for characters in different publishing house?

Que 8. How many movie appearances does the characters with most comic appearances have?

======
























