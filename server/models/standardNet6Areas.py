import io
import numpy as np
import random
import math
import logging
from . import util, correlation
import json


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
    # TODO these are the original values, but I've reduced them temporarily to demo the automated training
    # PAUSE_TIME = 30
    # INPUT_TIME = 16

    PAUSE_TIME = 2      # Duration of pause betw. inputs (time-steps)
    INPUT_TIME = 1      # Duration of input presentation (time-steps)
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
    sensInput: util.bVectorType
    # current inputs (NYAREAS areas) to "right" (motor)
    motorInput: util.bVectorType

    # Fixed input patterns (NYAREAS x P) to the left
    sensPatt: util.bVectorType
    # Fixed input patterns (NYAREAS x P) to the right
    motorPatt: util.bVectorType

    # Post-syn. potentials in input to area
    linkffb: util.VectorType
    linkrec: util.VectorType
    linkinh: util.VectorType
    tempffb: util.VectorType    # auxiliary (EPSPs from diff. areas)
    clampSMIn: util.VectorType  # Incoming sesnory OR motor input to one area

    slowinh: util.VectorType  # slow inhib (1 cell per area)

    diluted: util.bVectorType        # All "dead" cells
    above_thresh: util.bVectorType   # Cells CURRENTLY firing above CA_THRESHold
    above_hstory: util.bVectorType   # "history" of above_thresh vector activation

    ca_patts: util.bVectorType   # CA patterns emerging as a result of the training

    # Sum of synaptic weight *increase* (in each area)
    tot_LTP: util.VectorType
    # Sum of synaptic weight *decrease* (in each area)
    tot_LTD: util.VectorType

    fi: io.TextIOWrapper  # file handle for writing data during TESTING

    # Matrix specifying the network's Connectivity structure #
    # A "1" at coord. (x,y) means Area #x ==> Area #y
    # Note: keeping this 1d in the spirit of "like for like" translation
    # (Since each area has 625 cells, there are 625 * 625 area-to-area cellular connections
    # So if you want to index a particular connection in the entire network, in 1d:
    # E.g get index of connection between cell 500 and cell 200 in areas 2 and 3:
    # self.J[500*200*(6*2*3)] -> index is 1,500,000
    # total connections is 625*625*36 = 14,062,500)
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

    ## GUI variables - not in the original C implementation ##

    # sliders
    sdiluteprob: int = 0
    slrate: int = 0
    sgain: int = 1000
    stheta: int = 0
    snoise: int = 5
    spatno: int = 0
    sdilutearea: int = 0
    sJslow: int = 18
    sI0: int = 0
    sSInRow: int = 1
    sSInCol: int = 1
    sMInRow: int = 1
    sMInCol: int = 6
    sSI0: int = 300
    sMI0: int = 300
    sJffb: int = 500
    sJinh: int = 500
    sJrec: int = 500

    # switches
    sSInp: bool = False
    sMInp: bool = False
    sdilute: bool = False
    ssaveNet: bool = False
    sloadNet: bool = False
    strainNet: bool = False
    sCA_ovlps: bool = False
    sPrintTest: bool = False

    # Python-specific stuff
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

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

    @staticmethod
    def gener_random_bin_patterns(n: int, nones: int, p: int, pats: util.bVectorType):
        """
        A linearised version of gener_random_bin_patterns. This is the one used. My original translation
        vectorised the structure but this won't work with the rest of the logic, so we stick to linearised structures.
        Instead of returning the patterns matrix (12,625), it returns a 1D NumPy array with shape (12*625, ),
        having a total of 12 * 625 = 7500 elements arranged consecutively in a single dimension.
        Each block of 625 elements represents a single pattern.
        """
        util.Clear_bVector(pats)  # Clear content of ALL patterns
        for j in range(p):  # for each pattern
            start_index = n * j
            # Get the slice representing the current pattern
            temp_pat = pats[start_index:start_index + n]

            # Randomly set "nones" number of elements to 1
            random_indices = np.random.choice(n, nones, replace=False)
            temp_pat[random_indices] = 1

            # Ensure exactly "nones" number of 1s in the pattern
            while np.sum(temp_pat) < nones:  # inefficient, but fast enough
                random_index = np.random.randint(0, n)
                temp_pat[random_index] = 1

        return pats

    def init_gaussian_kernel(self, nx: int, ny: int, mx: int, my: int, J: np.ndarray, sigmax: float, sigmay: float, ampl: float):
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
        # self.logger.info(json.dumps({
        #     'func': 'init_gaussian_kernel',
        #     'area size (nx*ny)': nx*ny,
        #     'kernel size (mx*my)': mx*my,
        #     'std devation (sigmax)': sigmax,
        #     'std deviation (sigmay)': sigmay,
        #     'scaling factor (ampl)': ampl,
        #     'J slice len:': len(J),
        # }, sort_keys=False, indent=4))

        cx = mx // 2
        cy = my // 2

        h1 = 1.0 / (sigmax * sigmax)
        h2 = 1.0 / (sigmay * sigmay)

        # For this area, set up kernel (0,0)
        # e.g. 25 x 25 = 625
        for x in range(mx):
            for y in range(my):
                h = (x - cx) * (x - cx) * h1 + (y - cy) * (y - cy) * h2
                J[y * mx + x:y * mx + x + 1] = ampl * math.exp(-h)

        # Copy kernel (0,0) to other locations
        mm = mx * my  # e.g. 19 x 19 = 361
        for i in range(1, nx * ny):
            J[i * mm: (i + 1) * mm] = J[:mm]

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
        # self.logger.info(json.dumps({
        #     'func': 'init_patchy_gauss_kern',
        #     'area size (1cell<=>1kernel)': nx*ny,
        #     'kernel size': mx*my,
        #     'std devation (sigmax)': sigmax,
        #     'std deviation (sigmay)': sigmay,
        #     'scaling factor (prob)': prob,
        #     'J slice len:': len(J),
        # }, sort_keys=False, indent=4))

        # Checks that max. probability is within bounds
        if prob < 0.0 or prob > 1.0:
            print("ERROR: init_<..>_kernel() probab. not in [0,1]")
            exit(-1)

        # First, we compute the probabilities...
        self.init_gaussian_kernel(nx, ny, mx, my, J, sigmax, sigmay, prob)

        # ...then transform them into the requested synaptic values.
        pot_synapses = nx * ny * mx * my
        non_zero = 0
        for i in range(pot_synapses):
            if util.bool_noise(J[i]):
                non_zero = non_zero + 1
                J[i:i+1] = upper * util.equal_noise()
            else:
                J[i:i+1] = 0  # NO_SYNAPSE
        # print('total potential synapses for area-area:', pot_synapses)
        # print('synapses with non-zero weights:', non_zero)
        # print("% non zero", round((non_zero/pot_synapses)*100))

    def main_init(self):
        """
        main_init() is called when simulation PROGRAM is started. It does
        all initialisations the need to be done only ONCE at startup, eg.
        getting memory for data structures, init. random numbers, etc.

        Note: we could easily move this initialise these values in-line above, but I'm
        leaving as is, in the spirit of "like for like" translation
        """
        self.logger.info(json.dumps(
            {'func': 'main_init'}, sort_keys=False, indent=4))

        # Random numbers generation
        # random.seed(time.time())

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

    def resetNet(self):
        """
        Reset completely the network activity (the synaptic weights are
        left untouched). Recent "history" of TESTING activity is erased.

        Note: we modify the value of the mutable vector directly inside the function
        Note: I don't think we need to pass the len in here, but I'll leave it for now,
        in the spirit of "like for like" translation
        """
        self.logger.info(json.dumps(
            {'func': 'resetNet'}, sort_keys=False, indent=4))

        util.Clear_Vector(self.pot)
        util.Clear_Vector(self.inh)
        util.Clear_Vector(self.adapt)
        util.Clear_Vector(self.rates)
        util.Clear_Vector(self.slowinh)
        util.Clear_Vector(self.tot_LTP)
        util.Clear_Vector(self.tot_LTD)
        util.Clear_bVector(self.above_hstory)

        self.total_output = 0.0

    def init(self):
        """
        init() is called whenever "INIT" or "RUN" buttons in the GUI are
        pressed; it initialises individual simulation runs
        """
        self.logger.info(json.dumps(
            {'func': 'init'}, sort_keys=False, indent=4))

        util.Clear_Vector(self.pot)
        util.Clear_Vector(self.rates)
        util.Clear_Vector(self.adapt)
        util.Clear_Vector(self.avg_patts)
        util.Clear_bVector(self.ca_patts)
        util.Clear_Vector(self.ca_ovlps)
        util.Clear_Vector(self.ovlps)
        util.Clear_bVector(self.diluted)
        util.Clear_Vector(self.inh)
        util.Clear_Vector(self.slowinh)
        util.Clear_bVector(self.sensInput)
        util.Clear_bVector(self.motorInput)
        util.Clear_bVector(self.sensPatt)
        # NYAREAS rows x P col.
        util.Clear_bVector(self.motorPatt)
        # util.Clear_bVector(self.NAREAS * self.NAREAS, self.K);
        util.Clear_bVector(self.above_thresh)
        util.Clear_bVector(self.above_hstory)

        self.total_output = 0.0

        util.Clear_bVector(self.freq_distrib)

        ## Randomly initialise all sensorimotor input patterns ##
        self.sensPatt = self.gener_random_bin_patterns(
            self.N1, self.NONES, self.NYAREAS*self.P, self.sensPatt)
        self.motorPatt = self.gener_random_bin_patterns(
            self.N1, self.NONES, self.NYAREAS*self.P, self.motorPatt)

        ## INITIALISE ALL THE KERNELS ##
        util.Clear_Vector(self.J)

        # for each of the 36 area-area connections, pass to the kern funcs a slice of J corresponding to its
        # position in the linear sequence, e.g. for (0,0) pass J[0:390625]
        # if we just pass J[0:1], the funcs will not be able to modify J at any index beyond 0
        for j in range(self.NAREAS):
            for i in range(self.NAREAS):
                # Does area j have REC. links?
                if j == i and self.K[(self.NAREAS + 1) * j]:
                    # we need to pass a slice representing the section of J corresponding to the synapses for this area connection
                    # so downstream operations modify it in place
                    # e.g. for the area connection (0,0), J[0:390625]
                    start_idx = self.NSQR1 * (self.NAREAS * i + i)
                    self.init_patchy_gauss_kern(self.N11, self.N12, self.NREC1, self.NREC2, self.J[start_idx:start_idx+self.NSQR1],
                                                self.SIGMAX_REC, self.SIGMAY_REC, self.J_REC_PROB, self.J_UPPER)
                elif self.K[self.NAREAS * j + i]:  # Does AREA (j+1) --> (i+1)?
                    start_idx = self.NSQR1 * (self.NAREAS * j + i)
                    self.init_patchy_gauss_kern(self.N11, self.N12, self.NFFB1, self.NFFB2, self.J[start_idx:start_idx+self.NSQR1],
                                                self.SIGMAX, self.SIGMAY, self.J_PROB, self.J_UPPER)

        # logging
        pot_synapses = self.N1 * \
            (self.NREC1 * self.NREC1) * (self.NAREAS * self.NAREAS)
        weighted = sum(self.J > 0)
        inactive = sum(self.J == 0)
        non_zero_percent = round((weighted/pot_synapses)*100)
        inactive_percent = round((inactive/pot_synapses)*100)
        self.logger.info(json.dumps({
            'func': 'init',
            'total potential network synapses': pot_synapses,
            'non-zero synaptic weights': str(weighted),
            'inactive synapses': str(inactive),
            'non-zero synaptic weights (%)': str(non_zero_percent),
            'inactive synapses (%)': str(inactive_percent),
        }, sort_keys=False, indent=4))

        # There is only 1 inhibitory kernel (FIXED & identical for all)
        self.init_gaussian_kernel(1, 1, self.NINH1, self.NINH2, self.Jinh,
                                  self.SIGMAX_INH, self.SIGMAY_INH, self.J_INH_INIT)

        # If dilute switch is pressed, "damage" the appropriate area(s)
        # ("sdilutearea" slider indicates area to be lesioned; 0==ALL)
        # NB: this is only executed ONCE, at network INITIALISATION.
        if self.sdilute:
            for area in range(self.NAREAS):
                h = 0.01 * self.sdiluteprob  # sdiluteprob: a slider value
                if self.sdilutearea == 0 or (area + 1) == self.sdilutearea:
                    # temp. pointer to this area
                    # pdil = self.diluted[self.N1 * area]
                    pdil = self.diluted[area*self.N1:(area+1)*self.N1]
                    # A "1" in vector "diluted" will mean that cell is damaged
                    for i in range(self.N1):
                        pdil[i] = int(util.bool_noise(h))
            self.sdilute = False  # SET_SWITCH(sdilute, FALSE)

        self.training_phase = 0  # Init. training phase (used in TRAINING)
        self.stps_2b_avgd = 0    # Reset averaging steps count (4 TRAINING)
        self.test_phase = 0      # initialise testing phase (4 TESTING mode)
        self.stimRepet = 0       # Counter (no. of stimulation repetitions)

        self.stp = 0  # Initialise simulation-step

    def set_up_current_sensorimotor_input(self, noise: float):
        # Get & rescale NOISE(for "input" areas)
        if self.spatno == 0:  # 0 = no input: CLEAR all activity
            util.Clear_bVector(self.sensInput)
            util.Clear_bVector(self.motorInput)
        else:  # spatno > 0: SOME input stimulation
            # Create white noise in ALL sensory & motor input areas (EXCEPT
            # if we are TRAINING the netw. AND a stim. is being presented).
            # Some areas might be later "overwritten" by "real" s-m. patts.
            # If NOT training OR currently NOT presenting a stimulus
            if not self.strainNet or self.training_phase != 2:
                for j in range(self.NYAREAS):  # For all "rows" of the net
                    # Get addr. of sens. input area for current netw.'s "row"
                    pinput = self.sensInput[self.N1 * j:self.N1 * (j + 1)]
                    # Produce white noise there (noise def. at start of step())
                    for i in range(self.N1):
                        pinput[i] = util.bool_noise(noise)

                    # Get addr. of motor input area for current netw.'s "row"
                    pinput = self.motorInput[self.N1 * j:self.N1 * (j + 1)]
                    # Produce white noise there (noise def. at start of step())
                    for i in range(self.N1):
                        pinput[i] = util.bool_noise(noise)

            # COPY SENSORY PATTERNS to INPUT AREAS
            if self.sSInp and self.spatno < self.P + 1:  # Is there a sens. patt. to be presented?
                for j in range(self.NYAREAS):  # for each "row" of the network
                    # Check whether this "row" of the net should get any input
                    # NYAREAS+1 == ALL
                    if self.sSInRow == (j + 1) or self.sSInRow == self.NYAREAS + 1:
                        # Get pointer to relevant pattern in "sensPatt" matrix
                        pinput = self.sensPatt[(self.P * self.N1) * j + self.N1 *
                                               (self.spatno - 1):(self.P * self.N1) * j + self.N1 * self.spatno]

                        # Copy the sensory pattern
                        for i in range(self.N1):
                            self.sensInput[(self.N1 * j) + i] = pinput[i]

            # COPY MOTOR PATTERNS to INPUT AREAS
            if self.sMInp and self.spatno < self.P + 1:  # Is there a motor patt. to be presented?
                for j in range(self.NYAREAS):  # for each "row" of the network
                    # Check whether this "row" of the net should get any input
                    # NYAREAS+1 == ALL
                    if self.sMInRow == (j + 1) or self.sMInRow == self.NYAREAS + 1:
                        # Get pointer to relevant pattern in "motorPatt" matrix
                        pinput = self.motorPatt[(self.P * self.N1) * j + self.N1 *
                                                (self.spatno - 1):(self.P * self.N1) * j + self.N1 * self.spatno]
                        # Copy the motor pattern
                        for i in range(self.N1):
                            self.motorInput[(self.N1 * j) + i] = pinput[i]

    def compute_emerging_cell_assemblies_and_overlaps(self):
        if self.sCA_ovlps:
            self.compute_CApatts(self.CA_THRESH)  # re-compute all CAs
            self.compute_CAoverlaps()  # re-compute CA overlaps
            self.write_CApatts()  # write CA-cells numbers to file
            self.sCA_ovlps = False

    def compute_new_adaptation(self):
        for area in range(self.NAREAS):
            # e.g. 0:625 for area 1, 625:1250 for area 2 etc.
            prates = self.rates[self.N1 * area:self.N1 * (area + 1)]
            padapt = self.adapt[self.N1 * area:self.N1 * (area + 1)]

            # Cell's adaptation = low-pass filter of cell's output (f.rate)
            for i in range(self.N1):
                padapt[i] = util.leaky_integrate(
                    self.TAUADAPT, padapt[i], self.ADAPTSTRENGTH * prates[i], self.STEPSIZE)

    def compute_overlap_between_cell_assemblies_and_current_activity(self):
        """
        For each area, compute the overlap between the activity and each of the 12 cell assemblies.
        """
        for i in range(self.P):
            for area in range(self.NAREAS):
                # e.g. 0:625 for area 1, 625:1250 for area 2 etc.
                prates = self.rates[self.N1 * area:self.N1 * (area + 1)]

                # e.g. 0:625       for intersection of Area 1 and CA 1  (aka 1st segment of 1st area)
                # e.g. 44375:45000 for intersection of Area 6 and CA 12 (aka 12th segment of 6th area)
                pcapatts = self.ca_patts[self.N1 * (
                    self.NAREAS * i + area):self.N1 * (self.NAREAS * i + (area + 1))]

                self.ovlps[area * self.P + i] = util.bSkalar(
                    self.N1, prates, pcapatts)

    def compute_firing_rates(self, gain: float, theta: float):
        """
        COMPUTE FIRING RATES (OUTPUTS)
        """
        self.total_output = 0.0
        for area in range(self.NAREAS):  # For ALL areas in the network
            # "Define some helpful pointers (mostly for speed)"
            ppot = self.pot[self.N1 * area:self.N1 * (area + 1)]
            prates = self.rates[self.N1 * area:self.N1 * (area + 1)]
            padapt = self.adapt[self.N1 * area:self.N1 * (area + 1)]

            # self.total_output = 0.0 # TODO i'm not sure we want to do this?
            for i in range(self.N1):  # For ALL cells in current area
                prates[i] = self.FUNC(gain * (ppot[i] - theta - padapt[i]))
                self.total_output += prates[i]  # update total network output

    def record_average_responses_during_training(self):
        """
        RECORD AVERAGE RESPONSES DURING TRAINING
        """
        if (self.stps_2b_avgd > 0) and (self.spatno > 0) and (self.spatno < self.P + 1):
            for area in range(self.NAREAS):
                # Get addr. of 1st "cell" of pattern-specific averaging array
                start_index = self.N1 * \
                    (self.NAREAS * (self.spatno - 1) + area)
                end_index = self.N1 * \
                    (self.NAREAS * (self.spatno - 1) + area + 1)

                prates_avg = self.avg_patts[start_index:end_index]

                # point to f.rate of 1st cell of area
                prates = self.rates[self.N1 * area: self.N1 * (area + 1)]
                for i in range(self.N1):  # For all cells of this area
                    # Integrate cell's current f. rate into its average f. rate
                    prates_avg[i] = util.leaky_integrate(
                        self.TAU_AVG_RATES, prates_avg[i], prates[i], self.STEPSIZE)

            self.stps_2b_avgd -= 1  # Averaging is done only for a limited time

    def compute_CAoverlaps(self):
        for area in range(self.NAREAS):
            for i in range(self.P):
                for j in range(self.P):
                    idx_i = self.N1 * (self.NAREAS * i + area)
                    idx_j = self.N1 * (self.NAREAS * j + area)
                    overlap = util.bbSkalar(
                        self.N1, self.ca_patts[idx_i:idx_i + self.N1], self.ca_patts[idx_j:idx_j + self.N1])
                    self.ca_ovlps[self.P * (self.P * area + i) +
                                  j] = overlap / float(self.NONES)

    def write_CApatts(self):
        try:
            with open(self.CA_WR, 'a') as fiCA:  # Open the file for append (or writing)
                for i in range(self.P):  # For all CAs (patterns)
                    fiCA.write(f" \n CA #{i + 1}: ")
                    for area in range(self.NAREAS):  # for all areas
                        start_idx = self.N1 * (self.NAREAS * i + area)
                        end_idx = self.N1 * (self.NAREAS * i + area + 1)

                        # Write to file tot. no. of CA cells for this CA and area
                        sum_cells = util.bSum(
                            self.N1, self.ca_patts[start_idx: end_idx])
                        fiCA.write(f"{sum_cells} ")
                print("\n\n")
        except IOError:
            print(
                f"\n ERROR: Could not open file '{self.CA_WR}' for writing.\n")

    def compute_CApatts(self, threshold):
        """
        Compute the emerging Cell Assemblies using specified threshold

        Keyword arguments:
        threshold -- IN: threshold used to define a CA
        """
        for area in range(self.NAREAS):  # For all areas
            for i in range(self.P):  # for all input pattern pairs
                start_idx = self.N1 * (self.NAREAS * i + area)
                end_idx = start_idx + self.N1

                # Get firing rate of maximally responsive cell in current area
                max_act = util.Max_Elem(self.avg_patts[start_idx:end_idx])

                # Check if there is at least 1 cell strongly responsive
                if max_act >= self.MIN_CELLRATE:
                    # If cell rate > threshold, set cell to 1 in 'ca_patts'
                    util.Fire(self.N1, self.avg_patts[start_idx:end_idx], threshold*max_act,
                              self.ca_patts[start_idx:end_idx])
                # Else: NO cells are set to 1 in the 'ca_patts' vector

    def train_projection_cyclic(self, pre, post_pot, J, nx, ny, mx, my, hrate, totLTP, totLTD):
        """Train" all the synapses connecting area X to area Y (incl. X==Y)

        Keyword arguments:
        pre       -- IN: area X cells' firing rates (output)
        post_pot  -- IN: area Y cells' memb. potentials
        J         -- IN/OUT: all the kernels connecting X to Y
        nx, ny    -- IN: area dimensions (2 areas of same size)
        mx, my    -- IN: kernels' x and y's dimensions
        hrate     -- IN: learning rate (weight increm/decrem.)
        totLTP    -- OUT: tot. amount of LTP (PYTHON: pass in slice containing a single index, mutate in place, e.g. self.tot_LTP[i:i+1])
        totLTD    -- OUT: tot. amount of LTD (PYTHON: pass in slice containing a single index, mutate in place, e.g. self.tot_LTD[i:i+1])
        """
        kx2 = mx // 2
        ky2 = my // 2
        mxy = mx * my

        kern = J  # Address of 1st (potential) link between X and Y

        for i in range(ny):  # For all cells in area Y
            for j in range(nx):  # ("ij" counts tot. # of cells)
                ij = i * nx + j
                for k in range(-ky2, ky2 + 1):  # For all links of 1 kernel
                    for l in range(-kx2, kx2 + 1):  # ("kern" counts tot. #links)
                        m = ((i + k + ny) % ny) * nx + \
                            (j + l + nx) % nx  # Get index of cell in X

                        # Check if synapse considered "exists" (i.e. is <> 0.0 )
                        if kern[ij * mxy + k * mx + l] != self.NO_SYNAPSE:
                            # Synapse exists; update its weight using learning rule
                            # Get pre-synaptic activity (f. rate)
                            pre_D = pre[m]

                            # Check if post-synapt. pot. is above LTP threshold
                            if post_pot[ij] > self.LTP_THRESH:
                                if pre_D > self.F_THRESH:  # Is there suff. pre-syn. activ.?
                                    # Yes; reached MAX syn. weight?
                                    if kern[ij * mxy + k * mx + l] < self.JMAX:
                                        # Not yet: Homosynaptic LTP
                                        kern[ij * mxy + k * mx + l] += hrate
                                        totLTP += hrate  # Update TOT. amount of LTP
                                else:  # NO (i.e., pre_D <= F_THRESH)
                                    # Reached MIN synapt. weight?
                                    if kern[ij * mxy + k * mx + l] > self.JMIN:
                                        # Not yet: "low"-homo or hetero LTD
                                        kern[ij * mxy + k * mx + l] -= hrate
                                        totLTD += hrate  # Update TOT. amount of LTD
                                        # Make sure not to go below...
                                        if kern[ij * mxy + k * mx + l] < self.JMIN:
                                            kern[ij * mxy + k *
                                                 mx + l] = self.JMIN
                            else:  # IN THIS CASE: post_pot <= LTP_THRESH
                                if (pre_D > self.F_THRESH) and (post_pot[ij] > self.LTD_THRESH) and (kern[ij * mxy + k * mx + l] > self.JMIN):
                                    # Yes: homosynaptic LTD
                                    kern[ij * mxy + k * mx + l] -= hrate
                                    totLTD += hrate  # Update TOT. amount of LTD
                                    if kern[ij * mxy + k * mx + l] < self.JMIN:
                                        kern[ij * mxy + k * mx + l] = self.JMIN

    def compute_learning(self, hrate):
        if self.slrate > 0:  # Is learning ON?
            util.Clear_Vector(self.tot_LTP)
            util.Clear_Vector(self.tot_LTD)

            for i in range(self.NAREAS):  # For all DEST. areas (col. "i" of J[])
                for j in range(self.NAREAS):  # For all ORIGIN areas (row "j" of J[])

                    # Is ORIGIN == DEST. & does area (j+1) have REC. links?
                    if j == i and self.K[(self.NAREAS + 1) * j] != 0:
                        # Yes: train RECurrent kernel projections for this area
                        self.train_projection_cyclic(
                            # pre-syn. rates
                            self.rates[self.N1 * j:self.N1 * (j + 1)],
                            # post-syn. pot.
                            self.pot[self.N1 * i:self.N1 * (i + 1)],
                            # all (j+1)-->(j+1) kernels
                            self.J[self.NSQR1 * (self.NAREAS + 1) * j:self.NSQR1 * \
                                   (self.NAREAS + 1) * (j + 1)],
                            self.N11, self.N12, self.NREC1, self.NREC2, hrate, self.tot_LTP[i:i+1], self.tot_LTD[i:i+1])

                    # Does area (j+1) proj. to (i+1)?
                    elif self.K[self.NAREAS * j + i] != 0:
                        self.train_projection_cyclic(
                            # pre-syn. rates
                            self.rates[self.N1 * j:self.N1 * (j + 1)],
                            # post-syn. pot.
                            self.pot[self.N1 * i:self.N1 * (i + 1)],
                            # all (j+1)-->(i+1) kernels
                            self.J[self.NSQR1 * (self.NAREAS * j + i):self.NSQR1 * \
                                   (self.NAREAS * (j + 1) + i)],
                            self.N11, self.N12, self.NFFB1, self.NFFB2, hrate, self.tot_LTP[i:i+1], self.tot_LTD[i:i+1])

    @util.time_it
    def compute_new_membrane_potentials(self):
        for area in range(self.NAREAS):
            # get the slices of activity for this area (the 625 cells in area)
            ppot = self.pot[self.N1 * area:self.N1 * (area + 1)]
            pinh = self.inh[self.N1 * area:self.N1 * (area + 1)]
            pdil = self.diluted[self.N1 * area:self.N1 * (area + 1)]

            # Clear vectors containing incoming input to current area
            util.Clear_Vector(self.linkffb)   # From OTHER areas
            util.Clear_Vector(self.linkrec)   # From THIS area
            util.Clear_Vector(self.linkinh)   # From inhib. layer
            # auxiliary (used for OTHER areas)
            util.Clear_Vector(self.tempffb)
            # from sensory/OR/motor inp. patt.
            util.Clear_Vector(self.clampSMIn)

            ### Sensorimotor input ##

            # Is this area (possibly) receiving a sensory pattern as input?
            if area % self.NXAREAS == self.sSInCol - 1:
                # Yes: give any current sens. pattern as input to this area
                for i in range(self.N1):
                    # Note: sensInput[] is a column of NYAREAS elem. of size N1
                    self.clampSMIn[i] = self.sSI0 * \
                        self.sensInput[self.N1 * (area // self.NXAREAS) + i]
            elif area % self.NXAREAS == self.sMInCol - 1:  # Area receiving motor patt.?
                for i in range(self.N1):
                    # NB: motorInput[] is a column of NYAREAS elem. of size N1
                    self.clampSMIn[i] = self.sMI0 * \
                        self.motorInput[self.N1 * (area // self.NXAREAS) + i]

            ### FF/fb (between area) input ###

            for j in range(self.NAREAS):  # Check all areas (column "area" of K[])
                # Is "j" NOT same as "area" and does area (j+1)-->(area+1)?..
                if j != area and self.K[self.NAREAS * j + area]:
                    # Compute area (j+1)'s contrib. to TOT. input to (area+1)
                    correlation.Correlate_2d_cyclic_python(
                        self.rates[self.N1 * j: self.N1 * (j + 1)],
                        self.J[self.NSQR1 * (self.NAREAS * j + area)                               : self.NSQR1 * (self.NAREAS * (j + 1) + area)],
                        self.N11, self.N12, self.NFFB1, self.NFFB2, self.tempffb
                    )

                    # Add this contribution to the TOTAL EPSP to current area
                    for i in range(self.N1):
                        self.linkffb[i] = self.tempffb[i]

                    # Reset the temp. vector of results
                    util.Clear_Vector(self.tempffb)

            ### RECurrent (within area) input ###

            # Calculate linkrec[i] (total pre-synaptic pot. converging from
            # within-area cells to cell i) for all cells of area "area+1".
            if self.K[(self.NAREAS + 1) * area]:  # Does area have REC links?
                correlation.Correlate_2d_cyclic_python(
                    self.rates[self.N1 * area: self.N1 * (area + 1)],
                    self.J[self.NSQR1 * (self.NAREAS + 1) *
                           area: self.NSQR1 * (self.NAREAS + 1) * (area + 1)],
                    self.N11, self.N12, self.NREC1, self.NREC2, self.linkrec
                )

            ### INHibitory (within area) input ###

            # Calculate linkinh[i] (tot. activity from excitat. cells which
            # is being projected to each underlying inhibitory cell "i")
            correlation.Correlate_2d_Uni_cyclic(
                self.rates[self.N1 * area: self.N1 * (area + 1)],
                self.Jinh,
                self.N11, self.N12, self.NINH1, self.NINH2, self.linkinh
            )

            ### LEAKY INTEGRATIONS ###

            # Inhibitory cells: The total output from excit. cells (linkinh[i]) is now inte-
            # grated (ie, weight=1) into inhib. cell "i"'s membr. potential
            for i in range(self.N1):
                self.linkinh[i] = util.leaky_integrate(
                    self.TAU2, pinh[i], self.linkinh[i], self.STEPSIZE)

            # Slow/global inhibition/activity control
            self.slowinh[area] = util.leaky_integrate(self.TAUSLOW, self.slowinh[area], util.Sum(
                self.rates[self.N1 * area: self.N1 * (area + 1)]), self.STEPSIZE)

            # Excitatory cells
            for i in range(self.N1):  # For all cells of current area
                ppot[i] = util.leaky_integrate(self.TAU1, ppot[i], .01 * (self.sI0 + self.clampSMIn[i] + self.sJffb * self.linkffb[i] +
                                                                          self.sJrec * self.linkrec[i] - self.sJinh * self.FUNCI(pinh[i]) -
                                                                          self.sJslow * self.slowinh[area] - 1000 * pdil[i] +
                                                                          self.snoise * self.noise_fac * (util.equal_noise() - .5)), self.STEPSIZE)

    def manage_network_training(self):
        if self.strainNet:  # Is the "network training" switch pressed?
            if self.training_phase == 0:  # PHASE 0: prepare for a "PAUSE" phase
                self.last_stp = self.stp  # record current time step
                # SET_SLIDER(self.spatno, self.P + 1)  # pattern no. P+1 == noise
                self.spatno = self.P + 1
                # SET_SWITCH(self.ssaveNet, True)  # Force writing data (net0.dat)
                self.ssaveNet = True
                self.training_phase += 1  # move to next phase

            # PHASE 1: PAUSE -- wait until an "INPUT" phase is due..
            elif self.training_phase == 1:
                # levels decayed enough?
                # and glob. inhibition
                if (self.stp - self.last_stp >= self.PAUSE_TIME and self.slowinh[self.SLOWAREA1] < self.MAXINHIB1 and self.slowinh[self.SLOWAREA2] < self.MAXINHIB2):
                    # Pseudo-randomly select a number betw. 1 and P, ensuring
                    # that the patterns freq. distribution is approx. uniform
                    patt_no = int(1234.56 * util.equal_noise())
                    while True:
                        patt_no = (patt_no % self.P) + 1
                        if self.freq_distrib[patt_no - 1] <= self.freq_distrib[(patt_no % self.P)]:
                            break

                    self.spatno = patt_no  # SET_SLIDER(self.spatno, patt_no)

                    self.stps_2b_avgd = self.AVG_RATES_TIME  # Set averaging steps-counter
                    # Update presentation freq.
                    self.freq_distrib[patt_no - 1] += 1
                    self.last_stp = self.stp  # record current time step
                    self.training_phase += 1

            # PHASE 2: INPUT -- wait until a "PAUSE" phase is due..
            elif self.training_phase == 2:
                if (self.stp - self.last_stp) >= self.INPUT_TIME:  # Have enough steps passed?
                    # Is it time to save data or stop current simulation?
                    frq = self.freq_distrib[0]  # get patt.#1's frequency
                    if frq > self.TOT_TRAINING:  # Enough presentations?
                        self.training_phase += 1  # YES: END OF TRAINING - STOP
                    else:
                        # If no. presentations is multiple of SAVE_CYCLE OR is
                        # < SAVE_CYCLE && multiple of 100, save the net. data
                        if (frq > 0 and
                            (frq % self.SAVE_CYCLE == 0 or
                             (frq <= 50 and frq % 10 == 0) or
                             (frq < self.SAVE_CYCLE and frq % 100 == 0))):
                            # Will write data to file
                            self.ssaveNet = True  # SET_SWITCH(ssaveNet, True)

                            # spatno==P+1 ==> white noise
                            # SET_SLIDER(self.spatno, self.P + 1)
                            self.spatno = self.P + 1

                        self.last_stp = self.stp  # Record current time
                        # re-compute all CAs
                        self.compute_CApatts(self.CA_THRESH)
                        self.compute_CAoverlaps()  # re-compute CA overlaps
                        # Start (or continue) learning
                        # SET_SLIDER(self.slrate, self.LEARN_RATE)
                        self.slrate = self.LEARN_RATE
                        self.training_phase = 1  # GO BACK to PHASE 1

            else:  # Otherwise STOP the training (when stp reaches TOT_TRAINING)
                self.strainNet = False  # SET_SWITCH(self.strainNet, False)
                print("\n End of training phase. \n")
                exit(0)

    def step(self):
        """
        MAIN  "STEP" FUNCTION, executed at each sim. step
        """
        self.logger.info(json.dumps({
            'op': 'step',
            'step': self.stp,
            'training active': self.strainNet,
            'current pattern': self.spatno,
            'sinhib area1': self.slowinh[self.SLOWAREA1],
            'sinhib area2': self.slowinh[self.SLOWAREA2],
        }, sort_keys=False, indent=4))

        hrate: float = .0001 * self.slrate  # Get & rescale LEARN. rate specif. by slider
        gain = .001 * self.sgain  # Get & rescale GAIN value specif. by slider
        theta = .001 * self.stheta  # Get & rescale THRESH. value "    "   " "
        noise = .0001 * self.snoise  # Get & rescale NOISE(for "input" areas)

        ## TODO Save the entire network to file (incl. input patts.) ##

        ## TODO Load entire network from file (incl. input patts.) ##

        ## MANAGE network TRAINING ##
        self.manage_network_training()

        ## SET UP THE CURRENT SENSORIMOTOR INPUT ##
        self.set_up_current_sensorimotor_input(noise)

        ## COMPUTE NEW MEMBRANE POTENTIALS ##
        self.compute_new_membrane_potentials()

        ## COMPUTE FIRING RATES (OUTPUTS) ##
        self.compute_firing_rates(gain, theta)

        ## COMPUTE NEW ADAPTATION ##
        self.compute_new_adaptation()

        ## LEARNING ##
        self.compute_learning(hrate)

        ## RECORD AVERAGE RESPONSES DURING TRAINING ##
        self.record_average_responses_during_training()

        ## COMPUTE EMERGING CAs and their OVERLAPS ##
        self.compute_emerging_cell_assemblies_and_overlaps()

        ## COMPUTE OVERLAP BETW. CAs and CURRENT ACTIV. ##
        self.compute_overlap_between_cell_assemblies_and_current_activity()

        ## TODO AUTOMATED TESTING ##

        ## TODO ASCII DATA FILE WRITING ##

        self.stp = self.stp+1
        return self.get_current_activity()

    # TODO delegate this to the simulation_manager
    def get_current_activity(self):
        potentials = self.pot.reshape(6, 25, 25).tolist()
        global_inhibition = self.slowinh.tolist()
        long_term_potentiation = self.tot_LTP.tolist()
        long_term_depression = self.tot_LTD.tolist()
        cell_assembly_overlaps = self.ca_ovlps.reshape(6, 12, 12, order='C').tolist()

        return {
            'currentStep': self.stp,
            'config': dict({
                'patternNumber': self.spatno,
                'learningRate': self.slrate,
                'shouldSaveNetwork': self.ssaveNet,
                'networkTrainingActivated': self.strainNet,
                'computeCaOverlaps': self.sCA_ovlps
            }),
            'totalActivity': self.total_output,
            'sensInput': self.sensInput.reshape(25, 25).tolist(),
            'motorInput': self.motorInput.reshape(25, 25).tolist(),
            'longTermPotentiation': {
                'area1': long_term_potentiation[0],
                'area2': long_term_potentiation[1],
                'area3': long_term_potentiation[2],
                'area4': long_term_potentiation[3],
                'area5': long_term_potentiation[4],
                'area6': long_term_potentiation[5],
            },
            'longTermDepression': {
                'area1': long_term_depression[0],
                'area2': long_term_depression[1],
                'area3': long_term_depression[2],
                'area4': long_term_depression[3],
                'area5': long_term_depression[4],
                'area6': long_term_depression[5],
            },
            'globalInhibition': {
                'area1': global_inhibition[0],
                'area2': global_inhibition[1],
                'area3': global_inhibition[2],
                'area4': global_inhibition[3],
                'area5': global_inhibition[4],
                'area6': global_inhibition[5],
            },
            'potentials': {
                'area1': potentials[0],
                'area2': potentials[1],
                'area3': potentials[2],
                'area4': potentials[3],
                'area5': potentials[4],
                'area6': potentials[5],
            },
            'cellAssemblyOverlaps': {
                'area1': cell_assembly_overlaps[0],
                'area2': cell_assembly_overlaps[1],
                'area3': cell_assembly_overlaps[2],
                'area4': cell_assembly_overlaps[3],
                'area5': cell_assembly_overlaps[4],
                'area6': cell_assembly_overlaps[5],
            }
        }

    def config_set_noise(self, new_noise):
        self.snoise = new_noise

    def config_set_global_inhibition(self, new_global_inhibition):
        self.sJslow = new_global_inhibition

    def config_set_pattern_number(self, new_pattern_number):
        self.spatno = new_pattern_number

    def config_set_is_receiving_sensory_input(self, is_receiving_sens_input):
        self.sSInp = is_receiving_sens_input

    def config_set_is_receiving_motor_input(self, is_receiving_motor_input):
        self.sMInp = is_receiving_motor_input

    def config_set_sensory_stimulation_amplitude(self, sensory_stimulation_amplitude):
        self.sSI0 = sensory_stimulation_amplitude

    def config_set_motor_stimulation_amplitude(self, motor_stimulation_amplitude):
        self.sMI0 = motor_stimulation_amplitude

    def config_set_network_training_activated(self, network_training_activated):
        self.strainNet = network_training_activated

    def config_set_compute_ca_overlaps(self, compute_ca_overlaps):
        self.sCA_ovlps = compute_ca_overlaps

    def MAIN_INIT_RANDOM_ACTIVITY(self):
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

    def INIT_RANDOM_ACTIVITY(self):
        """
        For unit testing: generate activity vectors to pre-empt init
        """
        self.rates = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.pot = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.adapt = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.avg_patts = util.Get_Random_Vector(self.NAREAS * self.N1 * self.P)
        self.ca_patts = util.Get_Random_Vector(self.NAREAS * self.N1 * self.P)
        self.ca_ovlps = util.Get_Random_Vector(self.NAREAS * self.P * self.P)
        self.ovlps = util.Get_Random_Vector(self.NAREAS * self.P)
        self.diluted = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.inh = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.slowinh = util.Get_Random_Vector(self.NAREAS)
        self.sensInput = util.Get_Random_Vector(self.NYAREAS * self.N1)
        self.motorInput = util.Get_Random_Vector(self.NYAREAS * self.N1)
        self.sensPatt = util.Get_Random_Vector(self.NYAREAS * self.P * self.N1)
        self.motorPatt = util.Get_Random_Vector(
            self.NYAREAS * self.P * self.N1)
        self.above_thresh = util.Get_Random_Vector(self.NAREAS * self.N1)
        self.above_hstory = util.Get_Random_Vector(
            self.NAREAS * self.N1 * self.P)

        self.total_output = random.uniform(1, 1000)

        self.freq_distrib = util.Get_Random_Vector(self.P)
