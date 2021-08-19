#!/usr/bin/python3
import sys
import skyenglib
#import argparse
from skyenglib import SkyengLib

actions={}

def actionTest(args):
	'Test connection from skyeng API'
	if(not SkyengLib.testConnect()):
		print("Bad connection")
	else: 
		print("Good connection")
		
actions['test']=actionTest

def actionWord(args):
	'Search word in the dictionary'
	words=SkyengLib.searchWords(args[0],1,10)
	for ww in words:
		w:skyenglib.Word=ww
		#print(w.text)
		for ms in w.meanings:
			m:skyenglib.MeaningShort=ms
			print(" "+m.partOfSpeech.name+"		"+w.text+"["+m.transcription+"] "+str(m.translation)+f"		({m.id})")
		

actions['word']=actionWord

def actionMeaning(args):
	'Return the meaning of the word by the id of the meaning'
	meanings=SkyengLib.getMeanings(args[0])
	for mm in meanings:
		m:skyenglib.Meaning=mm
		print(" "+m.partOfSpeech.name+"		"+m.text+"["+m.transcription+"] "+str(m.translation)+f"		({m.id})")
		print(" "+m.definition.text)
		#print("Other transtations:")
		#for at in m.alternativeTranslations:
			#a:skyenglib.AlternativeTranslation=at
			#print("  "+a.text+" "+str(a.translation))
		print(" Other meanings:")
		for smt in m.meaningsWithSimilarTranslation:
			sm:skyenglib.MeaningWithSimilarTranslation=smt
			print("  "+sm.frequencyPercent+" "+str(sm.translation))
		print(" Examples:")
		for ee in m.examples:
			e:skyenglib.Example()=ee
			print("  "+e.text)
			

actions['meaning']=actionMeaning

def actionHelp(args):
	'Show this guidebook'
	print(f'usage: {sys.argv[0]} [action] [args]')
	print("Actions:")
	for k in actions.keys():
		doc=actions[k].__doc__
		print(f'	{k}:	{doc}')
actions['help']=actionHelp
	
args=[]
action=actionHelp
#argp=argparse.ArgumentParser()
#argp.add_argument("test")
#argp.test

if len(sys.argv)>1:
	cmd=sys.argv[1]
	if len(sys.argv)>2:
		args=sys.argv[2:]
	if len(cmd)>0:
		try:
			action=actions[cmd]
		except KeyError:
			pass
		
action(args)




