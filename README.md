The test 
===================================================================================
    
## CONTENTS / СОДЕРЖАНИЕ ##
[testVer1](#testVer1) - Version 1.  
[testVer2](#testVer2) - Version 2.  

-----

### testVer1 ###
See the source code [here](testVer1.py)   

A very simple implementation. First searches for two-word names, than searhes again for the one-word names.   

Advantages: fast enough
Drawbacks: usually fails when a two-word name and a one-word name are followed one after another without any splitting.  

### testVer2 ###
See the source code [here](testVer2.py)   

A slow one. Tries all possible permutations of the one-word names stored in the context to "apply" each for possible "solution". Each permutation is scored with the jaro function. If two one-word names that constitute a full name are found together in a permutation, these names are scored by the jaro function as a two-word name and may be granted with addiotional score points. 

Advantages: any possible combination of names including full names as well as one-word ones is recognized, e.g. 'I like movies with Jon Way Cruis Client East' (please refer to the [code](testVer2.py))       
Drawbacks: works too slowly (but can be optimized).
