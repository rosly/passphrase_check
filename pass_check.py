import sys
import math
import operator
import os  
import signal

def signal_handler(sig, frame):
        print('SIGINT ... exiting')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if not os.path.exists('frequency_list_orth.txt'):
   print 'Word list file not found. Extracting archive ...'
   os.system('7z e frequency_list_orth.7z') #do you often run python script without review?

print 'Loading words (this can take a while) ...'
words = [] #list
words_filter= {}
with open('frequency_list_orth.txt', 'r') as f:
   for line in f:
      try:
         subs = line.strip().split(';')
         if subs[2] not in words_filter:
            words.append((subs[2], int(subs[3])))
            words_filter[subs[2]] = 1
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
