//
//  UpdateSystem.hpp
//  NeuralCrestCpp
//
//  Created by Christopher Revell on 03/03/2020.
//
//

#ifndef UpdateSystem_hpp
#define UpdateSystem_hpp

#include <vector>
#include "cell.hpp"
#include "parameters.hpp"
#include <armadillo>

void UpdateSystem(std::vector<cell>& Cells,parameters& params, float& t);

#endif /* UpdateSystem_hpp */
