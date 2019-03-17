#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import math
import operator
import os  
import signal
import random
import sys, getopt

def signal_handler(sig, frame):
        print('SIGINT ... exiting')
        sys.exit(0)

def main(argv):

   freq_list_url = 'https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018'
   lang = 'pl'

   try:
      opts, args = getopt.getopt(argv,"l:",["lang="])
   except getopt.GetoptError:
      print './pass_check.py [-l LANG_CODE]'
      sys.exit(2)
   for opt, argval in opts:
      if opt in ("-l", "--lang="):
         print 'Got lang %s' % argval
         lang = argval
      else:
         print './pass_check.py [-l LANG_CODE]'
         sys.exit(2)

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
   print 'Example:\n> chrząszcz\n> brzebrzydły\n> moczymorda'
   print 'Enter empty line to reset calculations'
   set_size = 1
   word_cnt = 0
   pass_len = 0
   while True:
      print '\n> ',
      word = sys.stdin.readline().strip()
      if word == '':
         set_size = 1
         word_cnt = 0
         pass_len = 0
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
      brute_perm = pow(26, pass_len)
      
      print '%d word password entropy %f bits' % (word_cnt, math.log(float(word_perm),2))
      print '%d letters bruteforce password entropy %f bits' % (pass_len, math.log(float(brute_perm),2))
      seconds = operator.truediv(min(word_perm, brute_perm),23012000000) #magic number is hashrate of 8 Nvidia 1080 for sha256
      if seconds < 60:
         print 'crackable in %d seconds' % seconds
      elif seconds / 60 < 60:
         print 'crackable in %d minutes' % (seconds/60)
      elif seconds / 3600 < 24:
         print 'crackable in %d hours' % (seconds/3600)
      elif seconds / (3600 * 24) < 365:
         print 'crackable in %d days' % (seconds / (3600 * 24))
      else: 
         print 'crackable in %d years' % (seconds / (3600 * 24 * 365))

if __name__ == "__main__":
   main(sys.argv[1:])
