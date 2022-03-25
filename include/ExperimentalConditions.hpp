//
//  ExperimentalConditions.hpp
//  NeuralCrest
//
//  Created by Dylan Feldner-Busztin on 18/06/2020.
//
//

#ifndef ExperimentalConditions_hpp
#define ExperimentalConditions_hpp

#include <stdio.h>
#include <iostream>
#include <string>
#include "cell.hpp"
#include "parameters.hpp"
#include <random>
#include <cmath>
#include <stdlib.h>
#include <armadillo>

using namespace std;

void allLeaderModification(vector<cell>& Cells, parameters& params, int& nMigratingCells, int& firstCell, int& leaderID);

void leader_Modification(cell& Cell, parameters& params, int& nMigratingCells, int& firstCell, int& leaderID);

//void firstLeaderModification(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, float& PMZheight, int& leaderID,int& nMigratingCells,float& leader_k, float& leader_autonomousMag, float& leader_De, float& leader_interactionThreshold, float& follower_autonomousMag, float& follower_De, float& follower_interactionThreshold);

void leaderAblation(vector<cell>& Cells, parameters& params , int& firstCell, int& leaderID, int& nMigratingCells, int& leaderAblated);

void followerAblation(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, int& leaderID, float& PMZheight, int& followerAblated);

void leaderAblationNextCellLeader(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, float& PMZheight, int& leaderID, int& nMigratingCells, float& leader_autonomousMag, float& leader_De, float& leader_interactionThreshold, float& follower_autonomousMag, float& follower_De, float& follower_interactionThreshold, int& leaderAblated);

void applyExperimentalCondition( vector<cell>& Cells,parameters& params, int& nMigratingCells, int& firstCell, int& leaderAblated, int& followerAblated, int& leaderID);

void randomLeader(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, float& PMZheight, int& leaderID, int& nMigratingCells,float& leader_k, float& leader_autonomousMag, float& leader_De, float& leader_interactionThreshold, float& follower_autonomousMag, float& follower_De, float& follower_interactionThreshold, int& leaderAblated, float& leaderSize, float& leader_gradientSensitivity);

void oddLeaderModification(vector<cell>& Cells, parameters& params, int& firstCell, int& nMigratingCells);

void everyThirdLeaderSizeModification(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, float& PMZheight, int& leaderID, int& nMigratingCells, float& leader_k, float& leader_autonomousMag, float& leader_De, float& leader_interactionThreshold, float& leader_size, float& follower_autonomousMag, float& follower_De, float& follower_interactionThreshold, float& leader_gradientSensitivity, float& follower_gradientSensitivity);

void allLeaderSizeModification(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, float& PMZheight, int& leaderID, int& nMigratingCells, float& leader_autonomousMag,float& leader_k, float& leader_De, float& leader_interactionThreshold, float& follower_autonomousMag, float& follower_De, float& follower_interactionThreshold);

//void allFollowerModification(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, float& PMZheight, int& leaderID, int& nMigratingCells, float& leader_autonomousMag,float& leader_k, float& leader_De, float& leader_interactionThreshold, float& follower_autonomousMag, float& follower_De, float& follower_interactionThreshold);

void gainOfFunction(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, float& PMZheight, int& leaderID, int& nMigratingCells, float& leader_autonomousMag,float& leader_k, float& leader_De, float& leader_interactionThreshold, float& leader_size,float& follower_autonomousMag, float& follower_De, float& follower_interactionThreshold, float& leader_gradientSensitivity);

void lossOfFunction(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, float& PMZheight, int& leaderID, int& nMigratingCells, float& leader_autonomousMag,float& leader_k, float& leader_De, float& leader_interactionThreshold, float& leader_size, float& follower_autonomousMag, float& follower_De, float& follower_interactionThreshold, float& leader_gradientSensitivity, float& follower_gradientSensitivity);

#endif /* experiments_hpp */





