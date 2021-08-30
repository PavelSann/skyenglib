#!/usr/bin/python3
import sys
import subprocess
import skyenglib
import argparse
from utils import baseDecode, baseEncode,BASE62
from skyenglib import SkyengLib

def playSoundUrl(soundUrl):
	cmd=f"curl -s 'https:{soundUrl}' |ffplay -i pipe:0 -hide_banner -showmode 0 -autoexit"
	subprocess.call([cmd],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL,shell=True)

def actionWord(args):
	'Search word in the dictionary'
	words=SkyengLib.searchWords(args.word,1,args.limit)
	for ww in words:
		w:skyenglib.Word=ww
		print(w.text)
		for ms in w.meanings:
			m:skyenglib.MeaningShort=ms
			mUid=baseEncode(BASE62,m.id)
			print(f" [@{mUid}]  \t"+m.partOfSpeech.name+" \t"+w.text+"["+m.transcription+"] "+str(m.translation))
			if args.play_sound or args.play_all_sound:
				playSoundUrl(m.soundUrl)
		

def actionMeaning(args):
	'Return the meaning of the word by the id of the meaning'
	if(args.word[0]=='@'):
		mUid=baseDecode(BASE62,args.word[1:])
	else:
		return
	meanings=SkyengLib.getMeanings(mUid)
	for mm in meanings:
		m:skyenglib.Meaning=mm
		mUid=baseEncode(BASE62,int(m.id))
		print(f" [@{mUid}]  \t"+m.partOfSpeech.name+"		"+m.text+"["+m.transcription+"] "+str(m.translation))
		print(" "+m.definition.text)
		if args.play_sound or args.play_all_sound:
			playSoundUrl(m.soundUrl)

		#print("Other transtations:")
		#for at in m.alternativeTranslations:
			#a:skyenglib.AlternativeTranslation=at
			#print("  "+a.text+" "+str(a.translation))
		#print(" Other meanings:")
		#for smt in m.meaningsWithSimilarTranslation:
			#sm:skyenglib.MeaningWithSimilarTranslation=smt
			#print("  "+sm.frequencyPercent+" "+str(sm.translation))
		print(" Examples:")
		for ee in m.examples:
			e:skyenglib.Example()=ee
			print("  "+e.text)
			if args.play_all_sound:
				playSoundUrl(e.soundUrl)
			

	

argp=argparse.ArgumentParser(description="jhjh")
argp.add_argument("word",type=str,help="The word")

argp.add_argument("--limit","-l", type=int,default=5,help="Limit of the words")
argp.add_argument("--play_sound","-p", action="store_true",help="Play sounds")
argp.add_argument("--play_all_sound","-P", action="store_true",help="Play all sounds")
args=argp.parse_args();


if(args.word[0]=='@'):
	actionMeaning(args)
else:
	actionWord(args)








