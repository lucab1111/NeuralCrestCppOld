//
//  IdentifyNeighbours.cpp
//  NeuralCrest
//
//  Created by <author> on 17/09/2019.
//
//

#include "IdentifyNeighbours.hpp"
#include "cell.hpp"
#include <vector>
#include <armadillo>


using namespace std;
using namespace arma;

void IdentifyNeighbours(vector<cell>& Cells,const std::vector<unsigned long>& triangles,const int& Nc){

  // Refresh neighbour lists for all cells
  for(int n = 0; n < Nc; n++) {
    Cells[n].Nneighbours = 0;
    Cells[n].neighbours.fill(100);
  }

  // Loop over triangles in triangulation to identify neighbouring cells
  for(std::size_t i = 0; i < triangles.size(); i+=3) {
    // Store references to cells in this triangle
    const unsigned long& a = triangles[i];
    const unsigned long& b = triangles[i+1];
    const unsigned long& c = triangles[i+2];
    int adda = 1;
    int addb = 1;
    int addc = 1;
    // For each of the 3 cells in the triangle, check all components in neighbour array to see if the other two are already there.
    for (int j=0;j<12;j++){
      if (Cells[a].neighbours[j]==b){
        // Cell b is already noted as a neighbour of cell a
        addb = 0;
      }else if (Cells[a].neighbours[j]==c){
        // Cell c is alread noted as a neighbour of cell a
        addc = 0;
      }
    }
    // Make a note of neighbours of cell a if they haven't already been noted
    if (addb==1){
      Cells[a].neighbours(Cells[a].Nneighbours) = b;
      Cells[a].Nneighbours++;
    }
    if (addc==1){
      Cells[a].neighbours(Cells[a].Nneighbours) = c;
      Cells[a].Nneighbours++;
    }

    // Repeat the above for cells b and c
    adda = 1;
    addb = 1;
    addc = 1;
    for (int j=0;j<12;j++){
      if (Cells[b].neighbours[j]==a){
        adda = 0;
      }else if (Cells[b].neighbours[j]==c){
        addc = 0;
      }
    }
    if (adda==1){
      Cells[b].neighbours(Cells[b].Nneighbours) = a;
      Cells[b].Nneighbours++;
    }
    if (addc==1){
      Cells[b].neighbours(Cells[b].Nneighbours) = c;
      Cells[b].Nneighbours++;
    }

    adda = 1;
    addb = 1;
    addc = 1;
    for (int j=0;j<12;j++){ // TODO: check this hardcoding
      if (Cells[c].neighbours[j]==a){
        adda = 0;
      }else if (Cells[c].neighbours[j]==b){
        addb = 0;
      }
    }
    if (adda==1){
      Cells[c].neighbours(Cells[c].Nneighbours) = a;
      Cells[c].Nneighbours++;
    }
    if (addb==1){
      Cells[c].neighbours(Cells[c].Nneighbours) = b;
      Cells[c].Nneighbours++;
    }


  }
}
