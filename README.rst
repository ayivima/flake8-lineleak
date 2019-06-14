FLAKE8-LINELEAK
===============

Introduction
------------
If your script has more than a set number of lines, your code lines are leaking :)
...And if your code lines are leaking, it's difficult to navigate and understand :).

Lineleak is a ``flake8`` plugin that counts the lines containing live code in a script, 
and 'yells' if a set limit is exceeded. It is meant to help enforce short scripts and 
modular python programming.

For usefulness, lineleak only counts lines which contains live code. Thus the following 
lines are excluded from a count:

* Blank lines
* Comment lines
* Lines of a docstring 


Usage 
-----
To benefit from ``lineleak``, Use flake8 the usual way with plugins::

    $ flake8 [options] file ... 

The default line count limit is set at 100, and imposed on physical lines. These defaults, 
however, can be overridden with optional arguments as shown below and illustrated in the 
illustration section::
    
	optional arguments:
    
      --lineleak-logical
	         Applies line count limit to logical lines.
  
      --max-line-count=MAX_LINE_COUNT
             Changes the maximum limit for live code line count.
                          
      --live-code-count
	         Displays the number of physical and logical lines containing live code.
							
      --lineleak-ignore
	         Specifies a comma separated list of paths of files which leakline must ignore.
                        

Codes
-----
* ``LLW404`` Reports that logical line count has exceeded limit
* ``LLW405`` Reports that physical line count has exceeded specified limit
* ``LLI200`` Informs about the number of logical and physical lines containing live code.

Illustration
------------
a. Overriding default line count limit (limit -> 100)::

    $ flake8 --max-line-count=50 testfile.py
    testfile.py:82:1: LLW405 Maximum number of physical live code lines (50) exceeded.

b. Imposing limit on logical, instead of physical, lines::

    $ flake8 --max-line-count=50 --lineleak-logical testfile.py
    testfile.py:103:1: LLW404 Maximum number of logical live code lines (50) exceeded.

c. Display just the number of lines containing live code::

    $ flake8 --live-code-count testfile.py
    testfile.py:118:1: LLI200 [INFO] Live code count: 56 logical and 79 physical lines
	
d. Ignore file(s) by specifying a comma separated list of their file paths.

   Results using lineleak-ignore::
   
    $ flake8 --max-line-count=5 --filename=*.py --lineleak-ignore=.\lineleak.py,.\subber.py
    .\lineleak0.9.9.py:19:1: LLW405 Maximum number of physical live code lines (5) exceeded.
    .\setup.py:10:1: LLW405 Maximum number of physical live code lines (5) exceeded.
   
   Results without lineleak-ignore::
   
    $ flake8 --max-line-count=5 --filename=*.py
    .\lineleak.py:19:1: LLW405 Maximum number of physical live code lines (5) exceeded.
    .\lineleak0.9.9.py:19:1: LLW405 Maximum number of physical live code lines (5) exceeded.
    .\setup.py:10:1: LLW405 Maximum number of physical live code lines (5) exceeded.
    .\subber.py:10:1: LLW405 Maximum number of physical live code lines (5) exceeded.
	
e. Ignore limit enforcement.

   In adherence with flake8 design principles, lineleak can be silenced by adding the 
   appropriate error codes of lineleak to the ignore list::
   
    $ flake8 --ignore=LL testfile.py
    $


Installation
------------
Install using pip::

    pip install flake8-leakline
	

Dependencies & Compatibility
----------------------------
* Requires ``flake8 >= 3.3``
* Requires ``python >= 3.4``

	
Environment
-----------
* Shell

Software Cycle Stage
--------------------
* Development - Alpha

