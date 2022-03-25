//
//  Noise
//  NeuralCrest
//
//  Created by Christopher Revell on 14/03/19.
//
//

#include "CalculateNoise.hpp"
#include <armadillo>
#include <random>
#include <chrono>
#include "cell.hpp"
#include <vector>

using namespace std;
using namespace arma;

void CalculateNoise(vector<cell>& Cells,const float& gamma,normal_distribution<float>& gaussian,uniform_real_distribution<float>& unif,mt19937_64& gen){

	float currentRandomNumber;
	vec zeta = vec(2,fill::zeros); // Vector for stochastic component

	for (int ii=0;ii<Cells.size();ii++){
		// For each cell, use random number generator to find the angle of stochastic movement
	  currentRandomNumber = unif(gen);
	  zeta(0) = cos(2*M_PI*currentRandomNumber);
	  zeta(1) = sin(2*M_PI*currentRandomNumber);
		// Use the normal distribution to find the magnitude of stochastic movement in this direction
		Cells[ii].v = Cells[ii].v + fabs(gaussian(gen))*zeta/gamma;
	}
}
