import io
import numpy as np
import random
import math
import util
import time


class StandardNet6Areas:
    NXAREAS = 6
    NYAREAS = 1
    NAREAS = NXAREAS * NYAREAS

    AREA1 = 0
    AREA2 = 1
    AREA3 = 2
    AREA4 = 3
    AREA5 = 4
    AREA6 = 5
    AREA7 = 6

    P = 12  # no. of differnt pattern-ntuples to be learnt

    CA_THRESH = 0.5  # threshold used to define a CA

    # minimum activity required for an area to be considered responsive (to calculate CAs)
    MIN_CELLRATE = 0.10

    ## Layers dimensions ##

    N11 = 25
    N12 = 25
    N1 = (N11*N12)   # no. of cells in 1 area
    NSQR1 = (N1*N1)  # no. of (possible) synapses between 2 areas

    NONES = 19  # no. of "1"s in each random input pattern

    STEPSIZE = 0.5  # "delta-t" of the simulation

    ZOOMFACT = 5       # Size (pixels) of side of square for 1 cell
    ZOOMPATFACT = 4    # cell size (pix) for CA patterns windows
    OVRLPZOOMFACT = 5  # cell size (pix) for CA overlap

    ## Time constants ##

    TAU1 = 2.5      # for EPSPs
    TAU2 = 5.0      # for IPSPs
    TAUSLOW = 12.0  # for global/slow inhibition

    ADAPTSTRENGTH = .01  # Impact of adaptation (scaling factor)
    TAUADAPT = 15.0      # "speed" of f.rate integration into adapt.

    TAU_AVG_RATES = 10.0  # "speed" of f.rate integration into avg.
    AVG_RATES_TIME = 30   # length of period over which avg. is taken

    ##  Random firing activity generation ##

    r0 = 0.003
    r1 = 0.5

    def SFUNC(self, x: float):
        return util.bool_noise(self.r0+self.r1*util.TLIN(x))

    ## Rate functions of different cells ##

    @staticmethod
    def FUNCI(x: float):
        "For inhibitory cells"
        return util.TLIN(x)

    @staticmethod
    def FUNC(x: float):
        "For excitatory cells"
        return util.RAMP(x)

    ## Kernels & synaptic values ##

    NFFB1 = 19  # x/y sizes of forward & backward projections
    NFFB2 = 19
    NREC1 = 19  # x/y sizes of recurrent projections
    NREC2 = 19
    NINH1 = 5   # x/y sizes of inhibitory projections
    NINH2 = 5

    ## X- and Y-direction standard deviation of the Gaussian for.. ##

    SIGMAX = 6.5      # FF/BB projections
    SIGMAY = 6.5
    SIGMAX_REC = 4.5  # REC. projections
    SIGMAY_REC = 4.5
    SIGMAX_INH = 2.0  # INHIB. projections
    SIGMAY_INH = 2.0

    J_PROB = .28      # Gauss. centre PROB. (FF & FB kernels)
    J_REC_PROB = .15  # Gauss. centre PROB. (REC. kernels)
    # Gauss. centre WEIGHT (inhib. kernels) (This has impact on how "deep" activity penetrates the middle layers of the net)
    J_INH_INIT = .295
    J_UPPER = 0.1     # upper limit for initial synaptic WEIGHTs

    ## Synaptic bounds; max and min synaptic efficacies ##

    JMIN = .00000001  # MUST be greater than NO_SYNAPSE
    JMAX = .225       # cf. J_INH_INIT, LTP_THRESH     <<<<----

    ## LEARNING / synaptic thresholds ##

    LTP_THRESH = 0.15  # Postsynaptic pot. required for LTP
    LTD_THRESH = 0.15  # Postsynaptic pot. required for LTD
    F_THRESH = 0.05    # Presyn. firing rate required for LTP/LTD

    # NO_SYNAPSE is the weight that synapses that should NOT exist are # 
    # initialised to (these synapses shouold remain FIXED: no learning) #

    NO_SYNAPSE = 0.0

    # File names for Saving / Loading net data #

    NET_WR = "net%d.dat"
    NET_RD = "net.dat"
    CA_WR = "CA-structure.txt"

    ## For AUTOMATED TRAINING of the net ##

    PAUSE_TIME = 30      # Duration of pause betw. inputs (time-steps)
    INPUT_TIME = 16      # Duration of input presentation (time-steps)
    SAVE_CYCLE = 500     # Net is saved every SAVE_CYCLE input pres.
    LEARN_RATE = 8       # learning rate applied during training
    TOT_TRAINING = 4000  # Tot. no. patt. presentations 4 training

    SLOWAREA1 = AREA1    # 1st area used for global inhib. decay check
    MAXINHIB1 = 0.75     # max. inhib. in SLOWAREA1 b4 input switch
    SLOWAREA2 = AREA3    # 2nd area used for glob. inhib. decay check
    MAXINHIB2 = 0.65     # max. inhib. in SLOWAREA2 b4 input switch

    ROW_1 = 1     # Codes for multiplexing the sensory/motor input
    ROW_2 = 2     # to different "rows" of the network
    ALL_ROWS = 3  # (row 1 == DORSAL, row 2 == VENTRAL)

    ## For AUTOMATED TESTING of the net ##

    TESTING = False           # TRUE <=> runs in automatic testing mode
    GINHIB_TESTING = 0.35     # g.inh. level required to start testing
    GINHIB_TEST_AREA = AREA3  # area where to check g.inh. level
    DATA_WR = "DataOut.txt"   # where to save data during testing
    STIM_DURATION = 2         # (in simulation time-steps)
    PRINTSTEPS = 25           # No. of steps to be recorded (per trial)
    TOT_REPET = 12            # Number of CA stimulation repetitions
    STOPTEST_PHASE = 6        # If test_phase == 6, testing will stop
    STARTTEST_PHASE = 1       # If test_phase == 1, testing will start

    ## GLOBAL dynamic variables ##

    stp: int = 0,             # Simulation TIME-STEP counter
    last_stp: int = 0,        # 4 TRAINING: last time-step of input switch
    training_phase: int = 0,  # 4 TRAINING: current phase (PAUSE or INPUT)
    stps_2b_avgd: int = 0,    # 4 TRAINING: f.rates averaging counter (# steps)
    test_phase: int = 0,      # 4 TESTING: current testing phase
    stimRepet: int = 0,       # 4 TESTING: number of repeated stimulations
    stimCA: int = 0	          # 4 TESTING: CA currently being stimulated

    freq_distrib: util.VectorType  # array containing freq. of pattern presentations

    noise_fac: float = 0.0,     # amplitude of spontaneous firing rate
    total_output: float = 0.0,  # Sum of ALL cell's OUTPUT (firing rate)

    pot: util.VectorType        # (Entire network's) excitat. cells' potentials
    inh: util.VectorType        # inhib. cells' potentials
    adapt: util.VectorType      # adaptation of all excit cells
    rates: util.VectorType      # firing rates (output) of excitatory cells
    # time-average of cells' f.rates (pattern specific)
    avg_patts: util.VectorType
    # overlaps between emerging CA patts. (in each area)
    ca_ovlps: util.VectorType
    # "   " betw. current activity & CA patts. ("   " )
    ovlps: util.VectorType

    # current inputs (NYAREAS areas) to "left" (sensory)
    sensInput: util.VectorType
    # current inputs (NYAREAS areas) to "right" (motor)
    motorInput: util.VectorType

    # Fixed input patterns (NYAREAS x P) to the left
    sensPatt: util.VectorType
    # Fixed input patterns (NYAREAS x P) to the right
    motorPatt: util.VectorType

    # Post-syn. potentials in input to area
    linkffb: util.VectorType
    linkrec: util.VectorType
    linkinh: util.VectorType
    tempffb: util.VectorType    # auxiliary (EPSPs from diff. areas)
    clampSMIn: util.VectorType  # Incoming sesnory OR motor input to one area

    slowinh: util.VectorType  # slow inhib (1 cell per area)

    diluted: util.VectorType        # All "dead" cells
    above_thresh: util.VectorType   # Cells CURRENTLY firing above CA_THRESHold
    above_hstory: util.VectorType   # "history" of above_thresh vector activation

    ca_patts: util.bVectorType   # CA patterns emerging as a result of the training

    # Sum of synaptic weight *increase* (in each area)
    tot_LTP: util.VectorType
    # Sum of synaptic weight *decrease* (in each area)
    tot_LTD: util.VectorType

    fi: io.TextIOWrapper  # file handle for writing data during TESTING

    # Matrix specifying the network's Connectivity structure #
    # A "1" at coord. (x,y) means Area #x ==> Area #y
    # Note: keeping this 1d in the spirit of "like for like" translation
    K: util.bVectorType = np.array([
        # (to area)
        # 1, 2, 3, 4, 5, 6
        1, 1, 0, 0, 0, 0,  # 1
        1, 1, 1, 0, 0, 0,  # 2
        0, 1, 1, 1, 0, 0,  # 3
        0, 0, 1, 1, 1, 0,  # 4
        0, 0, 0, 1, 1, 1,  # 5
        0, 0, 0, 0, 1, 1   # 6 (from area)
    ])

    # ALL KERNELS of the network are (linearly) stored in J[].
    # Each "element" is a vector of NSQR1 values (syn. weights)
    # J[Row,Col] = kernel/links FROM area (Row) TO area (Col)
    J: util.VectorType

    # Contains the ONE and only inhibitory (Gauss.) kernel
    Jinh: util.VectorType

    def main_init(self):
        """
        main_init() is called when simulation PROGRAM is started. It does
        all initialisations the need to be done only ONCE at startup, eg.
        getting memory for data structures, init. random numbers, etc.

        Note: we could easily move this initialise these values in-line above, but I'm
        leaving as is, in the spirit of "like for like" translation
        """
        # Random numbers generation
        random.seed(time.time())
        # if STEPSIZE=0.5, noise_fac ~= 6.93
        self.noise_fac = math.sqrt(24.0 / self.STEPSIZE)

        # Membr. pot. of ALL excit. cells
        self.pot = util.Get_Vector(self.NAREAS * self.N1)
        # Firing rates of ALL excit. cells
        self.rates = util.Get_Vector(self.NAREAS * self.N1)
        # M. potential of ALL inhib. cells
        self.inh = util.Get_Vector(self.NAREAS * self.N1)
        # patt.-specific f.rates avg.
        self.avg_patts = util.Get_Vector(self.NAREAS * self.N1 * self.P)
        # emerging Cell Assemblies
        self.ca_patts = util.Get_bVector(self.NAREAS * self.N1 * self.P)
        # Per-area overlaps betw. CAs
        self.ca_ovlps = util.Get_Vector(self.NAREAS * self.P * self.P)
        # Ovlps. betw. CAs & current activity
        self.ovlps = util.Get_Vector(self.NAREAS * self.P)

        # M. potential of G. Inhib. cells
        self.slowinh = util.Get_Vector(self.NAREAS)
        # Adaptation of ALL excit. cells
        self.adapt = util.Get_Vector(self.NAREAS * self.N1)
        # Lesion mask (1 <=> lesioned)

        self.diluted = util.Get_bVector(self.NAREAS * self.N1)

        # cells CURRENTLY > thresh
        self.above_thresh = util.Get_bVector(self.NAREAS * self.N1)
        self.above_hstory = util.Get_bVector(
            self.NAREAS * self.N1 * self.P)  # above_thresh's history
        # (pattern specific)
        self.tot_LTP = util.Get_Vector(self.NAREAS)
        self.tot_LTD = util.Get_Vector(self.NAREAS)

        self.sensInput = util.Get_bVector(self.NYAREAS * self.N1)
        self.motorInput = util.Get_bVector(self.NYAREAS * self.N1)

        self.sensPatt = util.Get_bVector(self.NYAREAS*self.P*self.N1)
        self.motorPatt = util.Get_bVector(self.NYAREAS*self.P*self.N1)

        # note: in the C version there is `freq_distrib = (int*)calloc( P, sizeof(int) )` - Get_bVector is not used
        self.freq_distrib = util.Get_bVector(self.P)  # array of freq. pres.

        # Kernels: we allocate bigger arrays than we actually need (each
        # el. can contain up to NSQR1 synapses = all-to-all connectivity) #

        self.J = util.Get_Vector(self.NAREAS * self.NAREAS *
                                 self.NSQR1)  # NAREAS*NAREAS couplings
        # 1 inhib. kernel with at most self.N1 links
        self.Jinh = util.Get_Vector(self.N1)

        # Vectors of post-synapt. pot. incoming to each cell of one area #
        # EPSPs from OTHER (between-) areas
        self.linkffb = util.Get_Vector(self.N1)
        # EPSPs from THIS area (recurrent)
        self.linkrec = util.Get_Vector(self.N1)
        # Inh.Post-Syn. Pot from inhib. layer
        self.linkinh = util.Get_Vector(self.N1)
        # auxiliary (used for temp. EPSPs)
        self.tempffb = util.Get_Vector(self.N1)
        # "Clamp" input from sensorimotor patt.
        self.clampSMIn = util.Get_Vector(self.N1)

    def randomise_net_activity(self):
        """
        For unit testing: generate activity vectors to pre-empt resetNet
        """
        self.pot = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.inh = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.adapt = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.rates = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.slowinh = util.Get_Random_Vector(self.NAREAS)
        self.tot_LTP = util.Get_Random_Vector(self.NAREAS)
        self.tot_LTD = util.Get_Random_Vector(self.NAREAS)
        self.above_hstory = util.Get_Random_Vector(
            self.NAREAS * self.N1 * self.P)

        self.total_output = random.uniform(1, 1000)

    def resetNet(self):
        """
        Reset completely the network activity (the synaptic weights are 
        left untouched). Recent "history" of TESTING activity is erased.

        Note: we modify the value of the mutable vector directly inside the function
        Note: I don't think we need to pass the len in here, but I'll leave it for now, 
        in the spirit of "like for like" translation
        """
        util.Clear_Vector(self.NAREAS * self.N1, self.pot)
        util.Clear_Vector(self.NAREAS * self.N1, self.inh)
        util.Clear_Vector(self.NAREAS * self.N1, self.adapt)
        util.Clear_Vector(self.NAREAS * self.N1, self.rates)
        util.Clear_Vector(self.NAREAS, self.slowinh)
        util.Clear_Vector(self.NAREAS, self.tot_LTP)
        util.Clear_Vector(self.NAREAS, self.tot_LTD)
        util.Clear_bVector(self.NAREAS * self.N1 * self.P, self.above_hstory)

        self.total_output = 0.0

    @staticmethod
    def init():
        """
        init() is called whenever "INIT" or "RUN" buttons in the GUI are 
        pressed; it initialises individual simulation runs               
        """

        return

    @staticmethod
    def step():
        """
        MAIN  "STEP" FUNCTION, executed at each sim. step
        """
        return

    def display_K(self):
        """
        Visualise (as text output) the links of connectivity matrix K[].
        """
        areaConnections = dict()
        for i in range(self.NAREAS):
            areaConnectsTo = []
            print("Area %d receives from ", i+1)
            for j in range(self.NAREAS):
                if self.K[self.NAREAS*j+i]:
                    areaConnectsTo.append(j+1)
                    print(" %d", j+1)
            areaConnections[i+1] = areaConnectsTo
            print(" \n")
        return areaConnections

    # @todo unit test
    def compute_CAoverlaps(self):
        """
        Compute the PxP overlaps between the emergin Cell Assemblies
        """
        for area in range(self.NAREAS):
            for i in range(self.P):
                for j in range(self.P):
                    self.ca_ovlps[self.P*(self.P*area+i) + j] = bbSkalar(self.N1, self.ca_patts[self.N1*(
                        self.NAREAS*i+area)], self.ca_patts[self.N1*(self.NAREAS*j+area)]) / self.NONES

    # @todo unit test
    def write_CApatts(self):
        """
        Write no. of CA-cells of all CA.s to file (for all CA.s & areas). 
        CAs are computed by the above routine "compute_CApatts(thresh)".
        """
        with open(self.CA_WR, "a") as fiCA:
            if fiCA is None:
                print(
                    "\n ERROR: Could not open file '{}' for writing.\n".format(self.CA_WR))
            else:
                for i in range(self.P):
                    fiCA.write("\n CA #{}: ".format(i + 1))
                    for area in range(self.NAREAS):
                        fiCA.write("{} ".format(
                            sum(self.N1, self.ca_patts[self.N1*(self.NAREAS*i+area)])))
                print("\n\n")

    # @todo unit test
    @staticmethod
    def gener_random_bin_patterns(n: int, nones: int, p: int, pats: np.ndarray):
        """Creates p binary random vectors of length n, where "nones" units are="1" 
        at random positions. "pats" is the array of vectors/patts

        Keyword arguments:
        n     -- IN: no. cells per pattern
        nones -- IN: no. of "1"s per patt.
        p     -- IN: tot. no. patterns
        pats  -- OUT: the array of patterns
        """
        util.Clear_Vector(n*p, pats)  # Clear content of ALL patterns

        for j in range(p):  # For each pattern
            temp_pat = pats[n * j:n * (j + 1)]  # Get slice for current pattern
            for i in range(nones):  # For all cells of this pattern
                temp_pat[random.randint(0, n - 1)] = 1

            # It may be that two or more "1"s happen to coincide...
            while sum(temp_pat) < nones:  # Inefficient, but fast enough
                temp_pat[random.randint(0, n - 1)] = 1

    # @todo unit test
    def compute_CApatts(self, threshold):
        """
        Compute the emerging Cell Assemblies using specified threshold

        Keyword arguments:
        threshold -- IN: threshold used to define a CA
        """
        for area in range(self.NAREAS):  # For all areas
            for i in range(self.P):  # for all input pattern pairs
                # Get firing rate of maximally responsive cell in current area
                max_act = max(self.avg_patts[self.N1*(self.NAREAS*i+area)])

                # Check if there is at least 1 cell strongly responsive
                if max_act >= self.MIN_CELLRATE:
                    # If cell rate > threshold, set cell to 1 in 'ca_patts'
                    util.Fire(self.N1, self.avg_patts[self.N1*(self.NAREAS*i+area)], threshold*max_act,
                              self.ca_patts[self.N1*(self.NAREAS*i+area)])
                # Else: NO cells are set to 1 in the 'ca_patts' vector

    # @todo unit test
    @staticmethod
    def init_gaussian_kernel(nx: int, ny: int, mx: int, my: int, J: np.ndarray, sigmax: float, sigmay: float, ampl: float):
        """Initializes nx*ny kernels of size mx*my in the Array J with Gaussian 
        profile - sigmax and sigmay are standard deviations of the Gaussian in x 
        and y direction; ampl is scaling factor (= amplit. of the Gaussian function 
        at the center, point (0,0) ).

        Keyword arguments:
        nx, ny          -- IN: area size (1cell<=>1kernel)
        mx, my          -- IN: kernel size
        J               -- OUT: the kernels (linearised)
        sigmax, sigmay  -- IN: std. deviations
        ampl            -- IN: value at Gaussian center
        """
        cx = mx // 2
        cy = my // 2

        h1 = 1.0 / (sigmax * sigmax)
        h2 = 1.0 / (sigmay * sigmay)

        # Set up kernel (0,0)
        for x in range(mx):
            for y in range(my):
                h = (x - cx) * (x - cx) * h1 + (y - cy) * (y - cy) * h2
                J[y * mx + x] = ampl * math.exp(-h)

        # Copy kernel (0,0) to other locations
        mm = mx * my
        for i in range(1, nx * ny):
            J[i * mm: (i + 1) * mm] = J[:mm]

    # @todo unit test
    def init_patchy_gauss_kern(self, nx: int, ny: int, mx: int, my: int, J: np.ndarray, sigmax: float, sigmay: float, prob: float, upper: float):
        """This routine initializes nx*ny kernels of size mx*my in the Array
        J such that the probability of creating a synapse follows a Gaus-
        sian distribution falling with distance from center with standard
        deviations sigmax and sigmay in x and y direction and probability
        "prob" for the synapses at the center. If a synapse is present,  
        its value will be a random no. in range [0,upper[. Otherwise, the
        synaptic value is set to NO_SYNAPSE (indicating a FIXED synapse).

        Keyword arguments:
        nx, ny          -- IN: area size (1kern/cell)
        mx, my          -- IN: kernel size
        J               -- OUT: the actual Kernels
        sigmax, sigmay  -- IN: std. deviations
        prob            -- IN: IN: Gaussian amplitude
        upper           -- IN: upper synaptic value
        """
        # Checks that max. probability is within bounds
        if prob < 0.0 or prob > 1.0:
            print("ERROR: init_<..>_kernel() probab. not in [0,1]")
            exit(-1)

        # First, we compute the probabilities...
        self.init_gaussian_kernel(nx, ny, mx, my, J, sigmax, sigmay, prob)

        # ...then transform them into the requested synaptic values.
        for i in range(nx * ny * mx * my):
            if random.random() < J[i]:
                # random.uniform(0, upper) could be used instead of upper*random.random()
                J[i] = upper * random.random()
            else:
                J[i] = 0  # NO_SYNAPSE

    # @todo unit test
    def train_projection_cyclic(self, pre: np.ndarray, post_pot: np.ndarray, J: np.ndarray, nx: int, ny: int, mx: int, my: int, hrate: float, totLTP: float, totLTD: float):
        """Train" all the synapses connecting area X to area Y (incl. X==Y)

        Keyword arguments:
        pre       -- IN: area X cells' firing rates (output)
        post_pot  -- IN: area Y cells' memb. potentials
        J         -- IN/OUT: all the kernels connecting X to Y
        nx, ny    -- IN: area dimensions (2 areas of same size)
        mx, my    -- IN: kernels' x and y's dimensions
        hrate     -- IN: learning rate (weight increm/decrem.)
        totLTP    -- OUT: tot. amount of LTP
        totLTD    -- OUT: tot. amount of LTD
        """
        kx2 = mx // 2
        ky2 = my // 2
        mxy = mx * my
        kern = J

        for i in range(ny):  # For all cells in area Y
            for j in range(nx):  # For all cells in area X
                ij = i * nx + j  # "ij" counts total number of cells
                for k in range(-ky2, ky2 + 1):  # For all links of 1 kernel
                    for l in range(-kx2, kx2 + 1):  # "kern" counts total number of links
                        m = ((i + k + ny) % ny) * nx + \
                            (j + l + nx) % nx  # Get index of cell in X

                        # Check if synapse considered "exists" (i.e., is not equal to NO_SYNAPSE)
                        if kern[0] != self.NO_SYNAPSE:
                            # Synapse exists; update its weight using learning rule

                            # Get pre-synaptic activity (firing rate)
                            pre_D = pre[m]

                            # Check if post-synaptic potential is above LTP threshold
                            if post_pot[ij] > self.LTP_THRESH:
                                if pre_D > self.F_THRESH:  # Is there sufficient pre-synaptic activity?
                                    if kern[0] < self.JMAX:  # Not yet reached MAX synapse weight
                                        kern[0] += hrate  # Homosynaptic LTP
                                        # Update total amount of LTP
                                        totLTP[0] += hrate
                                else:  # pre_D <= F_THRESH
                                    if kern[0] > self.JMIN:  # Reached MIN synapse weight
                                        # "low"-homosynaptic or heterosynaptic LTD
                                        kern[0] -= hrate
                                        # Update total amount of LTD
                                        totLTD[0] += hrate
                                        if kern[0] < self.JMIN:  # Make sure not to go below JMIN
                                            kern[0] = self.JMIN
                            else:  # post_pot <= LTP_THRESH
                                # Are post_pot and pre_D right for LTD?
                                if pre_D > self.F_THRESH and post_pot[ij] > self.LTD_THRESH and kern[0] > self.JMIN:
                                    kern[0] -= hrate  # Homosynaptic LTD
                                    # Update total amount of LTD
                                    totLTD[0] += hrate
                                    if kern[0] < self.JMIN:  # Make sure not to go below JMIN
                                        kern[0] = self.JMIN

                        kern = kern[1:]  # Move to the next synaptic link
