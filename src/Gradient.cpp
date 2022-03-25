//
//  Gradient - downward force
//  NeuralCrest
//
//  Created by Dylan Feldner-Busztin on 12/10/20.
//
//

#include "Gradient.hpp"
#include <armadillo>
#include <random>
#include "cell.hpp"
#include "parameters.hpp"
#include <vector>

using namespace std;
using namespace arma;

void applyGradient(vector<cell>& Cells,normal_distribution<float>& gaussian,uniform_real_distribution<float>& unif,mt19937_64& gen, parameters& params){

    vec beta = vec(2,fill::zeros); // Vector for gradient component

    // Point at which gradient is zero. Above this, the gradient sends cells downward. Above this point gradient sends cells down
    // The idea with this is that the point where the direction changes may be below the midpoint, at the centre of the notochord
    //float gradientPoint = (params.PMZheight * params.mz_pmz_ratio) /2.0;

    float gradientPoint = 0; // Seeing what happens with cells getting stuck in the middle

	for (int ii=0;ii<Cells.size();ii++){

      // Apply downward force above notochord midline
        if ( Cells[ii].pos(0) > (- params.PMZheight/2.0 - params.Clength - (params.PMZheight * params.mz_pmz_ratio)/2.0 - gradientPoint))
        {

            beta(0) = cos(M_PI);
            beta(1) = sin(M_PI);

            if(Cells[ii].type == 2)
            {
              // Use the normal distribution to find the magnitude of movement in this direction
              Cells[ii].v = Cells[ii].v + fabs(gaussian(gen))*beta*Cells[ii].gradientSensitivity;
            }

        }
       else if ( Cells[ii].pos(0) < (- params.PMZheight/2.0 - params.Clength - (params.PMZheight * params.mz_pmz_ratio)/2.0 - gradientPoint) ){

            // Apply upward force below the notochord midline

            beta(0) = cos(0);
            beta(1) = sin(0);

            if(Cells[ii].type == 2)
            {
              // Use the normal distribution to find the magnitude of movement in this direction
              Cells[ii].v = Cells[ii].v + fabs(gaussian(gen))*beta*Cells[ii].gradientSensitivity;
            }

        }


	}
}
