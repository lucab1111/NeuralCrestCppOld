//
//  CalculateNoise
//  NeuralCrest
//
//  Created by Christopher Revell on 14/03/19.
//
//

#ifndef CalculateNoise_hpp
#define CalculateNoise_hpp

#include <armadillo>
#include <random>
#include <chrono>
#include "cell.hpp"
#include <vector>

void CalculateNoise(std::vector<cell>& Cells,const float& gamma,std::normal_distribution<float>& gaussian,std::uniform_real_distribution<float>& unif,std::mt19937_64& gen);

#endif
