#!/usr/bin/env python3

from math import floor

__author__ = "PavelSann"
__license__ = "GPL"
__email__ = "PawelSann@gmail.com"

if __name__ == '__main__':
	print('Это модуль для импорта')
	
BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
BASE36 = '0123456789abcdefghijklmnopqrstuvwxyz';

def baseDecode(base:str,val: str) -> int:
	bl=len(base)
	limit = len(val)
	res = 0
	for i in range(limit):
		res = bl * res + base.find(val[i])
	return res

def baseEncode(base:str,num: int) -> str:
	bl=len(base)
	if bl <= 0 or bl > 62:
		return 0
	r = num % bl
	res = base[r];
	q = floor(num / bl)
	while q:
		r = q % bl
		q = floor(q / bl)
		res = base[int(r)] + res
	return res
