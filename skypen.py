#!/usr/bin/python3
import sys
import skyenglib

from skyenglib import SkyengLib

cmd=sys.argv[1]
args=sys.argv[2:]

if cmd == 'test':
	if(not SkyengLib.testConnect()):
		print("Bad connection")
	else: 
		print("Good connection")

if cmd == 'word':
	words=SkyengLib.searchInDictionary(args[0])
	for ww in words:
		w:skyenglib.Word=ww
		print(w.text)
		for mm in w.meanings:
			m:skyenglib.Meaning=mm
			print("		"+m.partOfSpeech.name+" "+m.translationText+"["+m.transcription+"]")
			if not m.translationNote==None:
				print("		"+m.translationNote)



