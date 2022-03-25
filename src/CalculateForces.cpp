//
//  CalculateForces.cpp
//  NeuralCrest
//
//  Created by Christopher Revell on 28/11/2018.
//
//

#include "CalculateForces.hpp"
#include "cell.hpp"
#include <vector>
#include <armadillo>
#include "MorseForce.hpp"
#include "parameters.hpp"
#include <math.h>

using namespace std;
using namespace arma;

// Calculate nearest neighbour forces between cells. A combination of volume exclusion and coattraction.
void CalculateForces(vector<cell>& Cells,parameters& params, const float& gamma){

  vec dx = vec(2,fill::zeros);
  float distance_cells_a_b;
  float distance_threshold;

  for (int i=0; i<params.Nc; i++){
    // Loop over all cells
    cell& cella = Cells[i];
    float& De = cella.De;
    float& a = cella.a;
    for (int j=0; j<Cells[i].Nneighbours; j++){
      // Loop over all neighbours of a given cell

      cell& cellb = Cells[Cells[i].neighbours[j]];
      // Find separation distance of neighbours
      dx = cella.pos-cellb.pos;

      // Calculate the euclidean distance between two cells
      distance_cells_a_b = sqrt( pow(cella.pos(1) - cellb.pos(1),2) + pow(cella.pos(0) - cellb.pos(0),2) );
      distance_threshold = cella.interactionThreshold * params.cellradius;


            // Increment number of neighbours within threshold distance
      cella.withinThresholdNeighbours = cella.withinThresholdNeighbours + 1;

      if (cella.pos(1) + params.PMZwidth/2.0 < 0 || cella.pos(1) - params.PMZwidth/2.0 > 0 || cellb.pos(1) + params.PMZwidth/2.0 < 0 || cellb.pos(1) - params.PMZwidth/2.0 > 0)
        {

        // If one of the cells is in the buffer zone, apply a distance threshold to the interaction.
          if (cella.pos(0) > params.PMZheight/2.0){}
          else{MorseForce(cella,cellb,De,a,gamma);}
        }
      else
        {
          // Local interactions between neighbours modelled with morse potential
          MorseForce(cella,cellb,De,a,gamma);
        }

      // if(distance_cells_a_b < distance_threshold)
      // {

      //   // Increment number of neighbours within threshold distance
      //   cella.withinThresholdNeighbours = cella.withinThresholdNeighbours + 1;

      //   if (cella.pos(1) + params.PMZwidth/2.0 < 0 || cella.pos(1) - params.PMZwidth/2.0 > 0 || cellb.pos(1) + params.PMZwidth/2.0 < 0 || cellb.pos(1) - params.PMZwidth/2.0 > 0)
      //     {

      //     // If one of the cells is in the buffer zone, apply a distance threshold to the interaction.
      //       if (cella.pos(0) > params.PMZheight/2.0){}
      //       else{MorseForce(cella,cellb,De,a,gamma);}
      //     }
      //   else
      //     {
      //       // Local interactions between neighbours modelled with morse potential
      //       MorseForce(cella,cellb,De,a,gamma);
      //     }
      // }
    }
  }
}
