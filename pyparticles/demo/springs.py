# PyParticles : Particles simulation in python
# Copyright (C) 2012  Simone Riva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import pyparticles.pset.particles_set as ps

import pyparticles.forces.linear_spring as ls
import pyparticles.forces.const_force as cf
import pyparticles.forces.multiple_force as mf
import pyparticles.forces.drag as dr 

import pyparticles.pset.rebound_boundary as rb

import pyparticles.measures.elastic_potential_energy as epe
import pyparticles.measures.kinetic_energy as ke



import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.stormer_verlet_solver as svs
import pyparticles.ode.midpoint_solver as mds

import sys

if sys.version_info[0] == 2:
    import pyparticles.animation.animated_ogl as aogl


def springs() :
    
    dt = 0.02
    steps = 1000000
    
    G = 0.5

    pset = ps.ParticlesSet( 3 , 3 , label=True )
    
    pset.label[0] = "1"
    pset.label[1] = "2"
    pset.label[2] = "3"
    
    pset.X[:] = np.array(  [
                            [  2.0 ,  4.0  , 1.0 ],    # 1
                            [ -2.0 , -2.0  , 1.0 ],    # 2
                            [  3.0 , -3.0 ,  2.0 ]     # 3
                            ] )

    pset.M[:] = np.array(  [
                            [  1.0 ] ,
                            [  1.0 ] ,
                            [  1.5 ]
                            ] )

    pset.V[:] = np.array( [ [ 0. , 0. , 0.] ,
                            [ 0. , 0  , 0.] ,
                            [ 0. , 0  , 0.]
                            ] )
                    
    
    springs = ls.LinearSpring( pset.size , Consts=G )
    constf  = cf.ConstForce( pset.size , u_force=[ 0,0,-1.5 ] )
    drag = dr.Drag( pset.size , Consts=0.2 )
    
    mlf = mf.MultipleForce( pset.size , 3 )
    
    mlf.append_force( springs )
    mlf.append_force( constf )
    #mlf.append_force( drag )
    
    #pot = epe.ElasticPotentialEnergy( pset , springs )
    #ken = ke.KineticEnergy( pset , springs )
    #
    #pot.update_measure()
    #ken.update_measure()
    #
    #print( "Potential = %f " % pot.value() )
    #print( "Kinetic = %f " % ken.value() )
    
    bound = rb.ReboundBoundary( bound=(-10,10) )
    pset.set_boundary( bound )
    
    mlf.set_masses( pset.M )
    springs.set_masses( pset.M )
    
    #springs.update_force( pset )
    mlf.update_force( pset )
    
    #solver = rks.RungeKuttaSolver( springs , pset , dt )
    solver = rks.RungeKuttaSolver( mlf , pset , dt )
    
    pset.enable_log( True , log_max_size=1000 )
    
    
    a = aogl.AnimatedGl()
    
    a.trajectory = True
    a.trajectory_step = 1
    
    a.ode_solver = solver
    a.pset = pset
    a.steps = steps
    
    a.build_animation()
    
    a.start()
    
    return 