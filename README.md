# Passphrase entropy checker

This simple passphrase entropy checker allows you to estimate the entropy in
case your passphrase is created by conjuntion of several words.

# Idea

The idea behind this tool is to verify the real entropy of passphrase based on
several words stiched toghether. 

In the past companies followed NIST recomendations that force users to use set
of characters and certain length in password, which creates password that are
hard to remember and easy to crack. 

New NIST recommendations suggest to just use long password like in form of several
words connected together. The idea behind this is that such password is easy to
remember and hard to crack.

The cracking resistance comes from much bigger key space.

8 character password with base set of [a-z][A-Z][0-9][_?!@#$%^&*()]:

Key space = 78^8 = 1.3e15

Password made from 5 words (lets assume 5000 word set)

Key space = 5000^5 = 3.1e18

But there is a caveat in those calculations. We assumed that all words came from
certain set, which in real life does not have to be large as in our
calculations. Users have the tendency to use common words from much smaller set.
In that case the entropy drops dramaticly.  And that's why it is important to
verify how common are words used in your password. And that's why this tool is
handy.

Some may disagree that using "leetspeek" or mixing capital letters make small word
set attack impractical but in fact, using those tricks only increase the set by
factor of tenth. Such word mixing can be easily predicted and covered by
dictionary + ruleset attach in common cracking tools like hashcat.

# Usage

Just start the tool with "./pass_check.py" with your international language code
(like 'en' for english). Tool will download proper word frequency list. Than you
will be asked to give words which are elements of your password, one by one
pytting attention to proper spelling. This is important as tool does not
currently is not able to scan whole passphrase to look up for words so you need
to just gave those words with proper spelling.
In future some mechanism for automatic scanning, fixing spelling and "letsspeek"
demangling is planed to be implemented.

# Languages

Thanks to public Frequency Words database on CC license, you can use any
language of your choice. 

