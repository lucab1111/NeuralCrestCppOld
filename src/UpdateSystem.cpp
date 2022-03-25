//
//  UpdateSystem.cpp
//  NeuralCrestCpp
//
//  Created by Christopher Revell on 03/03/2020.
//
//

#include "UpdateSystem.hpp"
#include <vector>
#include "cell.hpp"
#include "parameters.hpp"
#include <armadillo>

using namespace std;
using namespace arma;

void UpdateSystem(vector<cell>& Cells, parameters& params, float& t){

  // Update all cell positions according to cell velocities and increment cell age
  for (int ii=0;ii<params.Nc;ii++){
    Cells[ii].pos = Cells[ii].pos+params.dt*Cells[ii].v;
    Cells[ii].v.zeros();
    Cells[ii].withinThresholdNeighbours = 0;
  }

  // Increment time
  t=t+params.dt;
}
