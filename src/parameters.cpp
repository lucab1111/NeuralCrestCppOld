//
// parameters.cpp
//
// Created by Dylan Feldner-Busztin on 10/11/2020
//
//

#include "parameters.hpp"

parameters::parameters(int& in_Nc, float& in_zeta_mag, float& in_cellradius, float& in_PMZwidth, float& in_PMZheight, float& in_CEwidth, float& in_CMwidth, float& in_Clength, float& in_t_max, float& in_dt, float& in_output_interval, int& in_chainShape, int& in_realTimePlot, int& in_experimentType, float& in_leader_k, float& in_leader_De, float& in_leader_autonomousMag, float& in_leader_interactionThreshold, float& in_leader_gradientSensitivity, float& in_leader_size, float& in_follower_k, float& in_follower_De, float& in_follower_autonomousMag, float& in_follower_interactionThreshold, float& in_follower_gradientSensitivity, int& in_slurm_array, int& in_runID, float& in_mz_pmz_ratio){

    Nc                              = in_Nc;
    zeta_mag                        = in_zeta_mag;
    cellradius                      = in_cellradius;
    PMZwidth                        = in_PMZwidth;
    PMZheight                       = in_PMZheight;
    CEwidth                         = in_CEwidth;
    CMwidth                         = in_CMwidth;
    Clength                         = in_Clength;
    t_max                           = in_t_max;
    dt                              = in_dt;
    output_interval                 = in_output_interval;
    chainShape                      = in_chainShape;
    realTimePlot                    = in_realTimePlot;
    experimentType                  = in_experimentType;
    leader_k                        = in_leader_k;
    leader_De                       = in_leader_De;
    leader_autonomousMag            = in_leader_autonomousMag;
    leader_interactionThreshold     = in_leader_interactionThreshold;
    leader_gradientSensitivity      = in_leader_gradientSensitivity;
    leader_size                     = in_leader_size;
    follower_k                      = in_follower_k;
    follower_De                     = in_follower_De;
    follower_autonomousMag          = in_follower_autonomousMag;
    follower_interactionThreshold   = in_follower_interactionThreshold;
    follower_gradientSensitivity    = in_follower_gradientSensitivity;
    slurm_array                     = in_slurm_array;
    runID                           = in_runID;
    mz_pmz_ratio                    = in_mz_pmz_ratio;
}
