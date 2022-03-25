//
//  MorseForce.cpp
//  NeuralCrest
//
//  Created by Christopher Revell on 04/10/2019.
//
//

#include "MorseForce.hpp"
#include <armadillo>
#include <cmath>

using namespace std;
using namespace arma;

// Subroutine to calculate the force exerted by the Morse potential between two given cells.
// Equilibrium radius for interaction between cells increases with age of both cells assuming linear growth of cell volume and corresponding increase in typical radius.
void MorseForce(cell& Cell1,cell& Cell2,const float& De,const float& a, const float& gamma){

  vec dx = vec(2,fill::zeros);
  vec v  = vec(2,fill::zeros);
  vec F  = vec(2,fill::zeros);
  float r,dif,dif1;

  dx = Cell1.pos - Cell2.pos;
  r = sqrt(dot(dx,dx));
  dif = (r-Cell1.cellradius-Cell2.cellradius);
  dif1 = Cell1.k*dif/(Cell1.k+Cell2.k);

  F = dx*2.0*Cell1.De*Cell1.a*(exp(-Cell1.a*dif1)-exp(-2.0*Cell1.a*dif1))/r;

  // Calculate velocity components from force.
  // Overdamped Langevin => velocity = force/drag factor
  v = F/gamma;
  // Velocity components from forces between different cells sum linearly
  Cell1.v = Cell1.v-v;
  Cell2.v = Cell2.v+v;

  // Add magnitude of force to their morseForseMag variables
  Cell1.morseForceMag = sqrt(pow(v(0),2) + pow(v(1),2));
  Cell2.morseForceMag = sqrt(pow(v(0),2) + pow(v(1),2));



}
