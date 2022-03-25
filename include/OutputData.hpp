//
//  OutputData.hpp
//  NeuralCrest
//
//  Created by Christopher Revell on 19/03/2019.
//
//

#ifndef OutputData_hpp
#define OutputData_hpp

#include <stdio.h>
#include <vector>
#include <armadillo>
#include "cell.hpp"
#include "parameters.hpp"
#include <fstream>

void OutputData(char* buffer2,std::vector<cell>& Cells, float& t, parameters& params, int& nloop, std::ofstream& outfile, std::ofstream& outfile2);

#endif /* OutputData_hpp */
