#!/usr/bin/python3
import sys
import skyenglib
import argparse
from utils import baseDecode, baseEncode,BASE62
from skyenglib import SkyengLib




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
			

	

argp=argparse.ArgumentParser(description="jhjh")
argp.add_argument("word",type=str,help="The word")

argp.add_argument("--limit","-l", type=int,default=5,help="Limit of the words")
#argp.add_argument("--meaning","-m",help="Show a external information about meaning by a ID")
args=argp.parse_args();


if(args.word[0]=='@'):
	actionMeaning(args)
else:
	actionWord(args)








