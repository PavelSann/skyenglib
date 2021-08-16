#!/usr/bin/python3
#https://vimbox.skyeng.ru/grammar/1
#https://grammar.skyeng.ru/api/v2/materials/1?withMistakes=true
#https://grammar.skyeng.ru/api/v2/materials/523?sectionTitle=&withMistakes=true&withMoreMaterialsFromSameNodes=true&withRelatedMaterials=true&withCharts=true&withVideos=tru
#https://grammar.skyeng.ru/api/v2/materials/spotlight?id=421
#https://grammar.skyeng.ru/api/v2/materials/spotlight?levels[]=2&search=gfff&withHighlights=true&pageSize=100
#https://grammar.skyeng.ru/api/v2/materials/spotlight?withHighlights=true&pageSize=100

#https://habr.com/ru/company/skyeng/blog/330456/
#https://words.skyeng.ru/api/doc/public
#https://dictionary.skyeng.ru/doc/api/external

import requests
import json
import dataclasses
import pickle 
import typing
from enum import Enum,unique


#import dataclasses_json
if __name__ == '__main__':
	print('Это модуль для импорта')

def obj_list(jsonArray,elementType)-> typing.List:
	result: List[elementType]=[]
	for r in jsonArray:
		e=elementType(r)
		result.append(e)
	return result

class SkyException(Exception):
	def __init__(self,status:int,msg: str):
		Exception.__init__(self)
		self.msg = msg
		self.status = status

@unique
class PartType(Enum):
	NOUN = 'n'
	VERB='v'
	ADJECTIVE='j'
	ADVERB='r'
	PREPOSITION='prp'
	PRONOUN='prn'
	CARDINAL_NUMBER='crd'
	CONJUNCTION='cjc'
	INTERJECTION='exc'
	ARTICLE='det'
	ABBREVIATION='abb'
	PARTICLE='x'
	ORDINAL_NUMBER='ord'
	MODAL_VERB='md'
	PHRASE='ph'
	IDIOM='phi'

class Result:
	def __init__(self,data):
		self.__dict__.update(data)

class Meaning(Result):
	def __init__(self,data):
		self.id=None
		self.partOfSpeechCode=None
		self.previewUrl=None
		self.imageUrl=None
		self.soundUrl=None
		self.transcription=None
		self.translationText=data['translation']['text']
		self.translationNote=data['translation']['note']
		if self.translationNote is None:
			self.translationNote=''
		self.partOfSpeech=PartType(data['partOfSpeechCode'])
		Result.__init__(self,data)

class Word(Result):
	def __init__(self, data):
		self.id=None
		self.text=None
		Result.__init__(self,data)
		self.meanings:typing.List[Meaning]=obj_list(data['meanings'],Meaning)
	

class SkyengLib:
	@staticmethod
	def req(module,path):
		r=requests.get(f'https://{module}.skyeng.ru/api/{path}')
		if r.status_code == 200:
			return json.loads(r.text)
		else:
			print(f'Error in query https://{module}.skyeng.ru/api/{path}')
			print(f'{r.status_code}	 {r.text}')
			raise SkyException(r.status_code,r.text)

	@staticmethod
	def testConnect():
		return not SkyengLib.req('dictionary','public/v1/words/search?search=test') == None

	@staticmethod
	def searchInDictionary(str,page=1,pageSize=100)-> typing.List[Word]:
		jsonData= SkyengLib.req('dictionary',f'public/v1/words/search?search={str}&page={page!s}&pageSize={pageSize!s}')
		return obj_list(jsonData,Word)	
	
	def __init__(self,email,token):
		"""Constructor"""
		self.email = email
		self.token = token
	



	def getMaterial(self,id):

		r=requests.get('https://grammar.skyeng.ru/api/v2/materials/{}?\
			withMistakes=true&withMoreMaterialsFromSameNodes=true&withRelatedMaterials=true&withCharts=true&withVideos=true'.format(id))
		if r.status_code == 200:
			return json.loads(r.text)
		else:
			return None


	
		
