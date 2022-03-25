//
//  CalculateForces.hpp
//  NeuralCrest
//
//  Created by Dylan Feldner-Busztin on 12/10/2020.
//
//

#ifndef Gradient_hpp
#define Gradient_hpp

#include <armadillo>
#include <random>
#include <chrono>
#include "cell.hpp"
#include "parameters.hpp"
#include <vector>

void applyGradient(std::vector<cell>& Cells,std::normal_distribution<float>& gaussian,std::uniform_real_distribution<float>& unif,std::mt19937_64& gen, parameters& params);

#endif
