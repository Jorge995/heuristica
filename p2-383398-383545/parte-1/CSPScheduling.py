from constraint import *

problem = Problem()

#Parte profesores
problem.addVariables(['J1', 'J2','L1', 'L2', 'A1','A2'], ['M', 'CN', 'CS', 'LL', 'I', 'EF'])

#Parte asignaturas
problem.addVariables(['CN1','CN2','LL1','LL2','I1','I2','EF'], ['Lun1', 'Lun2', 'Lun3', 'Mar1', 'Mar2','Mar3','Mier1','Mier2','Mier3','Jue1','Jue2'])
problem.addVariables(['M1','M2'], ['Lun1','Mar1','Mier1','Jue1'])
problem.addVariables(['CS1','CS2'], ['Lun3','Mar3','Mier3','Jue2'])
problem.addConstraint(AllDifferentConstraint(), ('J1', 'J2','L1', 'L2', 'A1','A2'))

def LuciayAndrea(a, b, c, d):
    if a=='EF' or c=='EF': 
        if b=='CS' or d=='CS':
            return True
        else: return False
    if b=='CS' or d=='CS':
        return False
    else: return True

problem.addConstraint(LuciayAndrea, ('A1', 'L1', 'A2', 'L2'))

problem.addConstraint(AllDifferentConstraint(), ('M1','M2','CN1','CN2','CS1','CS2','LL1','LL2','I1','I2','EF'))

def restriccion1(a,b):
  if a=='Lun2' or b=='Lun2':
    if a=='Lun1' or b=='Lun1' or a=='Lun3' or b=='Lun3':
      return True
    else: return False
  if a=='Mar2' or b=='Mar2':
    if a=='Mar1' or b=='Mar1' or a=='Mar3' or b=='Mar3':
      return True
    else: return False
  if a=='Mier2' or b=='Mier2':
    if a=='Mier1' or b=='Mier1' or a=='Mier3' or b=='Mier3':
      return True
    else: return False
  if a=='Jue1' or b=='Jue1':
    if a=='Jue2' or b=='Jue2':
      return True
    else: return False
  return False

problem.addConstraint(restriccion1,('CN1','CN2')) 

def restriccion2 (a, b, c ,d, e, f):
  if a=='Lun1' or b=='Lun1':
    if c=='Lun2' or c=='Lun3' or d=='Lun2' or d=='Lun3' or e=='Lun2' or e=='Lun3' or f=='Lun2' or f=='Lun3':
      return False
  if a=='Mar1' or b=='Mar1':
    if c=='Mar2' or c=='Mar3' or d=='Mar2' or d=='Mar3' or e=='Mar2' or e=='Mar3' or f=='Mar2' or f=='Mar3':
      return False
  if a=='Mier1' or b=='Mier1':
    if c=='Mier2' or c=='Mier3' or d=='Mier2' or d=='Mier3' or e=='Mier2' or e=='Mier3' or f=='Mier2' or f=='Mier3':
      return False
  if a=='Jue1' or b=='Jue1':
    if c=='Jue2' or d=='Jue2' or e=='Jue2' or f=='Jue2':
      return False
  return True
    
problem.addConstraint(restriccion2, ('M1','M2','CN1','CN2','I1','I2'))

def restriccion3(a,b,c,d):
  if a=='Lun1' or b=='Lun1' or a=='Jue1' or b=='Jue1':
    if c=='CN' or d=='CN':
      return False
    else: return True
  return True
  
problem.addConstraint(restriccion3, ('CN1','CN2','J1','J2'))

print(len(problem.getSolutions()))

  
  

