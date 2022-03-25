//
//  IdentifyNeighbours.hpp
//  NeuralCrest
//
//  Created by <author> on 17/09/2019.
//
//

#ifndef IdentifyNeighbours_hpp
#define IdentifyNeighbours_hpp

#include "cell.hpp"
#include <vector>
#include <armadillo>


void IdentifyNeighbours(std::vector<cell>& Cells,const std::vector<unsigned long>& triangles,const int& Nc);

#endif
