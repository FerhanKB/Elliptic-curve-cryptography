# y^2 = x^3 + ax + b
a = 1
b = 6
# Finite Field
p = 751
# base point
x0 = 2
y0 = 7

def modInverse(a, m):
	a = a % m
	for x in range(1, m):
		if ((a * x) % m == 1):
			return x
	return 1

def curvePointAddition(x1,y1,x2,y2):
  l = 0
  if x1 == x2 and y1 == y2:
    l = (( ( 3 * ( x1 * x1 ) ) + a ) * modInverse(2 * y1,p)) % p
  else:
    l = ((y2 - y1) * modInverse(x2 - x1,p)) % p

  x3 = (l*l - x1 - x2) % p
  y3 = (l*(x1 - x3) - y1) % p

  return x3,y3

def multiplyKPvtk(x,y,k):
  x4 = x
  y4 = y
  newX = 0
  newY = 0
  for i in range(k-1):
    if i == 0:
      newX, newY = curvePointAddition(x,y,x4,y4)
      # print(i+2,'P: ','(',newX,',',newY,')')
    else:
      newX, newY = curvePointAddition(x,y,newX,newY)
      # print(i+2,'P: ','(',newX,',',newY,')')

  return newX,newY

def encryptionECC(M,k,publicKey):
  C1 = multiplyKPvtk(x0,y0,k)
  x, y = multiplyKPvtk(publicKey[0],publicKey[1],k)
  C2 = curvePointAddition(x,y,M[0],M[1])
  return C1,C2

def decryptionECC(C1,C2,k):
  DX , DY = multiplyKPvtk(C1[0],C1[1],k)
  DY = DY * -1
  M = curvePointAddition(C2[0],C2[1],DX,DY)
  return M

def generatePublicKey(privateK):
  publicKx,publicKy = multiplyKPvtk(x0, y0, privateK)
  return (publicKx,publicKy)
