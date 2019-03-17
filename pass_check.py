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

#print 'Loading freqs'
#freq = {}
#with open('wordlist_count_freq.txt', 'r') as f:
#   for line in f:
#      pair = eval(line.strip())
#      freq[pair[0]] = pair[1]

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

print 'Enter each word from your password, one at the time'
cumpos = 1
while True:
   word = sys.stdin.readline().strip()
   if word == '':
      cumpos = 1
      print 'Reseting calculations. Clean start'
      continue
   if word not in score:
      print 'Your word seems to be uncomon, cannot find the score (password uncracable? check haveibeenpwned)'
   else:
      hit = score[word]
      cumpos *= hit[1]
      print '\"%s\" is used %d times on place %d, cumulative pos %d' % (word,hit[0],hit[1],cumpos)
      print 'password entropy %f bits' % (math.log(float(cumpos),2))
      seconds = operator.truediv(cumpos,23012000000)
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
         

   
