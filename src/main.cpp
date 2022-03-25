#include <cmath>
#include <armadillo>
#include <vector>
#include <iostream>
#include "cell.hpp"
#include "CalculateForces.hpp"
#include "Initialise.hpp"
#include "delaunator.hpp"
#include "CalculateNoise.hpp"
#include "ReadParameters.hpp"
#include "OutputData.hpp"
#include "Boundary0.hpp"
#include "Boundary1.hpp"
#include "Boundary2.hpp"
#include "Boundary3.hpp"
#include "OpenFiles.hpp"
#include "IdentifyNeighbours.hpp"
#include "ContactInhibition.hpp"
#include "UpdateSystem.hpp"
#include "ExperimentalConditions.hpp"
#include "Gradient.hpp"
#include "parameters.hpp"
#include <cmath>
#include <random>

using namespace std;
using namespace arma;

char outputfolder[100];

int main(int argc,char *argv[]){

  // Parameters of system
  int   Nc;                             // Number of cells in the system
  float cellradius;                     // Typical cell radius (ie Equilibrium separation for inter-cell interaction of cell with age 0)
  float dt;                             // Time interval
  float t_max;                          // Total run time for system
  float output_interval;                // Time interval for outputting data
  float zeta_mag;                       // Magnitude of stochastic component
  float PMZwidth;                       // Width of premigratory zone
  float PMZheight;                      // Height of premigratory zone
  float CEwidth;                        // Width of chain entrance
  float CMwidth;                        // Width of chain at widest point
  float Clength;                        // Length of chain
  float mz_pmz_ratio;                   // Height of the middle zone relative to PMZheight

  float t     = 0;                      // System clock
  float gamma = 1.0;                    // Overdamped Langevin equation drag factor
  float steadyStateTimer = 0;           // Tracks how long it has been since a cell moved below the previous lowest point
  double ymin_tmp        = 10;          // Value for calculating current lowest cell position
  double ymin            = 10;          // Stored minimum cell y position
  int   nloop = 0;                      // Counter for image files
  int   chainShape;                     // 0 for steadily widening chain, 1 for chain with diamond zone
  int   realTimePlot;                   // Controls whether or not plotting occurs during run
  vector<cell>     Cells;               // Vector containing cell objects corresponding to all cells in the system
  vector<ofstream> files;               // Set of output files

  // Cell types get separate attributes
  float leader_autonomousMag;           // Magnitude of autonomous velocity component
  float leader_De;
  float leader_interactionThreshold;    // Distance threshold for interactions as a proportion of equilibrium distance
  float leader_k;
  float leader_gradientSensitivity;
  float leader_size;

  float follower_autonomousMag;
  float follower_De;
  float follower_interactionThreshold;
  float follower_k;
  float follower_gradientSensitivity;

  int firstCell = 0;
  int leaderID;
  int nMigratingCells = 0;
  int nLeadersInChain = 0;
  int experimentType;
  int slurm_array;
  int runID;
  int leaderAblated = 0;
  int followerAblated = 0;

  // Initialise system
  // Read parameters from command line
  ReadParameters(argc,
                  argv,
                  Nc,
                  zeta_mag,
                  cellradius,
                  PMZwidth,
                  PMZheight,
                  CEwidth,
                  CMwidth,
                  Clength,
                  t_max,
                  dt,
                  output_interval,
                  chainShape,
                  realTimePlot,
                  experimentType,
                  leader_k,
                  leader_De,
                  leader_autonomousMag,
                  leader_interactionThreshold,
                  leader_gradientSensitivity,
                  leader_size,
                  follower_k,
                  follower_De,
                  follower_autonomousMag,
                  follower_interactionThreshold,
                  follower_gradientSensitivity,
                  slurm_array,
                  runID,
                  mz_pmz_ratio);

  // Populate parameters class with inputs
  parameters params = parameters(Nc,
                                zeta_mag,
                                cellradius,
                                PMZwidth,
                                PMZheight,
                                CEwidth,
                                CMwidth,
                                Clength,
                                t_max,
                                dt,
                                output_interval,
                                chainShape,
                                realTimePlot,
                                experimentType,
                                leader_k,
                                leader_De,
                                leader_autonomousMag,
                                leader_interactionThreshold,
                                leader_gradientSensitivity,
                                leader_size,
                                follower_k,
                                follower_De,
                                follower_autonomousMag,
                                follower_interactionThreshold,
                                follower_gradientSensitivity,
                                slurm_array,
                                runID,
                                mz_pmz_ratio);

  // Open files
  OpenFiles(outputfolder,files, params);

  std::random_device rd;  //Will be used to obtain a seed for the random number engine
  std::mt19937_64 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
  std::normal_distribution<float> gaussian{0.0,zeta_mag};
  std::uniform_real_distribution<float> unif(0.0,1.0);

  // Create cells and initialise positions
  Initialise(Cells,params);

  // Output initial setup
  OutputData(outputfolder,Cells,t,params,nloop,files[1],files[2]);

  // Iterate over simulation until reaching max alloted time
    // Add this condition to stop simulation once downward movement has stabilised
    // steadyStateTimer < 30.0*output_interval &&
  while (t < t_max){

    // Perform delaunay triangulation over cell locations
    vector<double> coords;
    for (int ii=0;ii<params.Nc;ii++){
      coords.push_back(static_cast<double>(Cells[ii].pos(0)));
      coords.push_back(static_cast<double>(Cells[ii].pos(1)));
    }
    delaunator::Delaunator triangulation(coords);

    // Identify nearest neighbours from triangulation
    IdentifyNeighbours(Cells,triangulation.triangles,params.Nc);

    // Calculate forces between identified nearest neighbours
    CalculateForces(Cells,params,gamma);

    // Apply boundary forces to all cells
    if (chainShape == 0){
      Boundary0(Cells,params,gamma);
    }
    else if (chainShape == 1){
      Boundary1(Cells,params,gamma);
    }
    else if (chainShape == 2){
      Boundary2(Cells,params,gamma);
    }
    else if (chainShape == 3){
      Boundary3(Cells,params,gamma);
    }

    // Calculate autonomous motion velocities as determined by contact inhibition
    // Use first 20th of run time to equilibrate system before initiation autonomous motion
    if (t>t_max/20){
      ContactInhibition(Cells,params);
    }

    // Apply gradient
    applyGradient(Cells,gaussian,unif,gen, params);

    // Apply stochastic noise to all cells
    CalculateNoise(Cells,gamma,gaussian,unif,gen);

    // Update system clock
    UpdateSystem(Cells,params,t);

    // Apply experimental conditions
    applyExperimentalCondition(Cells, params, nMigratingCells, firstCell, leaderAblated, followerAblated, leaderID);

    // Output cell positions to file and time to command line
    if (fmod(t,output_interval)<(dt-0.0001)){
      OutputData(outputfolder,Cells,t,params,nloop,files[1],files[2]);
    }


    if (t>t_max/4){
      for (int ii=0; ii<params.Nc; ii++){
        ymin_tmp = min(Cells[ii].pos(0),ymin_tmp);
      }
      if (ymin_tmp<ymin){
        ymin=ymin_tmp;
        steadyStateTimer=0;
      }else if (ymin < - PMZheight/2.0 - Clength/5.0){ // At least one cell must have entered the confinement zone
        steadyStateTimer+=dt;
      }
    }

  }

  // Convert image files to an animated gif
 if (realTimePlot == 1){
   system(("convert -delay 10 -loop 0 "+string(outputfolder)+"/plot*.png "+string(outputfolder)+"/animated.gif").c_str());
 }

  return 0;
}
