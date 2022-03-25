//
//  CalculateForces.hpp
//  NeuralCrest
//
//  Created by Christopher Revell on 28/11/2018.
//
//

#ifndef CalculateForces_hpp
#define CalculateForces_hpp

#include "cell.hpp"
#include <vector>
#include <armadillo>
#include "MorseForce.hpp"
#include "parameters.hpp"
#include <math.h>

// Subroutine to identify neighbouring cells and calculate forces between them.
void CalculateForces(std::vector<cell>& Cells,parameters& params, const float& gamma);

#endif /* CalculateForces_hpp */
