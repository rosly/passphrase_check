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

def crackability(combinations, suffix):
   seconds = operator.truediv(combinations, 23012000000) #magic number is hashrate of 8 Nvidia 1080 for sha256
   if seconds < 60:
      print 'crackable in %d seconds %s' % (seconds, suffix)
   elif seconds / 60 < 60:
      print 'crackable in %d minutes %s' % (seconds/60, suffix)
   elif seconds / 3600 < 24:
      print 'crackable in %d hours %s' % (seconds/3600, suffix)
   elif seconds / (3600 * 24) < 365:
      print 'crackable in %d days %s' % (seconds / (3600 * 24), suffix)
   else:
      print 'crackable in %d years %s' % (seconds / (3600 * 24 * 365), suffix)

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

   print 'Generating freqs ...'
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

   score = {}
   for word in words:
      seq = (word[1], freq[word[1]])
      score[word[0]] = seq

#print score

   print 'Enter each word from your password, one at the time with proper spelling (important)'
   print 'Example:\n> chrząszcz\n> przebrzydły\n> moczymorda'
   print 'Enter empty line to reset calculations'
   set_size = 1
   word_cnt = 0
   pass_len = 0
   cssize = 0
   while True:
      print '\n> ',
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
      if word not in score:
         print 'Your word seems to be uncomon or misspelled, cannot find the score (password uncracable? check haveibeenpwned)'
         print 'Assuming whole word set as crack set, %d words' % len(score)
         set_size = max(set_size, len(score))
      else:
         hit = score[word]
         set_size = max(set_size, hit[1])
         print '\"%s\" rank #%d used %d times, minimal word set size %d' % (word,hit[1],hit[0],set_size)
         
      word_perm = pow(set_size, word_cnt)
      cssize = max(1, max(cssize, charset_size(word)))
      brute_perm = pow(cssize, pass_len)
      
      print '%d word password entropy %f bits' % (word_cnt, math.log(float(word_perm),2))
      print '%d letters bruteforce password entropy %f bits' % (pass_len, math.log(float(brute_perm),2))
      crackability(word_perm, 'by word rule based method')
      crackability(brute_perm, 'by %d charset bruteforce method' % cssize)

if __name__ == "__main__":
   main(sys.argv[1:])
