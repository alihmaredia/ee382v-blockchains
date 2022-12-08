# Assignment 02 - Bitcoin Script

Name    : Ali Maredia  
Email   : ali.maredia@utexas.edu  
Discord : alihmaredia 

## Program Inputs

The input of the script has two integers that we will be used for some simple math operations.

```python
<1>
<2>
```

## Program Script

The script goes through the following operations:

```python
OP_ADD     # Checking some basic addition.
<3>        # Introducing another number for comparison.    
OP_EQUAL   # Checking equality, does 3 = 3?
<-1>       # Answer is true, so introducing another number for comparison.  
OP_EQUAL   # Checking equality, does 1 = -1?
<-0>       # Answer is false, but can we introduce -0 for another comparison?
OP_EQUAL   # Hmmm, -0 is not possible in Script Wiz but confirmed with supertestnet that it's 0x80 in Bitcoin Script.
```

## Result

The `OP_EQUAL` result should evaluate to true, because in Script Wiz, -0 = 0. In a sense, -0 is not possible in Script Wiz while it is 0x80 in Bitcoin Script.

## Resources

**Script Wiz IDE**  
https://ide.scriptwiz.app
