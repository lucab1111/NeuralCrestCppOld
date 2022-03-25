//
//  cell.hpp
//  NeuralCrest
//
//  Created by Christopher Revell on 19/11/2018.
//
//

#ifndef cell_hpp
#define cell_hpp

#include <armadillo>

class cell {
private:
public:
  cell(const int& celllabel,const float& initialx,const float& initialy,const float& radius, const int& typespecifier, const float& stiffness, const float& attractiveness,const float& vauto,const float& cellInteractionThreshold, const float& follower_gradientSensitivity);
  arma::vec      pos;                   // Cell position
  arma::vec      v;                     // Cell velocity
  arma::vec      v_auto;                // Autonomous velocity
  arma::vec      v_bound;               // Boundary velocity
  arma::Col<int> neighbours;            // List of this cell's neighbours
  float          cellradius;            // Typical radius
  int            label;                 // Label of this cell
  int            Nneighbours;           // Number of neighbours around this cell
  int            type;                  // =0 if cell is a follower; =1 if cell is a leader
  float          k;                     // For Morse potential. Measure of cell stiffness.
  float          De;                    // For Morse potential. Measure of chemotactic attractiveness.
  float          a;
  float          autonomousMag;
  float          interactionThreshold;
  float          morseForceMag;         // Magnitude of morse force experienced by cell
  int            withinThresholdNeighbours; // Number of neighbours within threshold distance
  float          gradientSensitivity;   // How much downward force cell experiences

  double          dll4; //internal delta-like4 level
  double          notch; //internal activated notch level
  
  ~cell();                              // Destructor
protected:

};


#endif /* cell_hpp */
