//
//  Boundary2.cpp
//  NeuralCrest
//
//  Created by Dylan Feldner-Busztin on 20/11/2020.
//
//

#include "Boundary3.hpp"
#include <armadillo>
#include <cmath>
#include "cell.hpp"
#include <vector>
#include "MorseForce.hpp"
#include "parameters.hpp"

using namespace std;
using namespace arma;

void Boundary3(vector<cell>& Cells,parameters& params,float& gamma)

{

    // Cells interact with boundary if they are within a cell radius of it.
    // This file is complex and should be tidied up or used with reference to a diagram.
    float dif;
    vec dx = vec(2,fill::zeros);
    vec F = vec(2,fill::zeros);

    for (int j=0; j<params.Nc; j++)

    {

    // File creates boundaries according to this shape
    //
    //                         PMZwidth
    //                   ********************     PMZceiling
    //               A---*------------------*---
    //                   *     D   0  E     *
    //                   *     |      |     *
    //               B---*-----|CMwidth-----*---
    //               C---*******------*******---  PMZ floor
    //                         *      *
    //                         *      *           Chain zone 1
    //                         *      *
    //               F---*******------*******---  MZ ceiling
    //               G---------|------|---------
    //                         |      |      
    //               H--------|CMwidth----------
    //               I---*******------*******---  MZ floor
    //                         *      *
    //                         *      *           Chain zone 2
    //                         *      *

    //float mz_height_to_pmz_height_ratio = params.mz_pmz_ratio;

    float horizontal_line_A     = params.PMZheight/2.0 - Cells[j].cellradius;
    float horizontal_line_B     = -params.PMZheight/2.0 + Cells[j].cellradius;
    float horizontal_line_C     = horizontal_line_B - Cells[j].cellradius;
    float vertical_line_D       = -params.CEwidth/2.0;
    float vertical_line_E       = params.CEwidth/2.0;
    float horizontal_line_F     = horizontal_line_C - params.Clength;
    float horizontal_line_G     = horizontal_line_F - Cells[j].cellradius;
    float horizontal_line_H     = horizontal_line_F - params.PMZheight * params.mz_pmz_ratio + Cells[j].cellradius;
    float horizontal_line_I     = horizontal_line_H - Cells[j].cellradius;



      float& a = Cells[j].a;
      float& De = Cells[j].De;
      Cells[j].v_bound.zeros();


      // According to the diagram:

      // If cell is above line A: PMZceiling
      if ( Cells[j].pos(0) > horizontal_line_A)
          {
              dx.zeros(); // Refresh boundary force direction
              dx(0) = 1.0;
              dif = params.PMZheight/2.0 - Cells[j].cellradius - Cells[j].pos(0);
              F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
              Cells[j].v = Cells[j].v + F/gamma;
              Cells[j].v_bound = Cells[j].v_bound + F/gamma;
          }

      // Else if cell is below line B and above line C:
      else if ( Cells[j].pos(0) < horizontal_line_B && Cells[j].pos(0) > horizontal_line_C )
          {

          // If cell is on the outside of lines D and E: PMZ floor
          if ( Cells[j].pos(1) < vertical_line_D || Cells[j].pos(1) > vertical_line_E)
              {

                  dx.zeros(); // Refresh boundary force direction
                  dx(0) = -1.0;
                  dif = Cells[j].pos(0) + params.PMZheight/2.0 - Cells[j].cellradius;
                  F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
                  Cells[j].v = Cells[j].v + F/gamma;
                  Cells[j].v_bound = Cells[j].v_bound + F/gamma;

              }

          }

      // Else if cell is below line C and above line F: Chain zone 1
      else if ( Cells[j].pos(0) < horizontal_line_C && Cells[j].pos(0) > horizontal_line_F )
          {
              dx.zeros();
              dx(1) = -1.0;

              // Cell interacts with left side of chain zone
              if (Cells[j].pos(1) - Cells[j].cellradius < -params.CEwidth/2.0){

                dif = Cells[j].pos(1) - Cells[j].cellradius + params.CEwidth/2.0;
                F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
                Cells[j].v = Cells[j].v + F/gamma;
                Cells[j].v_bound = Cells[j].v_bound + F/gamma;
              }

              // Cell interacts with right side of chain zone
              if (Cells[j].pos(1) + Cells[j].cellradius > params.CEwidth/2.0){

                dif = params.CEwidth/2.0 - Cells[j].pos(1) - Cells[j].cellradius;
                F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
                Cells[j].v = Cells[j].v - F/gamma;
                Cells[j].v_bound = Cells[j].v_bound - F/gamma;
              }
          }

      // Below line F and above line G: MZ ceiling
          else if ( Cells[j].pos(0) < horizontal_line_F && Cells[j].pos(0) > horizontal_line_G )
          {
              // If cell is on the outside of lines D and E: PMZ floor
              if ( Cells[j].pos(1) < vertical_line_D || Cells[j].pos(1) > vertical_line_E)
                  {

                      // Cell beneath the ceiling of the middle zone rather than the chain opening
                      dx.zeros(); // Refresh boundary force direction
                      dx(0) = 1.0;
                      dif = -params.PMZheight/2.0 - params.Clength - Cells[j].cellradius - Cells[j].pos(0);
                      F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
                      Cells[j].v = Cells[j].v + F/gamma;
                      Cells[j].v_bound = Cells[j].v_bound + F/gamma;

                  }
          }

      // Below line H and above line I: MZ floor
      else if ( Cells[j].pos(0) < horizontal_line_H && Cells[j].pos(0) > horizontal_line_I )
          {

              // If cell is on the outside of lines D and E: PMZ floor
              if ( Cells[j].pos(1) < vertical_line_D || Cells[j].pos(1) > vertical_line_E)
                  {

                      dx.zeros(); // Refresh boundary force direction
                      dx(0) = -1.0;
                      dif = Cells[j].pos(0) + params.PMZheight/2.0 +params.Clength +params.PMZheight - Cells[j].cellradius;
                      F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
                      Cells[j].v = Cells[j].v + F/gamma;
                      Cells[j].v_bound = Cells[j].v_bound + F/gamma;

                  }

          }

      // Below line I: chain zone 2
      else if ( Cells[j].pos(0) < horizontal_line_I )
          {

              dx.zeros();
              dx(1) = -1.0;

              // Cell interacts with left side of chain zone
              if (Cells[j].pos(1) - Cells[j].cellradius < -params.CEwidth/2.0){

                dif = Cells[j].pos(1) - Cells[j].cellradius + params.CEwidth/2.0;
                F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
                Cells[j].v = Cells[j].v + F/gamma;
                Cells[j].v_bound = Cells[j].v_bound + F/gamma;
              }

              // Cell interacts with right side of chain zone
              if (Cells[j].pos(1) + Cells[j].cellradius > params.CEwidth/2.0){

                dif = params.CEwidth/2.0 - Cells[j].pos(1) - Cells[j].cellradius;
                F = dx*2.0*De*a*(exp(-a*dif)-exp(-2.0*a*dif));
                Cells[j].v = Cells[j].v - F/gamma;
                Cells[j].v_bound = Cells[j].v_bound - F/gamma;
              }

          }
    }
}

