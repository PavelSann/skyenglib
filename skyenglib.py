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
	result: typing.List[elementType]=[]
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

class Translation(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self, data):
		self.text=None
		self.note=None
		Result.__init__(self,data)
		if self.note is None:
			self.note=""
		
	def __str__(self):
		return self.text+" "+self.note
		
class Example(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self, data):
		self.text=None
		self.soundUrl=None
		Result.__init__(self,data)


class Image(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self, data):
		self.url=None
		Result.__init__(self,data)
		
class Definition(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self, data):
		self.text=None
		self.soundUrl=None
		Result.__init__(self,data)


class AlternativeTranslation(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self, data):
		self.text=None
		Result.__init__(self,data)
		self.translation=Translation(data['translation'])

class MeaningWithSimilarTranslation(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self, data):
		self.meaningId=None
		self.frequencyPercent=None
		self.partOfSpeechAbbreviation=None
		self.partOfSpeechAbbreviation=None
		Result.__init__(self,data)
		self.translation=Translation(data['translation'])

class Meaning(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self,data):
		self.id=None
		self.wordId=None
		self.difficultyLevel=None
		self.partOfSpeechCode=None
		self.prefix=None
		self.text=None
		self.soundUrl=None
		self.transcription=None
		self.properties:dict =data['properties']
		self.updatedAt=None
		self.mnemonics=None
		self.examples=None
		
		Result.__init__(self,data)
		self.partOfSpeech=PartType(data['partOfSpeechCode'])
		self.images=obj_list(data['images'],Image)
		self.translation=Translation(data['translation'])
		self.definition=Definition(data['definition'])
		self.alternativeTranslations=obj_list(data['alternativeTranslations'],AlternativeTranslation)
		self.examples=obj_list(data['examples'],Example)
		self.meaningsWithSimilarTranslation=obj_list(data['meaningsWithSimilarTranslation'],MeaningWithSimilarTranslation)

class MeaningShort(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self,data):
		self.id=None
		self.partOfSpeechCode=None
		self.previewUrl=None
		self.imageUrl=None
		self.soundUrl=None
		self.transcription=None
		Result.__init__(self,data)
		self.translation=Translation(data['translation'])
		self.partOfSpeech=PartType(data['partOfSpeechCode'])



class Word(Result):
	'https://dictionary.skyeng.ru/doc/api/external'
	def __init__(self, data):
		self.id=None
		self.text=None
		Result.__init__(self,data)
		self.meanings:typing.List[MeaningShort]=obj_list(data['meanings'],MeaningShort)
	

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
	def searchWords(word,page=1,pageSize=100)-> typing.List[Word]:
		jsonData= SkyengLib.req('dictionary',f'public/v1/words/search?search={word}&page={page!s}&pageSize={pageSize!s}')
		return obj_list(jsonData,Word)	
	
	@staticmethod
	def getMeanings(ids)-> typing.List[Meaning]:
		'ids - An array of meaning ids. Separated by a comma'
		jsonData= SkyengLib.req('dictionary',f'public/v1/meanings?ids={ids}')
		return obj_list(jsonData,Meaning)	
	
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


	
		
