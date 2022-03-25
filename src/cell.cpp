//
//  cell.cpp
//  NeuralCrest
//
//  Created by Christopher Revell on 19/11/2018.
//
//

#include "cell.hpp"
#include <armadillo>

using namespace std;
using namespace arma;

cell::cell(const int& celllabel,const float& initialx,const float& initialy,const float& radius, const int& typespecifier, const float& stiffness, const float& attractiveness,const float& vauto,const float& cellInteractionThreshold, const float& follower_gradientSensitivity){
  pos                   = vec(2,fill::zeros);
  v                     = vec(2,fill::zeros);
  v_auto                = vec(2,fill::zeros);
  v_bound               = vec(2,fill::zeros);
  neighbours            = Col<int>(24,fill::zeros);
  cellradius            = radius;
  pos(0)                = initialx; // TODO: this is actually y
  pos(1)                = initialy; // TODO: this is actually x
  label                 = celllabel;
  type                  = typespecifier;
  Nneighbours           = 0;
  k                     = stiffness;
  De                    = attractiveness;
  a                     = sqrt(k/(2*De));
  autonomousMag         = vauto;
  interactionThreshold  = cellInteractionThreshold;
  gradientSensitivity = follower_gradientSensitivity;

  dll4 = 0.99; //internal delta-like4 level
  notch = 0.99; //internal activated notch level
}

cell::~cell() {}
