#!/bin/env python3
import sys

def C(n,p):
  if (p==0 or n==p):
    return 1
  else:
    return C(n-1,p)+C(n-1,p-1)

def main():
  if len(sys.argv)!=3:
    print("2 arguments sont requis !")
    exit(1)
  n = int(sys.argv[1])
  p = int(sys.argv[2])
  if p<=n and n>=0 and p>=0:
    print(f"C({n},{p})={C(n,p)}")
  else:
    print("les arguments sont hors limite !")  

