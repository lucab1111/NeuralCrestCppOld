//
//  OutputData.cpp
//  NeuralCrest
//
//  Created by Christopher Revell on 19/03/2019.
//
//

#include "OutputData.hpp"
#include <vector>
#include <armadillo>
#include "cell.hpp"
#include "parameters.hpp"
#include <fstream>

using namespace std;
using namespace arma;

void OutputData(char* buffer2,vector<cell>& Cells,float& t, parameters& params, int& nloop, ofstream& outfile, ofstream& outfile2){

  char  buffer[150];       // Dummy string for system calls
  int   PMZcellcount;      // Number of cells within the PMZ region

  PMZcellcount = 0;
  // Write positions to file
  for (int ii=0;ii<params.Nc;ii++){
    outfile << t << " " <<
    Cells[ii].pos(0) << " " <<
    Cells[ii].pos(1) << " " <<
    Cells[ii].v_auto(0) << " " <<
    Cells[ii].v_auto(1) << " " <<
    Cells[ii].v_bound(0) << " " <<
    Cells[ii].v_bound(1) << " " <<
    Cells[ii].cellradius << " " <<
    Cells[ii].label << " " <<
    Cells[ii].type << " " <<
    Cells[ii].notch << " " <<
    Cells[ii].dll4 << " " <<
    params.experimentType << " " <<
    params.Nc << endl;

    if (fabs(Cells[ii].pos(0)) < params.PMZheight/2.0 && fabs(Cells[ii].pos(1)) < params.PMZwidth/2.0){
      PMZcellcount = PMZcellcount+1;
    }
  }

  outfile2 << t << " " << PMZcellcount << endl;

  // Call plotter
  if (params.realTimePlot == 1){
    //sprintf(buffer,"python3 scripts/plottersingle.py %d %d ",nloop, Nc);
    //sprintf(buffer,"python3 scripts/plottersingle.py %d %d %f %f %f %f %f %d ",Nc,nloop,PMZwidth,PMZheight,CEwidth,CMwidth,Clength,chainShape);
    sprintf(buffer,
            "python3 plotting/plottersingle.py %d %d %f %f %f %f %f %d %f ",
            params.Nc,
            nloop,
            params.PMZwidth,
            params.PMZheight,
            params.CEwidth,
            params.CMwidth,
            params.Clength,
            params.chainShape,
            params.mz_pmz_ratio),
    system((string(buffer)+string(buffer2)).c_str());
    nloop = nloop+1;
  }
}
