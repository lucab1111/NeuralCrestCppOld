//
//  Boundary0.cpp
//  NeuralCrest
//
//  Created by Christopher Revell on 08/08/2019.
//
//

#include "Boundary0.hpp"
#include <armadillo>
#include <cmath>
#include "cell.hpp"
#include <vector>
#include "MorseForce.hpp"
#include "parameters.hpp"

using namespace std;
using namespace arma;

void Boundary0(vector<cell>& Cells,parameters& params, float& gamma){

  // Cells interact with boundary if they are within a cell radius of it.
  // This file is complex and should be tidied up or used with reference to a diagram.
  float dif,dx_mag,q,p,yleft,dy;
  vec dx = vec(2,fill::zeros);
  vec F = vec(2,fill::zeros);

  for (int j=0; j<params.Nc; j++){
    float& a = Cells[j].a;
    float& De = Cells[j].De;
    Cells[j].v_bound.zeros();
    if ((Cells[j].pos(0) + params.PMZheight/2.0) < Cells[j].cellradius){
      // Cell interacts with lower boundary.
      if ((Cells[j].pos(0) + params.PMZheight/2.0) > 0){
        // Cell is in PMZ but interacts with lower boundary.
        if (fabs(Cells[j].pos(1)) < params.CEwidth/2.0){
          // Cell is within the chain entrance zone of PMZ
          // Interaction with left edge
          dx(0) = -params.PMZheight/2.0; // Location of left corner of chain entrance
          dx(1) = -params.CEwidth/2.0;
          dx = Cells[j].pos - dx; // Vector from left corner of chain entrance to cell
          dx_mag = sqrt(dot(dx,dx));
          dif = dx_mag - Cells[j].cellradius;
          if (dif < 0){
            F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif))/dx_mag;
            Cells[j].v = Cells[j].v - F/gamma;
            Cells[j].v_bound = Cells[j].v_bound - F/gamma;
          }
          //Interaction with right edge
          dx(0) = -params.PMZheight/2.0; // Location of right corner of chain entrance
          dx(1) = params.CEwidth/2.0;
          dx = Cells[j].pos - dx; // Vector from right corner of chain entrance to cell
          dx_mag = sqrt(dot(dx,dx));
          dif = dx_mag - Cells[j].cellradius;
          if (dif < 0){
            F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif))/dx_mag;
            Cells[j].v = Cells[j].v - F/gamma;
            Cells[j].v_bound = Cells[j].v_bound - F/gamma;
          }
        }
        else{
          // Cell interacts with lower boundary of PMZ away from chain entrance
          dx.zeros(); // Refresh boundary force direction
          dx(0) = -1.0;
          dif = Cells[j].pos(0) + params.PMZheight/2.0 - Cells[j].cellradius;
          F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
          Cells[j].v = Cells[j].v + F/gamma;
          Cells[j].v_bound = Cells[j].v_bound + F/gamma;
        }
      }
      else{
        // Cell is below PMZ
        if (fabs(Cells[j].pos(1)) > params.CEwidth/2.0 && fabs(Cells[j].pos(0)+params.PMZheight/2.0) < fabs(Cells[j].pos(1))-params.CEwidth/2.0){
          // Cell outside chain zone and closer to lower surface of PMZ than chain zone
          dx.zeros(); // Refresh boundary force direction
          dx(0) = -1.0;
          dif = Cells[j].pos(0) + params.PMZheight/2.0 - Cells[j].cellradius;
          F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
          Cells[j].v = Cells[j].v + F/gamma;
          Cells[j].v_bound = Cells[j].v_bound + F/gamma;
        }
        else{
          // Cell is closer to chain zone than lower surface of PMZ

          if (fabs(params.CMwidth-params.CEwidth) < 0.000001){
            // Chain is straight
            dx.zeros();
            dx(1) = -1.0;
            if (Cells[j].pos(1) - Cells[j].cellradius < -params.CEwidth/2.0){
              // Cell interacts with left side of chain zone
              dif = Cells[j].pos(1) - Cells[j].cellradius + params.CEwidth/2.0;
              F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));;
              Cells[j].v = Cells[j].v + F/gamma;
              Cells[j].v_bound = Cells[j].v_bound + F/gamma;
            }

            if (Cells[j].pos(1) + Cells[j].cellradius > params.CEwidth/2.0){
              // Cell interacts with right side of chain zone
              dif = params.CEwidth/2.0 - Cells[j].pos(1) - Cells[j].cellradius;
              F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));;
              Cells[j].v = Cells[j].v - F/gamma;
              Cells[j].v_bound = Cells[j].v_bound - F/gamma;
            }

          }
          else{
            // Chain is not straight
            dx.zeros(); // Refresh boundary force direction
            q = 2.0*params.Clength*(params.CEwidth/2.0 - Cells[j].cellradius*sqrt((params.CMwidth-params.CEwidth)*(params.CMwidth-params.CEwidth)/(4.0*params.Clength*params.Clength) +1.0))/(params.CMwidth-params.CEwidth) - params.PMZheight/2.0;
            p = 2.0*params.Clength/(params.CMwidth-params.CEwidth);
            yleft = p*Cells[j].pos(1) + q;
            if (Cells[j].pos(0) > yleft) {
              //Interacts with top left side of chain zone
              dx(0) = params.CMwidth-params.CEwidth;
              dx(1) = -2.0*params.Clength;
              dx_mag = sqrt(dot(dx,dx));
              dy = Cells[j].pos(0) - yleft;
              dif = -dy*(params.CMwidth-params.CEwidth)/sqrt(4.0*params.Clength*params.Clength + (params.CMwidth-params.CEwidth)*(params.CMwidth-params.CEwidth));
              F = (dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif)))/dx_mag;
              Cells[j].v = Cells[j].v + F/gamma;
              Cells[j].v_bound = Cells[j].v_bound + F/gamma;
            }

            dx.zeros(); // Refresh boundary force direction
            q = 2.0*params.Clength*(params.CEwidth/2.0 - Cells[j].cellradius*sqrt((params.CMwidth-params.CEwidth)*(params.CMwidth-params.CEwidth)/(4.0*params.Clength*params.Clength) +1.0))/(params.CMwidth-params.CEwidth) - params.PMZheight/2.0;
            p = 2.0*params.Clength/(params.CMwidth-params.CEwidth);
            yleft = - p*Cells[j].pos(1) + q;
            if (Cells[j].pos(0) > yleft) {
              //Interacts with top right side of chain zone
              dx(0) = params.CMwidth-params.CEwidth;
              dx(1) = 2.0*params.Clength;
              dx_mag = sqrt(dot(dx,dx));
              dy = Cells[j].pos(0) - yleft;
              dif = -dy*(params.CMwidth-params.CEwidth)/sqrt(4.0*params.Clength*params.Clength + (params.CMwidth-params.CEwidth)*(params.CMwidth-params.CEwidth));
              F = (dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif)))/dx_mag;
              Cells[j].v = Cells[j].v + F/gamma;
              Cells[j].v_bound = Cells[j].v_bound + F/gamma;
            }

            dx.zeros(); // Refresh boundary force direction
            q = 2.0*params.Clength*(Cells[j].cellradius*sqrt((params.CMwidth-params.CEwidth)*(params.CMwidth-params.CEwidth)/(4.0*params.Clength*params.Clength) +1.0) - params.CMwidth/2.0)/(params.CMwidth-params.CEwidth) - params.PMZheight/2.0 - params.Clength;
            p = -2.0*params.Clength/(params.CMwidth-params.CEwidth);
            yleft = p*Cells[j].pos(1) + q;
            if (Cells[j].pos(0) < yleft) {
              //Interacts with bottom left side of chain zone
              dx(0) = -(params.CMwidth-params.CEwidth);
              dx(1) = -2.0*params.Clength;
              dx_mag = sqrt(dot(dx,dx));
              dy = Cells[j].pos(0) - yleft;
              dif = dy*(params.CMwidth-params.CEwidth)/sqrt(4.0*params.Clength*params.Clength + (params.CMwidth-params.CEwidth)*(params.CMwidth-params.CEwidth));
              F = (dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif)))/dx_mag;
              Cells[j].v = Cells[j].v + F/gamma;
              Cells[j].v_bound = Cells[j].v_bound + F/gamma;
            }

            dx.zeros(); // Refresh boundary force direction
            q = 2.0*params.Clength*(Cells[j].cellradius*sqrt((params.CMwidth-params.CEwidth)*(params.CMwidth-params.CEwidth)/(4.0*params.Clength*params.Clength) +1.0) - params.CMwidth/2.0)/(params.CMwidth-params.CEwidth) - params.PMZheight/2.0 - params.Clength;
            p = -2.0*params.Clength/(params.CMwidth-params.CEwidth);
            yleft = -p*Cells[j].pos(1) + q;
            if (Cells[j].pos(0) < yleft) {
              //Interacts with bottom right side of chain zone
              dx(0) = -(params.CMwidth-params.CEwidth);
              dx(1) = 2.0*params.Clength;
              dx_mag = sqrt(dot(dx,dx));
              dy = Cells[j].pos(0) - yleft;
              dif = dy*(params.CMwidth-params.CEwidth)/sqrt(4.0*params.Clength*params.Clength + (params.CMwidth-params.CEwidth)*(params.CMwidth-params.CEwidth));
              F = (dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif)))/dx_mag;
              Cells[j].v = Cells[j].v + F/gamma;
              Cells[j].v_bound = Cells[j].v_bound + F/gamma;
            }
          }
        }
      }
    }


    if ((Cells[j].pos(0) + Cells[j].cellradius) > params.PMZheight/2.0){
      // Cell interacts with upper boundary
      // Apply vertical returning force  as a function of proximity to boundary
      dx.zeros(); // Refresh boundary force direction
      dx(0) = 1.0;
      dif = params.PMZheight/2.0 - Cells[j].cellradius - Cells[j].pos(0);
      F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
      Cells[j].v = Cells[j].v + F/gamma;
      Cells[j].v_bound = Cells[j].v_bound + F/gamma;
    }

  }
}
