//
//  OpenFiles.cpp
//
//  Created by Christopher Revell on 08/02/2019.
//
//

#include "OpenFiles.hpp"
#include "parameters.hpp"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>
#include <ctime>

using namespace std;

// Open files needed for simulation and store objects in the files vector.
void OpenFiles(char* buffer,vector<ofstream>& files, parameters& params)
{

  vector<string> names;

  int aMag = params.leader_autonomousMag*1000000000;

  // Create directory to store simulation results
  sprintf(buffer,"output/l_aM%d_l_De%d_l_iT%d_f_aM%d_f_De%d_f_iT_%d_slurmArray_%d_runID_%d_experimentType_%d",aMag,static_cast<int>(params.leader_De*1000000),static_cast<int>(params.leader_interactionThreshold*1000000),static_cast<int>(params.follower_autonomousMag*1000000000),static_cast<int>(params.follower_De*1000000),static_cast<int>(params.follower_interactionThreshold),static_cast<int>(params.slurm_array), static_cast<int>(params.runID), params.experimentType);
  
  system(("mkdir "+string(buffer)).c_str());
  // Open data files within directory
  names.push_back((string(buffer)+"/initialconditions.txt").c_str());
  names.push_back((string(buffer)+"/cellpositions.txt").c_str());
  names.push_back((string(buffer)+"/cellCountPMZ.txt").c_str());
  files.resize(names.size());
  for (int ii=0;ii<names.size();ii++){
    files[ii].open(names[ii],fstream::out);
  }



    // Print to input parameter file for reference later
  files[0] << "Nc                             " << params.Nc                               << endl;
  files[0] << "zeta_mag                       " << params.zeta_mag                         << endl;
  files[0] << "cellradius                     " << params.cellradius                       << endl;
  files[0] << "PMZwidth                       " << params.PMZwidth                         << endl;
  files[0] << "PMZheight                      " << params.PMZheight                        << endl;
  files[0] << "CEwidth                        " << params.CEwidth                          << endl;
  files[0] << "CMwidth                        " << params.CMwidth                          << endl;
  files[0] << "Clength                        " << params.Clength                          << endl;
  files[0] << "t_max                          " << params.t_max                            << endl;
  files[0] << "dt                             " << params.dt                               << endl;
  files[0] << "output_interval                " << params.output_interval                  << endl;
  files[0] << "chainShape                     " << params.chainShape                       << endl;
  files[0] << "experimentType                 " << params.experimentType                   << endl;
  files[0] << "leader_k                       " << params.leader_k                         << endl;
  files[0] << "leader_De                      " << params.leader_De                        << endl;
  files[0] << "leader_autonomousMag           " << params.leader_autonomousMag             << endl;
  files[0] << "leader_interactionThreshold    " << params.leader_interactionThreshold      << endl;
  files[0] << "leader_gradientSensitivity     " << params.leader_gradientSensitivity       << endl;
  files[0] << "leader_Size                    " << params.leader_size                      << endl;
  files[0] << "follower_k                     " << params.follower_k                       << endl;
  files[0] << "follower_De                    " << params.follower_De                      << endl;
  files[0] << "follower_autonomousMag         " << params.follower_autonomousMag           << endl;
  files[0] << "follower_interactionThreshold  " << params.follower_interactionThreshold    << endl;
  files[0] << "follower_gradientSensitivity   " << params.follower_gradientSensitivity     << endl;
  files[0] << "slurm_array                    " << params.slurm_array                      << endl;
  files[0] << "runID                          " << params.runID                            << endl;
  files[0] << "realTimePlot                   " << params.realTimePlot                     << endl;
  files[0] << "middle_zone_height             " << params.mz_pmz_ratio                     << endl;


}
