#!/usr/bin/python3
import sys
import skyenglib
from skyenglib import SkyengLib

scriptName=sys.argv[0]
cmd=sys.argv[1]
args=sys.argv[2:]
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
	words=SkyengLib.searchInDictionary(args[0],1,10)
	for ww in words:
		w:skyenglib.Word=ww
		#print(w.text)
		for mm in w.meanings:
			m:skyenglib.Meaning=mm
			print(" "+m.partOfSpeech.name+"		"+w.text+"["+m.transcription+"] "+m.translationText+" "+m.translationNote)

actions['word']=actionWord

def actionHelp(args):
	'Show this guidebook'
	print(f'usage: {scriptName} [action] [args]')
	print("Actions:")
	for k in actions.keys():
		doc=actions[k].__doc__
		print(f'	{k}:	{doc}')
actions['help']=actionHelp
	

if len(cmd)>0:
	try:
		action=actions[cmd]
	except KeyError:
		action=actionHelp
	action(args)
	




