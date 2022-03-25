 //
//  ExperimentalConditions.cpp
//  NeuralCrest
//
//  Created by Dylan Feldner-Busztin on 28/02/2021.
//
//

#include "ExperimentalConditions.hpp"
#include "parameters.hpp"
#include <iostream>
#include <string>
#include "cell.hpp"
#include <random>
#include <cmath>
#include <stdlib.h>
#include <armadillo>

using namespace std;
using namespace arma;

float allocation_level = 10; // Beyond this point cells are considered to be migrating

void leader_Modification(cell& Cell, parameters& params, int& nMigratingCells, int& firstCell, int& leaderID)
{


        Cell.autonomousMag = params.leader_autonomousMag;
        Cell.De = params.leader_De;
        Cell.k = params.leader_k;
        Cell.a = sqrt(Cell.k/(2*Cell.De));
        Cell.cellradius = params.leader_size;
        Cell.type = 2;
        firstCell = 1;
        Cell.interactionThreshold = params.leader_interactionThreshold;
        Cell.gradientSensitivity = params.leader_gradientSensitivity;
        nMigratingCells = nMigratingCells+1;

}


// alternative to oddLeaderModification where all cells become type 2
void allLeaderModification(vector<cell>& Cells, parameters& params, int& nMigratingCells, int& firstCell, int& leaderID){


      for (int ii=0;ii<params.Nc;ii++){

        // leaders
        if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && Cells[ii].type != 2)
          {
            leader_Modification(Cells[ii], params, nMigratingCells, firstCell, leaderID);
            leaderID = ii;
          }
      }
    }


// All followers
void allFollowerModification( vector<cell>& Cells, parameters& params, int& firstCell, int& leaderID, int& nMigratingCells ){


      for (int ii=0;ii<params.Nc;ii++){

        // Followers
        if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && Cells[ii].type != 1)
          {
            Cells[ii].type = 1;
            nMigratingCells = nMigratingCells+1;
          }
      }
    }


  // Odd leader size
void everyForthLeaderModification(vector<cell>& Cells, parameters& params, int& firstCell, int& leaderID, int& nMigratingCells){


      for (int ii=0;ii<params.Nc;ii++){

        // First ever cell
        if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==0)
        {
            leader_Modification(Cells[ii], params, nMigratingCells, firstCell, leaderID);
            leaderID = ii;
        }

        // Next cells - leader
          else if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==1 && nMigratingCells%4 == 0 && Cells[ii].type == 0 ){

            leader_Modification(Cells[ii], params, nMigratingCells, firstCell, leaderID);
        }

          // Next cells - follower. Just change type for plotting purposes
          else if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==1 && nMigratingCells%4 != 0 && Cells[ii].type == 0 ){

            Cells[ii].type = 1;
            firstCell = 1;
            nMigratingCells = nMigratingCells+1;
        }
      }
    }


  // Just one leader
void firstLeaderModification(vector<cell>& Cells, parameters& params, int& firstCell, int& leaderID, int& nMigratingCells){


      for (int ii=0;ii<params.Nc;ii++){

        // First ever cell
        if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==0)
        {
            leader_Modification(Cells[ii], params, nMigratingCells, firstCell, leaderID);
            leaderID = ii;
        }

          // Next cells - follower. Just change type for plotting purposes
          else if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==1 && Cells[ii].type == 0 ){

            Cells[ii].type = 1;
            firstCell = 1;
            nMigratingCells = nMigratingCells+1;
        }
      }
    }


// Perform leader ablation experiment
void leaderAblation(vector<cell>& Cells, parameters& params , int& firstCell, int& leaderID, int& nMigratingCells, int& leaderAblated)
{
  // Ablate first cell to go beyond y = Clength/2
  for (int ii=0;ii<params.Nc;ii++)
  {

     float y_of_middle_zone_middle = -params.PMZheight/2 - params.Clength -(params.PMZheight * params.mz_pmz_ratio)/2;

      if (Cells[ii].pos[0] < y_of_middle_zone_middle && leaderAblated==0 && ii == leaderID)
      {
        cout << Cells[ii].pos[0];
        Cells.erase (Cells.begin()+ii);
        leaderAblated = 1;
        params.Nc = params.Nc - 1;
        cout << endl << "leader ablated" << endl;
      }
  }

}


