#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import math
import operator
import os  
import signal
import random
import string
import sys, getopt

def signal_handler(sig, frame):
        print('SIGINT ... exiting')
        sys.exit(0)

def crackability(combinations, speed):
   seconds = operator.truediv(combinations, speed)
   if seconds < 60:
      return '%d seconds' % (seconds)
   elif seconds / 60 < 60:
      return '%d minutess' % (seconds/60)
   elif seconds / 3600 < 24:
      return '%d hours' % (seconds/3600)
   elif seconds / (3600 * 24) < 365:
      return '%d days' % (seconds / (3600 * 24))
   else:
      return '%d years' % (seconds / (3600 * 24 * 365))

def cracktime(combinations):
   # crack speeds taken from https://gist.github.com/epixoip/a83d38f412b4737e99bbef804a270c40
   print 'SHA1            in %s' % crackability(combinations, 68771000000)
   print 'SHA256          in %s' % crackability(combinations, 8408000000)
   print 'PBKDF2-HMAC-MD5 in %s' % crackability(combinations, 59296000)
   print 'scrypt          in %s' % crackability(combinations, 3493000)
   print 'WPA/WPA2        in %s' % crackability(combinations, 3177000)

def charset_size(passphrase):
   special = ['_', '?', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ' ']
   lowercase = set(string.ascii_lowercase)
   uppercase = set(string.ascii_uppercase)
   digits = set(string.digits)
   charset_size = 0
   for c in passphrase:
      if c in special:
         charset_size += len(special)
         break
   for c in passphrase:
      if c in lowercase:
         charset_size += len(lowercase)
         break
   for c in passphrase:
      if c in uppercase:
         charset_size += len(uppercase)
         break
   for c in passphrase:
      if c in digits:
         charset_size += len(digits)
         break
   return charset_size

def usage():
   print './pass_check.py [-l LANG_CODE]'

def main(argv):

   freq_list_url = 'https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018'
   lang = ''

   try:
      opts, args = getopt.getopt(argv,"l:",["lang="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)
   for opt, argval in opts:
      if opt in ("-l", "--lang="):
         print 'Got lang %s' % argval
         lang = argval
      else:
         usage()
         sys.exit(2)

   if lang == '':
      usage()
      sys.exit(2);
   freq_list_file = '%s_full.txt' % lang

   if not os.path.exists(freq_list_file):
      print 'Downloading word frequency list ...'
      os.system('wget %s/%s/%s' % (freq_list_url, lang, freq_list_file)) #do you often run python script without review?

   signal.signal(signal.SIGINT, signal_handler)

   print 'Loading words (this can take a while) ...'
   words = [] #list
   words_filter= {}
   with open(freq_list_file, 'r') as f:
      for line in f:
         try:
            subs = line.strip().split(' ')
            if subs[0] not in words_filter:
               words.append((subs[0], int(subs[1])))
               words_filter[subs[0]] = 1
         except ValueError:
            continue #ignoring lines with headers and comments

   print '%d words loaded' % len(words)

   print 'Generating commonness ranks ...'
   pos = 0
   cum = 1
   prev_count = 0
   freq = {}
   for word in words:
      count = word[1]
      if (prev_count != count):
         pos += cum
         cum = 1
      else:
         cum += 1
      freq[count] = pos

#print freq

   crank = {}
   for word in words:
      crank[word[0]] = (word[1], freq[word[1]])

#print crank

   print 'Enter each word from your password, one at the time with proper spelling (important)'
   print 'Example:\n> chrząszcz\n> przebrzydły\n> moczymorda'
   print 'Enter empty line to reset calculations\n'
   set_size = 1
   word_cnt = 0
   pass_len = 0
   cssize = 0
   while True:
      print '> ',
      word = sys.stdin.readline().strip()
      if word == '':
         set_size = 1
         word_cnt = 0
         pass_len = 0
         cssize = 0
         print 'Reseting calculations. Clean start'
         continue

      word_cnt += 1
      pass_len += len(word)
      if word not in crank:
         print 'Your word seems to be uncomon or misspelled, cannot find it in dictionary (password uncracable? check haveibeenpwned.com)'
         print 'Assuming whole dictionary for cracking with dict + rules, %d words' % len(crank)
         set_size = max(set_size, len(crank))
      else:
         hit = crank[word]
         set_size = max(set_size, hit[1])
         print '\"%s\" commonness #%d used %d times' % (word,hit[1],hit[0])
         
      word_perm = pow(set_size, word_cnt)
      cssize = max(1, max(cssize, charset_size(word)))
      brute_perm = pow(cssize, pass_len)
      
      print '\n%d word password based entropy %f bits, minimal dictionary size %d' % (word_cnt, math.log(float(word_perm),2), set_size)
      print 'dictionaty + rules method crack times:'
      cracktime(word_perm)
#print '\n%d letters with %d charset password based entropy %f bits' % (pass_len, cssize, math.log(float(brute_perm),2))
#print 'bruteforce crack times:'
#cracktime(brute_perm)

      print '\n\nType next word or just enter to reset estimations'

if __name__ == "__main__":
   main(sys.argv[1:])
