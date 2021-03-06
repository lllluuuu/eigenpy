from geometry import *
import numpy as np
from numpy import cos,sin

verbose = False

def isapprox(a,b,epsilon=1e-6):
    if issubclass(a.__class__,np.ndarray) and issubclass(b.__class__,np.ndarray):
        return np.allclose(a,b,epsilon)
    else:
        return abs(a-b)<epsilon

# --- Quaternion ---------------------------------------------------------------
q = Quaternion(1,2,3,4)
q.normalize()
assert(isapprox(np.linalg.norm(q.coeffs()),q.norm()))
assert(isapprox(np.linalg.norm(q.coeffs()),1))

r = AngleAxis(q)
q2 = Quaternion(r)
assert(q==q2)
assert(isapprox(q.coeffs(),q2.coeffs()))

Rq = q.matrix()
Rr = r.matrix()
assert(isapprox(Rq*Rq.T,np.eye(3)))
assert(isapprox(Rr,Rq))

qR = Quaternion(Rr)
assert(q==qR)
assert(isapprox(q.coeffs(),qR.coeffs()))

assert(isapprox(qR[3],1./np.sqrt(30)))
try:
   qR[5]
   print "Error, this message should not appear."
except Exception,e:
  if verbose: print "As expected, catched exception: ",e.message

# --- Angle Vector ------------------------------------------------
r = AngleAxis(.1,np.array([1,0,0],np.double))
if verbose: print "Rx(.1) = \n\n",r.matrix(),"\n"
assert( isapprox(r.matrix()[2,2],cos(r.angle)))
assert( isapprox(r.axis,np.matrix("1;0;0")) )
assert( isapprox(r.angle,0.1) )

r.axis = np.array([0,1,0],np.double)
assert( isapprox(r.matrix()[0,0],cos(r.angle)))

ri = r.inverse()
assert( isapprox(ri.angle,-.1) )

R = r.matrix()
r2 = AngleAxis(np.dot(R,R))
assert( isapprox(r2.angle,r.angle*2) )

# --- USER FUNCTIONS -----------------------------------------------------------
ro = testOutAngleAxis()
assert(ro.__class__ == AngleAxis)
res = testInAngleAxis(r)
assert( res==r.angle )

qo = testOutQuaternion()
assert(qo.__class__ == Quaternion)
res = testInQuaternion_fx(q)
assert(q.norm() == res)
try:
    testInQuaternion(q)
    print "Error, this message should not appear."
except:
    if verbose: print "As expected, catch a Boost::python::ArgError exception."
