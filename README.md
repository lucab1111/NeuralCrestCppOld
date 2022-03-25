# NeuralCrest

Compile with `make`.

Run with `./NeuralCrest <Nc> <zeta_mag> <cellradius> <PMZwidth> <PMZheight> <CEwidth> <CMwidth> <Clength> <t_max> <dt> <output_interval> <chainShape> <realTimePlot> <ExperimentType> <leader_k> <leader_De> <leader_autonomousMag> <leader_interactionThreshold> <leader_interactionThreshold> <leader_gradientSensitivity> <leader_size> <follower_k> <follower_De> <follower_autonomousMag> <follower_interactionThreshold> <follower_gradientSensitivity> <slurm_array_task> <runID> <mz_pmz_ratio>`
eg. `./NeuralCrest 6 0.035 0.13 1 0.52 0.4 0.4 1 2000 0.1 10 3 1 1 0.03 9e-05 3e-06 1 0 0.13 0.01 3e-05 1.1e-07 1 0 1 639 0.5`

Or through one of the Python run files `python3 experiments/runSingleContol_1_3.py `


* Nc = Number of cells in pre-migratory zone.
* zeta_mag = Magnitude of stochastic component. Term of the Langevin equation, which controls cell dynamics. This varies the amount of random jiggle in cell movements.
* cellradius =  Typical cell radius.
* PMZwidth = Width of pre-migratory zone in arbitrary units (set at 1.0).
* PMZheight = Height of pre-migratory zone in arbitrary units (measured to be 0.5).
* CEwidth = Width of chain entrance zone in arbitrary units (measured to be 0.25).
* CMwidth = Width of the mid point of the chain zone.
* Clength = Distance between PMZ and the mid point of the chain zone.
* t_max = Total run time in arbitrary units.
* dt = Time interval between iterations.
* output_interval = Time interval between data outputs.
* chainShape = Flag controlling whether the chain zone is straight, a steadily widening quadrilateral, straight with a diamond mid point or has a rectangular gap in the middle.
* realTimePlot = Flag controlling whether results are plotted as the simulation runs (1) or not plotted (0).
* ExperimentType = Flag controlling conditions of the run (e.g., how many leaders there are or ablation of a cell)
* leader_k = Leader cell spring constant near equilibrium (parameter of Morse potential). You can think of this as the stiffness of the cells. Low k means the cells are * squishier.
* leader_De = Leader depth of potential well (parameter of Morse potential). Greater De means greater range of coattraction. You can think of this as the amount of * chemotactic attraction signal released by each cell.
* leader_autonomousMag = Leader cell magnitude of autonomous cell velocity.
* leader_interactionThreshold = Leader cell multiples of cellradius beyond which neighbours no longer cause polarisation by contact inhibition.
* leader_gradientSensitivity = Extent to which a leader cell's movement is influenced by a downward force simulating a chemotactic gradient.
* leader_size = Leader cellradius.
* follower_k = Follower cell spring constant near equilibrium (parameter of Morse potential). You can think of this as the stiffness of the cells. Low k means the cells are squishier.
* follower_De = Follower depth of potential well (parameter of Morse potential). Greater De means greater range of coattraction. You can think of this as the amount of chemotactic attraction signal released by each cell.
* follower_autonomousMag = Follower cell magnitude of autonomous cell velocity.
* follower_interactionThreshold = Follower cell multiples of cellradius beyond which neighbours no longer cause polarisation by contact inhibition.
* follower_gradientSensitivity = Extent to which a leader cell's movement is influenced by a downward force simulating a chemotactic gradient.
* slurm_array_task = Input used to indicate which slurm array this run is coming from.
* run = Randomly generated number used to prevent files ending up with the same name and replacing one another.
* mz_pmz_ratio = Ratio of the middle zone height relative to the PMZ height.

Two different visualisations available. Change between the two by changing `visualisationMode` in `scripts/plottersingle.py` between `0` and `1`.

__Model setup__

* Cells modelled as point particles moving by over-damped Langevin dynamics.
* Cells interact with nearest neighbours via local Morse potential.
* Initial cell positions are allocated randomly at the start of the simulation.
* Morse potential models volume exclusion - cells push away from each other at short distances - and chemoattraction ("coattraction") at longer distances - cells pull together when separated by longer distances. Two paremeters of the Morse potential - k and De - are supplied at command line.
* Nearest neighbours identified by Delaunay triangulation.
* Typical cell radius set such that 12 cells exist within the premigratory zone. Typical cell radius and premigratory zone dimensions supplied at command line.
* Width of chain migration zone suppled at command line.
* Boundary of premigratory zone and chain migration zone applies a repulsive Morse potential to cells within a cell radius of the boundary.
* Cells exhibit autonomous motion with magnitude supplied at command line.
* Direction of autonomous motion determined by contact inhibition from neighbours and boundary. Cell moves into largest space between neighbours with velocity proportional to square of angle into which it moves and supplied autonomous magnitude parameter.
* Only neighbours within a threshold distance are considered for contact inhibition. This threshold is supplied as a multiple of the typical cell radius at the command line.
* Cells with no neighbours within this threshold distance cease autonomous motion.

__Dependencies:__

* Requires Armadillo linear algebra package. Install with Homebrew: `brew install armadillo`
* Plotter requires python3, numpy, scipy, and matplotlib. Install python3 with homebrew or anaconda. Install packages with pip or anaconda: eg "pip install numpy".
* Animation requires Imagemagick. Install with Homebrew: `brew install imagemagick`.
* Need to create a subdirectory named `output` within the base directory of the repository. Run `mkdir output`.

On Mac M1
* `export CPATH=/opt/homebrew/include`
* `export LIBRARY_PATH=/opt/homebrew/lib`
* `brew install llvm`