//
//  OpenFiles.hpp
//
//  Created by Christopher Revell on 08/02/2019.
//
//

#ifndef OpenFiles_hpp
#define OpenFiles_hpp

#include "parameters.hpp"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>
#include <ctime>

void OpenFiles(char* buffer,std::vector<std::ofstream>& files, parameters& params);

#endif
