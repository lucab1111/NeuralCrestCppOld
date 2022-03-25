//
//  ContactInhibition.cpp
//  NeuralCrest
//
//  Created by Christopher Revell on 17/09/2019.
//
//

#include "ContactInhibition.hpp"
#include <armadillo>
#include <math.h>
#include "cell.hpp"
#include "parameters.hpp"

using namespace std;
using namespace arma;

void ContactInhibition(vector<cell>& Cells,parameters& params){

  // Use neighbour locations to decide direction for autonomous movement
  float theta;
  vec dx = vec(2,fill::zeros);
  vec thetas = vec(24,fill::zeros);
  int directionBound2;
  int directionBound1;
  int currentBound2;
  int currentBound1;
  int addBoundary;
  int neighboursInRange;
  float maxangle;
  uvec sortedThetaIndices;
  float angle;
  float autonomousDirection;

  for(int i = 0; i < params.Nc; i++) {
    cell& cella = Cells[i];
    cella.v_auto.zeros();


    if (fabs(cella.pos(1)) > params.PMZwidth/2.0 || cella.pos(0) > params.PMZheight/2.0){
      // Do not apply contact inhibition/autonomous motion is cell is outside PMZ
    }
    else{

      // Refresh array storing neighbour angles
      thetas.zeros();

      // Counter for the number of neighbours (including the boundary) within interaction radius of the current cell.
      // Neighbours beyond the interaction threshold cannot polarise the current cell and thus are not considered in contact inhibition
      neighboursInRange = 0;

      // Calculate angle corresponding to "boundary neighbour"
      dx(0) = -cella.v_bound(0);
      dx(1) = -cella.v_bound(1);
      if (dot(dx,dx) > 0){
        // Cell interacts with boundary so we include the boundary force as another neighbour
        theta = atan(fabs(dx(0)/dx(1)))*180/M_PI;
        if (dx(0) >= 0 && dx(1) >= 0){
        }else if (dx(0) >= 0 && dx(1) < 0){
          theta = 180-theta;
        }else if (dx(0) < 0 && dx(1) <= 0){
          theta = 180 + theta;
        }else if (dx(0) < 0 && dx(1) > 0){
          theta = 360 - theta;
        }
        thetas(0) = theta;
        // Increment counters so the algorithm knows to consider the boundary "neighbour" later
        addBoundary = 1;
        neighboursInRange = neighboursInRange + 1;
      }
      else{
        // Cell does not interact with boundary so we shouldn't include the boundary force as another neighbour
        addBoundary = 0;
      }

      // Find angles corresponding to all cell neighbours
      for (int j=0; j<cella.Nneighbours;j++){
        dx = Cells[cella.neighbours[j]].pos - cella.pos;

        // Check if the neighbours' type is different to the first cell so that leaders can interact with followers/PMZ cells
        // Alternatively any pairs that contain either a follower or a PMZ cell can interact
        // This is so that leaders and leaders do not experience CIL
        //if ( Cells[cella.neighbours[j]].type != cella.type || cella.type != 2 || Cells[cella.neighbours[j]].type != 2 ){

        // Only CIL between cells of different types
        //if ( Cells[cella.neighbours[j]].type != cella.type ){

        // Only CIL between cells of different types or if one cell is a PMZ cell
        //if ( Cells[cella.neighbours[j]].type != cella.type || cella.type == 0 || Cells[cella.neighbours[j]].type == 0 ){



        // No CIL Between cells of different types, but CIL between cells of same types
        if ( cella.type == 0 || Cells[cella.neighbours[j]].type == 0 || Cells[cella.neighbours[j]].type != cella.type ){

            // Only if PMZ cells
            //if ( cella.type == 0 && Cells[cella.neighbours[j]].type == 0 ){

            //if (1){
            // Test whether this neighbour is within the threshold distance for interaction.
            if (dot(dx,dx) < pow(cella.interactionThreshold*(Cells[cella.neighbours[j]].cellradius+cella.cellradius),2)){
              // Neighbour is within the threshold for polarisation
              neighboursInRange = neighboursInRange + 1;
              // Calculate angle of this neighbour
              theta = atan(fabs(dx(0)/dx(1)))*180/M_PI;
              if (dx(0) > 0 && dx(1) > 0){
              }else if (dx(0) > 0 && dx(1) < 0){
                theta = 180-theta;
              }else if (dx(0) < 0 && dx(1) < 0){
                theta = 180 + theta;
              }else if (dx(0) < 0 && dx(1) > 0){
                theta = 360 - theta;
              }
              // Store calculated angle in thetas array
              thetas(neighboursInRange) = theta;
            }
            else{
              // Neighbour is outside the threshold distance for polarisation
            }
       }
      }

      // Only apply contact inhibition and autonomous motion if there are neighbours within interaction range
      if (neighboursInRange > 0){

        // Sort the thetas array to give angles in descending order
        sortedThetaIndices = sort_index(thetas,"descend");

        // Find the maximum angle between any two adjacent neighbours
        maxangle = 0;
        for (int j=0; j<neighboursInRange; j++){
          if (j==neighboursInRange-1){
            // Special treatment for the gap between highest angle and lowest angle
            currentBound2 = neighboursInRange-1;
            currentBound1 = 0;
            angle = thetas(sortedThetaIndices(currentBound2))+360 - thetas(sortedThetaIndices(currentBound1));
          }else{
            currentBound2 = j;
            currentBound1 = j+1;
            angle = thetas(sortedThetaIndices(j)) - thetas(sortedThetaIndices(j+1));
          }
          if (angle>360){
            angle = angle-360;
          }else{}
          if (angle > maxangle){
            // If the current angle is greater than the previous max, update stored max values
            maxangle = angle;
            directionBound2 = currentBound2;
            directionBound1 = currentBound1;
          }
          else {
            // Current angle is smaller than previous max, so ignore
          }
        }

        // Set direction of autonomous movement by bisecting the neighbours corresponding to the max angle
        autonomousDirection = (thetas(sortedThetaIndices(directionBound1)) + maxangle/2.0)*M_PI/180.0;
        // Use direction to find autonomous motion vector with magnitude proportional to square of max angle
        cella.v_auto(0) = pow(maxangle,2)*cella.autonomousMag*sin(autonomousDirection);
        cella.v_auto(1) = pow(maxangle,2)*cella.autonomousMag*cos(autonomousDirection);
        // Update cell velocity with autonomous motion vector
        cella.v(0) = cella.v(0) + cella.v_auto(0);
        cella.v(1) = cella.v(1) + cella.v_auto(1);

      }
      else{
        // No neighours within interaction range
        cella.v_auto(0) = 0;
        cella.v_auto(1) = 0;
      }
    }
  }
}
