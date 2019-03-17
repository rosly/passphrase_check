# Phrase password checker

This simple phrase password checker allows you to estimate the entropy of your
password.

# Idea

The idea behind this tool is that new password recommendations starting to
suggest that old rules that force user to use set of characters and certain
length in password, creates password that are hard to remember and easy to
crack. 

Those recommendations suggest to just use long password like in form of several
words connected together. The idea behind this is that such password is easy to
remember and hard to crack.

The cracking resistance comes from much bigger key space. Lest calculate:

8 character password with base set of [a-z][A-Z][0-9][_?!@#$%^&*()]:

Entropy = 78^8 = 1.3e15

Password made from 5 words (lets assume 5000 word set)

Entropy = 5000^5 = 3.1e18

But there is a caveat in those calculations. We assumed that all words came
certain set, which in real life does not have to be true. User have the tendency
to use common words which create much smaller set.

With smaller word set the entropy drastically drops. And that's why it is important
to verify how common are words used in your password.

Some may disagree that using "leetspeek" or mixing capital letters make small word
set attack impractical but in fact, using those tricks only increase the set by
factor of tenth. Such word mixing can be easily predicted and covered by
dictionary + ruleset attach in common cracking tools like hashcat.

# Usage

Just start the tool with "python pass_check.py" and give your words one by one
pytting attention to proper spelling.
In future some mechanism for fixing spelling and "letsspeek" demangling is planed
to be implemented.

# Languages

Currently only Polish language is supported. But any language can be added just
by importing frequency word list database.

