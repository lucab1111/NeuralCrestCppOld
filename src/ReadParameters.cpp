//
//  ReadParameters.cpp
//  NeuralCrest
//
//  Created by Christopher Revell on 15/03/2019.
//
//

#include "ReadParameters.hpp"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>

// Read simulation parameters from the command line.
void ReadParameters(int argc,char *argv[],int& Nc, float& zeta_mag, float& cellradius, float& PMZwidth, float&	PMZheight, float& CEwidth, float& CMwidth, float& Clength, float& t_max, float& dt, float& output_interval, int& chainShape, int& realTimePlot, int& experimentType, float& leader_k, float& leader_De, float& leader_autonomousMag, float& leader_interactionThreshold, float& leader_gradientSensitivity, float& leader_size, float& follower_k, float& follower_De, float& follower_autonomousMag, float& follower_interactionThreshold, float& follower_gradientSensitivity, int& slurm_array, int& runID, float& mz_pmz_ratio){

	// Read from command line
	Nc									= atoi(argv[1]);
	zeta_mag							= atof(argv[2]);
	cellradius							= atof(argv[3]);
	PMZwidth							= atof(argv[4]);
	PMZheight							= atof(argv[5]);
	CEwidth								= atof(argv[6]);
	CMwidth								= atof(argv[7]);
	Clength								= atof(argv[8]);
	t_max								= atof(argv[9]);
	dt									= atof(argv[10]);
	output_interval						= atof(argv[11]);
    chainShape							= atoi(argv[12]);
    realTimePlot						= atoi(argv[13]);
    experimentType						= atoi(argv[14]);
	leader_k							= atof(argv[15]);
	leader_De 							= atof(argv[16]);
	leader_autonomousMag 				= atof(argv[17]);
	leader_interactionThreshold 		= atof(argv[18]);
	leader_gradientSensitivity			= atof(argv[19]);
	leader_size							= atof(argv[20]);
	follower_k							= atof(argv[21]);
	follower_De 						= atof(argv[22]);
	follower_autonomousMag 				= atof(argv[23]);
	follower_interactionThreshold 		= atof(argv[24]);
	follower_gradientSensitivity 		= atof(argv[25]);
    slurm_array							= atoi(argv[26]);
    runID								= atoi(argv[27]);
    mz_pmz_ratio						= atof(argv[28]);

}
