//
// parameters.hpp
//
// Created by Dylan Feldner-Busztin on 10/11/2020
//
//

#ifndef parameters_hpp
#define parameters_hpp

class parameters{

    public:
        parameters(int& Nc, float& zeta_mag, float& cellradius, float& PMZwidth, float& PMZheight, float& CEwidth, float& CMwidth, float& Clength, float& t_max, float& dt, float& output_interval, int& chainShape, int& realTimePlot, int& experimentType, float& leader_k, float& leader_De, float& leader_autonomousMag, float& leader_interactionThreshold, float& leader_gradientSensitivity, float& leader_size, float& follower_k, float& follower_De, float& follower_autonomousMag, float& follower_interactionThreshold, float& follower_gradientSensitivity, int& slurm_array, int& runID, float& mz_pmz_ratio);
        int                 Nc;
        float               zeta_mag;
        float               cellradius;
        float               PMZwidth;
        float               PMZheight;
        float               CEwidth;
        float               CMwidth;
        float               Clength;
        float               t_max;
        float               dt;
        float               output_interval;
        int                 chainShape;
        int                 realTimePlot;
        int                 experimentType;
        float               leader_k;
        float               leader_De;
        float               leader_autonomousMag;
        float               leader_interactionThreshold;
        float               leader_gradientSensitivity;
        float               leader_size;
        float               follower_k;
        float               follower_De;
        float               follower_autonomousMag;
        float               follower_interactionThreshold;
        float               follower_gradientSensitivity;
        int                 slurm_array;
        int                 runID;
        float               mz_pmz_ratio;
};


#endif
