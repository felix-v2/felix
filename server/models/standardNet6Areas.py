import io
import numpy as np
import random


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
    # @todo
    # define SFUNC(_x) bool_noise( r0+r1*TLIN(_x) )

    ## Rate functions of different cells ##

    # @todo
    # define FUNCI(x) TLIN(x)   // For inhibitory cells
    # define FUNC(x)  RAMP(x)   // For excitatory cells
    # define SIGMOID(_x) ( 1.0 / ( 1.0+exp(-2.0*(_x)) ) )   // ? is this used?..

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

    freq_distrib: list = []  # array containing freq. of pattern presentations

    noise_fac: float = 0,    # amplitude of spontaneous firing rate
    total_output: float = 0  # Sum of ALL cell's OUTPUT (firing rate)

    pot: list = []        # (Entire network's) excitat. cells' potentials
    inh: list = []        # inhib. cells' potentials
    adapt: list = []      # adaptation of all excit cells
    rates: list = []      # firing rates (output) of excitatory cells
    avg_patts: list = []  # time-average of cells' f.rates (pattern specific)
    ca_ovlps: list = []   # overlaps between emerging CA patts. (in each area)
    ovlps: list = []      # "   " betw. current activity & CA patts. ("   " )

    # @todo defined as type bVector in the C code - what is that?
    sensInput: list = [],  # current inputs (NYAREAS areas) to "left" (sensory)
    motorInput: list = []  # current inputs (NYAREAS areas) to "right" (motor)

    # @todo defined as type bVector in the C code - what is that?
    sensPatt: list = [],  # Fixed input patterns (NYAREAS x P) to the left
    motorPatt: list = []  # Fixed input patterns (NYAREAS x P) to the right

    # Post-syn. potentials in input to area
    linkffb: list = [],
    linkrec: list = [],
    linkinh: list = [],
    tempffb: list = [],   # auxiliary (EPSPs from diff. areas)
    clampSMIn: list = []  # Incoming sesnory OR motor input to one area

    slowinh: list = []  # slow inhib (1 cell per area)

    # @todo defined as type bVector in the C code - what is that?
    diluted: list = [],       # All "dead" cells
    above_thresh: list = [],  # Cells CURRENTLY firing above CA_THRESHold
    above_hstory: list = []   # "history" of above_thresh vector activation

    # @todo defined as type bVector in the C code - what is that?
    ca_patts: list = []  # CA patterns emerging as a result of the training

    tot_LTP: list = [],  # Sum of synaptic weight *increase* (in each area)
    tot_LTD: list = []   # Sum of synaptic weight *decrease* (in each area)

    fi: io.TextIOWrapper  # file handle for writing data during TESTING

    # Matrix specifying the network's Connectivity structure #
    # A "1" at coord. (x,y) means Area #x ==> Area #y
    K: list = [
        # (to area)
        # 1, 2, 3, 4, 5, 6
        1, 1, 0, 0, 0, 0,  # 1
        1, 1, 1, 0, 0, 0,  # 2
        0, 1, 1, 1, 0, 0,  # 3
        0, 0, 1, 1, 1, 0,  # 4
        0, 0, 0, 1, 1, 1,  # 5
        0, 0, 0, 0, 1, 1   # 6 (from area)
    ]

    # ALL KERNELS of the network are (linearly) stored in J[].
    # Each "element" is a vector of NSQR1 values (syn. weights)
    # J[Row,Col] = kernel/links FROM area (Row) TO area (Col)
    J: list = []

    Jinh: list = []  # Contains the ONE and only inhibitory (Gauss.) kernel

    def main_init(self):
        """
        main_init() is called when simulation PROGRAM is started. It does
        all initialisations the need to be done only ONCE at startup, eg.
        getting memory for data structures, init. random numbers, etc.
        """
        # Random numbers generation                                      */
        # srandom( time(NULL) );
        # randomize( time(NULL) );
        # noise_fac = sqrt(24.0/STEPSIZE);  // if STEPSIZE=0.5, noise_fac ~= 6.93

        # Membr. pot. of ALL excit. cells
        self.pot = np.zeros(self.NAREAS * self.N1)
        # Firing rates of ALL excit. cells
        self.rates = np.zeros(self.NAREAS * self.N1)
        # M. potential of ALL inhib. cells
        self.inh = np.zeros(self.NAREAS * self.N1)
        # patt.-specific f.rates avg.
        self.avg_patts = np.zeros(self.NAREAS * self.N1 * self.P)
        # emerging Cell Assemblies
        # @todo vVector
        self.ca_patts = np.zeros(self.NAREAS * self.N1 * self.P)
        # Per-area overlaps betw. CAs
        self.ca_ovlps = np.zeros(self.NAREAS * self.P * self.P)
        # Ovlps. betw. CAs & current activity
        self.ovlps = np.zeros(self.NAREAS * self.P)

        # M. potential of G. Inhib. cells
        self.slowinh = np.zeros(self.NAREAS)
        # Adaptation of ALL excit. cells
        self.adapt = np.zeros(self.NAREAS * self.N1)
        # Lesion mask (1 <=> lesioned)

        # @todo vVector
        self.diluted = np.zeros(self.NAREAS * self.N1)

        # @todo vVector
        # cells CURRENTLY > thresh
        self.above_thresh = np.zeros(self.NAREAS * self.N1)
        # @todo vVector
        self.above_hstory = np.zeros(
            self.NAREAS * self.N1 * self.P)  # above_thresh's history
        # (pattern specific)
        self.tot_LTP = np.zeros(self.NAREAS)
        self.tot_LTD = np.zeros(self.NAREAS)

        # @todo bVector
        self.sensInput = np.zeros(self.NYAREAS * self.N1)
        # @todo bVector
        self.motorInput = np.zeros(self.NYAREAS * self.N1)

        # @todo bVector
        self.sensPatt = np.zeros(self.NYAREAS*self.P*self.N1)
        # @todo bVector
        self.motorPatt = np.zeros(self.NYAREAS*self.P*self.N1)

        # freq_distrib = (int*)calloc( P, sizeof(int) ); # array of freq. pres.

        # Kernels: we allocate bigger arrays than we actually need (each
        # el. can contain up to NSQR1 synapses = all-to-all connectivity) #

        self.J = np.zeros(self.NAREAS * self.NAREAS *
                          self.NSQR1)  # NAREAS*NAREAS couplings
        # 1 inhib. kernel with at most self.N1 links
        self.Jinh = np.zeros(self.N1)

        # Vectors of post-synapt. pot. incoming to each cell of one area #
        self.linkffb = np.zeros(self.N1)  # EPSPs from OTHER (between-) areas
        self.linkrec = np.zeros(self.N1)  # EPSPs from THIS area (recurrent)
        # Inh.Post-Syn. Pot from inhib. layer
        self.linkinh = np.zeros(self.N1)
        self.tempffb = np.zeros(self.N1)  # auxiliary (used for temp. EPSPs)
        # "Clamp" input from sensorimotor patt.
        self.clampSMIn = np.zeros(self.N1)

    def randomise_net_activity(self):
        """
        For unit testing: generate activity vectors to pre-empt resetNet
        """
        self.pot = np.random.rand(self.NAREAS * self.N1)
        self.inh = np.random.rand(self.NAREAS * self.N1)
        self.adapt = np.random.rand(self.NAREAS * self.N1)
        self.rates = np.random.rand(self.NAREAS * self.N1)
        self.slowinh = np.random.rand(self.NAREAS)
        self.tot_LTP = np.random.rand(self.NAREAS)
        self.tot_LTD = np.random.rand(self.NAREAS)
        self.above_hstory = np.random.rand(self.NAREAS * self.N1 * self.P)

        self.total_output = random.uniform(1, 1000)

    def resetNet(self):
        """
        Reset completely the network activity (the synaptic weights are 
        left untouched). Recent "history" of TESTING activity is erased.
        """
        self.pot = np.zeros(self.NAREAS * self.N1)
        self.inh = np.zeros(self.NAREAS * self.N1)
        self.adapt = np.zeros(self.NAREAS * self.N1)
        self.rates = np.zeros(self.NAREAS * self.N1)
        self.slowinh = np.zeros(self.NAREAS)
        self.tot_LTP = np.zeros(self.NAREAS)
        self.tot_LTD = np.zeros(self.NAREAS)
        self.above_hstory = np.zeros(self.NAREAS * self.N1 * self.P)

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

    @staticmethod
    def gener_random_bin_patterns(n: int, nones: int, p: int, pats: list):
        """Creates p binary random vectors of length n, where "nones" units are="1" 
        at random positions. "pats" is the array of vectors/patts

        Keyword arguments:
        n     -- IN: no. cells per pattern
        nones -- IN: no. of "1"s per patt.
        p     -- IN: tot. no. patterns
        pats  -- OUT: the array of patterns
        """
        return

    @staticmethod
    def init_gaussian_kernel(nx: int, ny: int, mx: int, my: int, J: list, sigmax: float, sigmay: float, ampl: float):
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
        return

    @staticmethod
    def init_patchy_gauss_kern(nx: int, ny: int, mx: int, my: int, J: list, sigmax: float, sigmay: float, prob: float, upper: float):
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
        return

    @staticmethod
    def train_projection_cyclic(pre: list, post_pot: list, J: list, nx: int, ny: int, mx: int, my: int, hrate: float, totLTP: float, totLTD: float):
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
        return

    @staticmethod
    def compute_CApatts(threshold: float):
        """
        Compute the emerging Cell Assemblies using specified threshold

        Keyword arguments:
        threshold -- IN: threshold used to define a CA
        """
        return

    @staticmethod
    def write_CApatts():
        """
        Write no. of CA-cells of all CA.s to file (for all CA.s & areas). 
        CAs are computed by the above routine "compute_CApatts(thresh)".
        """
        return

    @staticmethod
    def compute_CAoverlaps():
        """
        Compute the PxP overlaps between the emergin Cell Assemblies
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
