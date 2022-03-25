//
//  ReadParameters.hpp
//  NeuralCrest
//
//  Created by Christopher Revell on 15/03/2019.
//
//

#ifndef ReadParameters_hpp
#define ReadParameters_hpp

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>

void ReadParameters(int argc,char *argv[],int& Nc, float& zeta_mag, float& cellradius, float& PMZwidth, float&	PMZheight, float& CEwidth, float& CMwidth, float& Clength, float& t_max, float& dt, float& output_interval, int& chainShape, int& realTimePlot, int& experimentType, float& leader_k, float& leader_De, float& leader_autonomousMag, float& leader_interactionThreshold, float& leader_gradientSensitivity, float& leader_size, float& follower_k, float& follower_De, float& follower_autonomousMag, float& follower_interactionThreshold, float& follower_gradientSensitivity, int& slurm_array, int& runID, float& mz_pmz_ratio);

#endif /* ReadParameters_hpp */