// Perform follower ablation experiment
void followerAblation(vector<cell>& Cells,int& Nc, int& firstCell, float& Clength, int& leaderID, float& PMZheight, int& followerAblated)
{
  // Ablate second cell to go beyond y = Clength/2
  for (int ii=0;ii<Nc;ii++)
  {
    // Exclude the leader from ablation
    if (ii != leaderID)
    {
      // Ablate first follower
      if (firstCell==1 && (Cells[ii].pos[0] < (-PMZheight/2-Clength*0.5) && followerAblated == 0))
      {
        Cells.erase (Cells.begin()+ii);
        cout << "follower ablated" << endl;
        followerAblated = 1; // Increment this so that ablation occurs only once
        Nc = Nc - 1;
      }
    }
  }
}


void oddLeaderModification(vector<cell>& Cells, parameters& params, int& nMigratingCells, int& firstCell, int& leaderID){


     for (int ii=0;ii<params.Nc;ii++){

       // First ever cell
       if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==0)
       {
          leader_Modification(Cells[ii], params, nMigratingCells, firstCell, leaderID);
       }

       // Next cells - leader
         else if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==1 && nMigratingCells%2 == 0 && Cells[ii].type == 0 ){

          leader_Modification(Cells[ii], params, nMigratingCells, firstCell, leaderID);
       }

         // Next cells - follower. Just change type for plotting purposes
         else if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==1 && nMigratingCells%2 != 0 && Cells[ii].type == 0 ){

           //allFollowerModification( Cells, params, firstCell, leaderID, nMigratingCells );
          Cells[ii].type = 1;
          nMigratingCells = nMigratingCells+1;
       }
     }
   }


void everyThirdLeaderModification(vector<cell>& Cells, parameters& params, int& nMigratingCells, int& firstCell, int& leaderID){


     for (int ii=0;ii<params.Nc;ii++){

       // First ever cell
       if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==0)
       {

          leader_Modification(Cells[ii], params, nMigratingCells, firstCell, leaderID);
          leaderID = ii;
       }

       // Next cells - leader
         else if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==1 && nMigratingCells%3 == 0 && Cells[ii].type == 0 ){

          leader_Modification(Cells[ii], params, nMigratingCells, firstCell, leaderID);
       }

         // Next cells - follower. Just change type for plotting purposes
         else if (Cells[ii].pos[0] < (-params.PMZheight/2.0-params.Clength/allocation_level) && firstCell==1 && nMigratingCells%3 != 0 && Cells[ii].type == 0 ){

           //allFollowerModification( Cells, params, firstCell, leaderID, nMigratingCells );
          Cells[ii].type = 1;
          nMigratingCells = nMigratingCells+1;
       }
     }
   }


void applyExperimentalCondition(vector<cell>& Cells, parameters& params, int& nMigratingCells, int& firstCell, int& leaderAblated, int& followerAblated, int& leaderID)
{

    // Every fourth cell is a leader
   if (params.experimentType == 1)
     {
       everyForthLeaderModification( Cells, params, firstCell, leaderID, nMigratingCells);
     }

    // Every cell is a leader
   if (params.experimentType == 2)
     {
       allLeaderModification(Cells, params, nMigratingCells, firstCell, leaderID);
     }

   // Every cell is a follower
   if (params.experimentType == 3)
     {
       allFollowerModification(Cells, params, nMigratingCells, firstCell, leaderID);
     }

    // Every second cell is a leader
   if (params.experimentType == 4)
     {
       oddLeaderModification(Cells, params, nMigratingCells, firstCell, leaderID);
     }

    // Leader ablation
    if (params.experimentType == 5)
    {
      everyForthLeaderModification( Cells, params, firstCell, leaderID, nMigratingCells);
      leaderAblation( Cells, params , firstCell, leaderID, nMigratingCells, leaderAblated);
    }

    // Follower ablation
    if (params.experimentType == 6)
    {
      everyForthLeaderModification( Cells, params, firstCell, leaderID, nMigratingCells);
      followerAblation( Cells, params.Nc, firstCell, params.Clength, leaderID, params.PMZheight, followerAblated);
    }

    // Only first cell leader
    if (params.experimentType == 7)
    {
      firstLeaderModification( Cells, params, firstCell, leaderID, nMigratingCells);

    }

    // Every third cell leader
    if (params.experimentType == 8)
    {
      everyThirdLeaderModification(Cells, params, nMigratingCells, firstCell, leaderID);

    }
}
