//
//  Initialise.cpp
//  NeuralCrest
//
//  Created by Christopher Revell on 13/03/2019.
//
//

#include "Initialise.hpp"
#include <iostream>
#include <string>
#include "cell.hpp"
#include "parameters.hpp"
#include <random>
#include <cmath>

using namespace std;

// Set up initial arrangement of cells: at the start all cells are followers
void Initialise(vector<cell>& Cells,parameters& params){

  float posx,posy;
  // Number of cells specified at command line is the number per PMZ. Multiply by 3 so we have enough for the buffer on either side.
  params.Nc = 3*params.Nc;

  // Distribute cells between x (-PMZwidth, PMZwidth)
  // and y (-PMZheight, PMZheight)
  for (int i = 0; i < params.Nc; i++){
    if ( i % 2 == 0 )
    {
      posy = 0.5*params.PMZheight/2.0;
      posx = -params.PMZwidth + ((2*params.PMZwidth)/params.Nc)*i;
      Cells.push_back(cell(i,
        posy,
        posx,
        params.cellradius,
        0,
        params.follower_k,
        params.follower_De,
        params.follower_autonomousMag,
        params.follower_interactionThreshold,
        params.follower_gradientSensitivity));
    }


    else
    {
      posy = -0.5*params.PMZheight/2.0;
      posx = -params.PMZwidth + ((2*params.PMZwidth)/params.Nc)*i;
      Cells.push_back(cell(i,
        posy,
        posx,
        params.cellradius,
        0,
        params.follower_k,
        params.follower_De,
        params.follower_autonomousMag,
        params.follower_interactionThreshold,
        params.follower_gradientSensitivity));
    }

  }


}












