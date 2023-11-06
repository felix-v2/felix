/*
 * NET 37 -- (c) Max Garagnani 2014
 *
 * This version extends the existing 6-area network by
 * adding 3+3 visual/motor semantic modules.
 *
 * Most recent additions:
 *
 * -- Enables automated testing & writing output to file
 * -- Window with overlap betw. CAs & current activity
 * -- Presents "fixed" patts. to ALL input areas during TRAINING
 * -- Enables writing current CAs structure (# CA cells) to file
 */

# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <strings.h>
# include <math.h>
# include <time.h>

# include <felix.h>



 # define NXAREAS 6        // x-size of the net (in no. of areas)
 # define NYAREAS 1        // y-size of the net (in no. of areas)
 # define NAREAS (NXAREAS*NYAREAS)  // Network's TOT no. of areas

// These definitions are used to make the code more readable

 # define AREA1 0
 # define AREA2 1
 # define AREA3 2
 # define AREA4 3
 # define AREA5 4
 # define AREA6 5
 # define AREA7 6
// # define AREA8 7
// # define AREA9 8
// # define AREA10 9
// # define AREA11 10
// # define AREA12 11

 # define P 12             // no. of differnt pattern-ntuples to be learnt

 # define CA_THRESH  0.5   // threshold used to define a CA
 # define MIN_CELLRATE 0.10 // minimum activity required for an area to be
                            // considered responsive (to calculate CAs)

/* ********************* Layers dimensions ************************* */
 # define N11   25
 # define N12   25
 # define N1    (N11*N12)   // # of cells in 1 area
 # define NSQR1 (N1*N1)     // # of (possible) synapses between 2 areas

 # define NONES 19          // # of "1"s in each random input pattern

 # define STEPSIZE  0.5     // "delta-t" of the simulation

 # define ZOOMFACT  5       // Size (pixels) of side of square for 1 cell
 # define ZOOMPATFACT 4     // cell size (pix) for CA patterns windows
 # define OVRLPZOOMFACT 5   // cell size (pix) for CA overlap

/* ************************ Time constants ************************* */

 # define TAU1     2.5     // for EPSPs
 # define TAU2     5.0     // for IPSPs
 # define TAUSLOW 12.0     // for global/slow inhibition

 # define ADAPTSTRENGTH .01 // Impact of adaptation (scaling factor)
 # define TAUADAPT    15.0  // "speed" of f.rate integration into adapt.

 # define TAU_AVG_RATES  10.0 // "speed" of f.rate integration into avg.
 # define AVG_RATES_TIME 30   // length of period over which avg. is taken

/* ***************** Random firing activity generation ************* */
 # define r0 0.003
 # define r1 0.5
 # define SFUNC(_x) bool_noise( r0+r1*TLIN(_x) )

/* ***************** Rate functions of different cells  ************ */

 # define FUNCI(x) TLIN(x)   // For inhibitory cells
 # define FUNC(x)  RAMP(x)   // For excitatory cells

 # define SIGMOID(_x) ( 1.0 / ( 1.0+exp(-2.0*(_x)) ) )   // ? is this used?..

/* ********************* Kernels & synaptic values ***************** */

 # define NFFB1 19      // x/y sizes of forward & backward projections
 # define NFFB2 19
 # define NREC1 19      // x/y sizes of recurrent projections
 # define NREC2 19
 # define NINH1 5       // x/y sizes of inhibitory projections
 # define NINH2 5

 /* X- and Y-direction standard deviation of the Gaussian for..      */
 # define SIGMAX 6.5       // FF/BB projections
 # define SIGMAY 6.5
 # define SIGMAX_REC 4.5   // REC. projections
 # define SIGMAY_REC 4.5
 # define SIGMAX_INH 2.0   // INHIB. projections
 # define SIGMAY_INH 2.0

 # define J_PROB     .28   // Gauss. centre PROB. (FF & FB kernels)
 # define J_REC_PROB .15   // Gauss. centre PROB. (REC. kernels)
 # define J_INH_INIT .295  // Gauss. centre WEIGHT (inhib. kernels)
                           // (This has impact on how "deep" activity
                           //  penetrates the middle layers of the net)

 # define J_UPPER 0.1      // upper limit for initial synaptic WEIGHTs

 /* Synaptic bounds; max and min synaptic efficacies                 */
 # define JMIN .00000001   // MUST be greater than NO_SYNAPSE
 # define JMAX .225        // cf. J_INH_INIT, LTP_THRESH     <<<<----

/* **************** LEARNING / synaptic thresholds ***************** */

 # define LTP_THRESH  0.15  // Postsynaptic pot. required for LTP
 # define LTD_THRESH  0.15   // Postsynaptic pot. required for LTD
 # define F_THRESH    0.05   // Presyn. firing rate required for LTP/LTD

 /* NO_SYNAPSE is the weight that synapses that should NOT exist are */
 /* initialised to (these synapses shouold remain FIXED: no learning)*/

 # define NO_SYNAPSE 0.0

/* ***********  File names for Saving / Loading net data *********** */

 # define NET_WR "net%d.dat"
 # define NET_RD "net.dat"
 # define CA_WR "CA-structure.txt"

/* ***************** For AUTOMATED TRAINING of the net ************* */

 # define PAUSE_TIME 30  // Duration of pause betw. inputs (time-steps)
 # define INPUT_TIME 16  // Duration of input presentation (time-steps)
 # define SAVE_CYCLE 500 // Net is saved every SAVE_CYCLE input pres.
 # define LEARN_RATE 8   // learning rate applied during training
 # define TOT_TRAINING 4000 // Tot. no. patt. presentations 4 training

 # define SLOWAREA1 AREA1 // 1st area used for global inhib. decay check
 # define MAXINHIB1 0.75  // max. inhib. in SLOWAREA1 b4 input switch
 # define SLOWAREA2 AREA3 // 2nd area used for glob. inhib. decay check
 # define MAXINHIB2 0.65  // max. inhib. in SLOWAREA2 b4 input switch

 # define ROW_1 1     // Codes for multiplexing the sensory/motor input
 # define ROW_2 2     // to different "rows" of the network
 # define ALL_ROWS 3  // (row 1 == DORSAL, row 2 == VENTRAL)

/* **************** For AUTOMATED TESTING of the net *************** */

 # define TESTING FALSE       // TRUE <=> runs in automatic testing mode
 # define GINHIB_TESTING 0.35 // g.inh. level required to start testing
 # define GINHIB_TEST_AREA AREA3   // area where to check g.inh. level
 # define DATA_WR "DataOut.txt"    // where to save data during testing
 # define STIM_DURATION 2     // (in simulation time-steps)
 # define PRINTSTEPS 25       // No. of steps to be recorded (per trial)
 # define TOT_REPET 12        // Number of CA stimulation repetitions
 # define STOPTEST_PHASE 6    // If test_phase == 6, testing will stop
 # define STARTTEST_PHASE 1   // If test_phase == 1, testing will start

/* ***************************************************************** */
/* ************     GLOBAL dynamic variables     ******************* */
/* ***************************************************************** */

int stp,            // Simulation TIME-STEP counter
    last_stp,       // 4 TRAINING: last time-step of input switch
    training_phase, // 4 TRAINING: current phase (PAUSE or INPUT)
    stps_2b_avgd,   // 4 TRAINING: f.rates averaging counter (# steps)
    test_phase,     // 4 TESTING: current testing phase
    stimRepet,      // 4 TESTING: number of repeated stimulations
    stimCA;	    // 4 TESTING: CA currently being stimulated

int* freq_distrib;  // array containing freq. of pattern presentations

float noise_fac,    // amplitude of spontaneous firing rate
      total_output; // Sum of ALL cell's OUTPUT (firing rate)

Vector  pot,       // (Entire network's) excitat. cells' potentials
        inh,       // inhib. cells' potentials
        adapt,     // adaptation of all excit cells
        rates,     // firing rates (output) of excitatory cells
        avg_patts, // time-average of cells' f.rates (pattern specific)
        ca_ovlps,  // overlaps between emerging CA patts. (in each area)
        ovlps;     // "   " betw. current activity & CA patts. ("   " )

bVector sensInput,  // current inputs (NYAREAS areas) to "left" (sensory)
        motorInput; // current inputs (NYAREAS areas) to "right" (motor)

bVector sensPatt,  // Fixed input patterns (NYAREAS x P) to the left
        motorPatt; // Fixed input patterns (NYAREAS x P) to the right

Vector linkffb, linkrec, linkinh, // Post-syn. potentials in input to area
       tempffb,                   // auxiliary (EPSPs from diff. areas)
       clampSMIn;       // Incoming sesnory OR motor input to one area

Vector slowinh;         // slow inhib (1 cell per area)
bVector diluted,        // All "dead" cells
        above_thresh,   // Cells CURRENTLY firing above CA_THRESHold
	above_hstory;   // "history" of above_thresh vector activation

bVector ca_patts; // CA patterns emerging as a result of the training

Vector tot_LTP,   // Sum of synaptic weight *increase* (in each area)
       tot_LTD;   // Sum of synaptic weight *decrease* (in each area)

FILE *fi;         // file handle for writing data during TESTING

/* **** Matrix specifying the network's Connectivity structure ***** */
//
// A "1" at coord. (x,y) means Area #x ==> Area #y
//
                         //             to area
char K[NAREAS*NAREAS] =  //  1  2  3  4  5  6   7  8  9  10 11 12
                          {
                             1, 1, 0, 0, 0, 0,  //   1
                             1, 1, 1, 0, 0, 0,  //   2
                             0, 1, 1, 1, 0, 0,  //   3
                             0, 0, 1, 1, 1, 0,  //   4
                             0, 0, 0, 1, 1, 1,  //   5
                             0, 0, 0, 0, 1, 1   //   6   from area

                          };


Vector J;  // ALL KERNELS of the network are (linearly) stored in J[].
           // Each "element" is a vector of NSQR1 values (syn. weights)
           // J[Row,Col] = kernel/links FROM area #(Row) TO area #(Col)

Vector Jinh; // Contains the ONE and only inhibitory (Gauss.) kernel


/* ***************************************************************** */
/* Declaration and definition of graphical interface                 */
/* ***************************************************************** */

 SwitchValue sSInp = TRUE;      // activates all sensory inputs (left)
 SwitchValue sMInp = TRUE;      // activates all motor inputs (right)
 SwitchValue sdilute  = FALSE;  // lesion the network
 SwitchValue ssaveNet = FALSE;  // save current network (incl. kernels)
 SwitchValue sloadNet = FALSE;  // load a network from file
 SwitchValue strainNet = TRUE;  // train the network with sens-mot. input
 SwitchValue sPrintTest = FALSE;// write to file current CA activity data
 SwitchValue sCA_ovlps = FALSE; // compute CAs (using CA_THRESH) & overlaps

 SliderValue sI0 = 0;           // baseline input to all excit. cells
 SliderValue snoise =  25;      // Noise intensity slider
 SliderValue sMInRow = NYAREAS+1; // which rows get sensory input: ALL
 SliderValue sSInRow = NYAREAS+1; // which rows get motor input: ALL
 SliderValue sSI0 = 0;          // Sensory input amplitude
 SliderValue sMI0 = 0;          // Motor input amplitude
 SliderValue sSInCol = 1;       // which column sens. input goes to
 SliderValue sMInCol = 1;       // which column motor input goes to
 SliderValue spatno = P+1;      // current sensorimotor input pattern
 SliderValue slrate = 0;        // learning rate (0 only at very start)
 SliderValue sdiluteprob = 0;   // dilute probability
 SliderValue sdilutearea = 0;   // 0 = ALL areas are damaged
 SliderValue sJffb = 500;       // Between-area (ff/fb) links strength
 SliderValue sJinh = 500;       // Local inhib. links strength
 SliderValue sJrec = 500;       // Within-area (recurrent) links strength
 SliderValue sJslow = 95;       // Global inhibition strength
 SliderValue sgain  = 1000;     // trasnform. funct.'s slope (in 1000ths)
 SliderValue stheta = 0;        // transformation function's threshold

BEGIN_DISPLAY

   long i,j, k, area;
   char label[30];

   SWITCH( "sensIn", sSInp)
   SWITCH( "motorIn", sMInp)
   SWITCH( "dilute", sdilute)
   SWITCH( "saveNet", ssaveNet);
   SWITCH( "loadNet", sloadNet);
   SWITCH( "trainNet", strainNet);
   SWITCH( "printTest", sPrintTest);
   SWITCH( "compCA/Ovlps", sCA_ovlps);

   SLIDER_COLUMNS( 2 )

   SLIDER( "I0", sI0, -1000, 1000 )           // Baseline input to cells
   SLIDER( "Noise",  snoise, 0, 1000 )
   SLIDER( "Sens. inp. Row", sSInRow, 1, NYAREAS+1) // To multiplex sens.
   SLIDER( "Motor inp. Row", sMInRow, 1, NYAREAS+1) // and motor input
   SLIDER( "Sens. inp. Col.", sSInCol, 1, NXAREAS/2)
   SLIDER( "Motor inp. Col.", sMInCol, NXAREAS/2+1, NXAREAS)
   SLIDER( "Sens. stim. Amp.", sSI0, 0, 1000) // Amplitude of sens. stim.
   SLIDER( "Motor stim. Amp.", sMI0, 0, 1000) // Ampl. of motor stim.
   SLIDER( "Pattern no.", spatno, 0, P+1)     // which pattern to present
   SLIDER( "Learn", slrate, 0, 1000)        // Learning rate
   SLIDER( "Dilute prob", sdiluteprob, 0, 100)
   SLIDER( "Dilute area", sdilutearea, 0, NAREAS)
   SLIDER( "Jffb", sJffb, 0, 5000)          // ff/backward links strength
   SLIDER( "Jrec", sJrec, 0, 5000)          // recurrent    "      "
   SLIDER( "Jinh", sJinh, 0, 5000)          // local inhib.  "      "
   SLIDER( "J-slow", sJslow, 0, 5000)       // Global inhib. strength
   SLIDER( "gain", sgain, 0, 5000)          // Transf. function's slope
   SLIDER( "theta", stheta, 0, 5000)        // Transf. funct.'s threshold



   /* ************************************************************** */
   /* ***************** DEFINE ALL THE WINDOWS ********************* */

   /* ************************************************************** */
   /* NB: the way in which the cell potentials are displayed implies */
   /* that the "linear" order in the vector is Area1,Area2,.. Area12 */

   WINDOW("Potentials")

   for (j=0, area=0; j<NYAREAS; j++)  // For each ROW of areas:
   {
     sprintf( label, "Sens. inp. %d",j+1);
     IMAGE( strdup(label), NR, C0, &sensInput[N1*j], bVECTOR, N11, N12,
					            0., 1., ZOOMFACT)
     for (i=0; i<NXAREAS; i++, area++) // Display all areas on New columns
     {
       sprintf( label, "Area %d", area+1);
       IMAGE( strdup(label), AR, NC, &pot[N1*area], VECTOR, N11, N12,
                                                   -.25, 1., ZOOMFACT)
     }
     sprintf( label, "Motor inp. %d",j+1);
     IMAGE( strdup(label), AR, NC, &motorInput[N1*j], bVECTOR, N11, N12,
	                                            0., 1., ZOOMFACT)
   }

   /* ************************************************************** */

   WINDOW("Current firing rates")

   for (j=0, area=0; j< NYAREAS; j++)  // For each ROW of areas:
   {
     sprintf( label, "Sens. inp. %d",j+1);
     IMAGE( strdup(label), NR, C0, &sensInput[N1*j], bVECTOR, N11, N12,
					            0., 1., ZOOMFACT)
     for (i=0; i<NXAREAS; i++, area++) // Display all areas on New columns
     {
       sprintf( label, "Area %d", area+1);
       IMAGE( strdup(label), AR, NC, &rates[N1*area], VECTOR, N11, N12,
                                                   -.1, .2, ZOOMFACT)
     }
     sprintf( label, "Motor inp. %d",j+1);
     IMAGE( strdup(label), AR, NC, &motorInput[N1*j], bVECTOR, N11, N12,
	                                            0., 1., ZOOMFACT)
   }

   /* ************************************************************** */

   WINDOW("Sensory input patterns")

   for (j=0; j<NYAREAS; j++)      // For each ROW of areas:
   {
     // Patt. #1 on a New ROW, Column 0
     IMAGE( "Pat. #1", NR, C0, &sensPatt[P*N1*j], bVECTOR,
                                         N11, N12, 0., 1., ZOOMFACT)

     for (i=1; i<P; i++)           // For all remaining patterns
     {                             // display them on New Columns
       sprintf( label, "Pat. #%d", i+1);
       IMAGE( strdup(label), AR, NC, &sensPatt[(P*N1)*j + N1*i],
                                 bVECTOR, N11, N12, 0., 1., ZOOMFACT)
     }
   }

   /* ************************************************************** */

   WINDOW("Motor input patterns")

   for (j=0; j< NYAREAS; j++)      // For each ROW of areas:
   {
     // Patt. #1 on a New ROW, Column 0
     IMAGE( "Pat. #1", NR, C0, &motorPatt[P*N1*j],
	                          bVECTOR, N11, N12, 0., 1., ZOOMFACT)

     for (i=1; i<P; i++)           // For all remaining patterns
     {                             // display them on New COLUMNS
       sprintf( label, "Pat. #%d", i+1);
       IMAGE( strdup(label), AR, NC, &motorPatt[(P*N1)*j + N1*i],
                                  bVECTOR, N11, N12, 0., 1., ZOOMFACT)
     }
   }

   /* ************************************************************** */

   WINDOW("Total network output")

   sprintf( label, "Change scale");
   GRAPH( strdup(label), NR, AC, &total_output, FLOAT_TYPE, 0, 0, 0, 0, -0.5, N1/2)

   /* ************************************************************** */

   WINDOW("Slow Inhib")

   GRAPH( "Select area", AR, AC, slowinh, VECTOR, NAREAS, 0, 0, 0, 0, 1 )

   /* ************************************************************** */

   for (k=0; k<P; k++) // For each pattern n-tuple (if sensory/motor,
                       // dorsal/ventral, then 1 pattern is a 4-tuple)
   {
      sprintf( label, "CA #%d", k+1);
      WINDOW( strdup(label) )        // CREATE 1 WINDOW PER CA-PATTERN

      for (j=0, area=0; j<NYAREAS; j++)  // For each ROW of areas:
      {
        sprintf( label, "Area %d", area+1);
        IMAGE( strdup(label), NR, C0, &avg_patts[N1*(NAREAS*k+area)],
                                 VECTOR, N11, N12, -.1, .2, ZOOMPATFACT)
	area++;
        for (i=1; i<NXAREAS; i++, area++) // Each area on a New Column
        {
          sprintf( label, "Area %d", area+1);
          IMAGE( strdup(label), AR, NC, &avg_patts[N1*(NAREAS*k+area)],
                                VECTOR, N11, N12, -.1, .2, ZOOMPATFACT)
	}
      }
   }


   /* ************************************************************** */
   /* For each area, display all INCOMING kernels (incl. RECurrent). */
   /* For any area n, these are on n-th COLUMN of matrix J[].        */

   for (i=0; i<NAREAS; i++)      // For each DESTINATION area "i+1"
   {
     sprintf( label, "Area #%d's kernels", i+1);

     WINDOW( strdup(label) )

     for (j=0; j<NAREAS; j++)     // For each ORIGIN area "j+1"
     {
       sprintf( label, "From #%d", j+1);

       if (j==i)
        IMAGE_ARRAY(  strdup(label) , AR, NC, &J[ NSQR1*(NAREAS*j +i) ],
            MATRIX, NREC1, NREC2, N11, N12, 0, 0, JMIN, JMAX,  ZOOMFACT)
       else
         IMAGE_ARRAY(  strdup(label) , AR, NC, &J[ NSQR1*(NAREAS*j +i) ],
            MATRIX, NFFB1, NFFB2, N11, N12, 0, 0, JMIN, JMAX,  ZOOMFACT)
     }
   }

   /* ************************************************************** */

   WINDOW("Inhib. kernel(s)")

     IMAGE( "Inhib. kernel", NR, C0, Jinh, VECTOR, NINH1, NINH2,
                                               JMIN, JMAX, ZOOMFACT*3)

   /* ************************************************************** */

   WINDOW("LTP")

     GRAPH( "LTP", AR,AC, tot_LTP, VECTOR, NAREAS, 0, 0, 0, -0.5, 1)

   WINDOW("LTD")

     GRAPH( "LTD", AR,AC, tot_LTD, VECTOR, NAREAS, 0, 0, 0, -0.5, 1)


   WINDOW("Between-CAs overlaps")

   for (j=0, area=0; j< NYAREAS; j++, area++) // For each ROW of areas:
   {
     sprintf( label, "A%d", area+1);
     IMAGE( strdup(label), NR, C0, &ca_ovlps[area*P*P], MATRIX, P, P,
					       0.0, 1., OVRLPZOOMFACT)
     for (i=1; i<NXAREAS; i++)   // Display all areas on New columns
     {
       area++;
       sprintf( label, "A%d", area+1);
       IMAGE( strdup(label), AR, NC, &ca_ovlps[area*P*P], MATRIX, P, P,
					       0.0, 1., OVRLPZOOMFACT)
     }
   }

   WINDOW("Scalar(CA x Activy)")

   for (j=0, area=0; j< NYAREAS; j++, area++) // For each ROW of areas:
   {
     sprintf( label, "A%d", area+1);
     RASTER( strdup(label), NR, C0, &ovlps[area*P], VECTOR, P, 0, 0.0,
	                                            NONES/2, OVRLPZOOMFACT)

     for (i=1; i<NXAREAS; i++)   // Display all areas on New columns
     {
       area++;
       sprintf( label, "A%d", area+1);
       RASTER( strdup(label), AR, NC, &ovlps[area*P], VECTOR, P, 0, 0.0,
                                                NONES/2, OVRLPZOOMFACT)
     }
   }


END_DISPLAY

NO_OUTPUT


/*********************************************************************/
/*****************        AUXILIARY ROUTINES        ******************/
/*********************************************************************/

/* ***************************************************************** */
/* Creates p binary random vectors of length n, where "nones" units  */
/* are="1" at random positions. "pats" is the array of vectors/patts */

 static void gener_random_bin_patterns(
                             int n,    // IN: no. cells per pattern
                         int nones,    // IN: no. of "1"s per patt.
                             int p,    // IN: tot. no. patterns
                      bVector pats)    // OUT: the array of patterns
 {
   int np, i, j;
   bVector temp_pat;             // temporary pointer

   Clear_bVector( n * p, pats);  // clear content of ALL patterns

   for (j=0; j<p; j++)           // for each pattern
   {
     /* Get pointer to 1st cell of current binary pattern            */
     temp_pat=&pats[n*j];
     for ( i = 0; i < nones; i++)   // For all cells of this pattern
       temp_pat[ random() % n ] = 1;

     /* It may be that two or more "1"s happen to coincide...        */
     while ( bSum( n, temp_pat) < nones)  // inefficient, but fast enough
       temp_pat[ random() % n ] = 1;
   }
 }

/* ***************************************************************** */
/* Initializes nx*ny kernels of size mx*my in the Array J with Gaus- */
/* sian profile - sigmax and sigmay are standard deviations of the   */
/* Gaussian in x and y direction; ampl is scaling factor (= amplit.  */
/* of the Gaussian function at the center, point (0,0) ).            */

 static void init_gaussian_kernel(
                     	 int nx, int ny, // IN: area size (1cell<=>1kernel)
			 int mx, int my, // IN: kernel size
			       Vector J, // OUT: the kernels (linearised)
 	     float sigmax, float sigmay, // IN: std. deviations
	 	    	     float ampl) // IN: value at Gaussian center
 {
    int x, y, cx, cy, i, j, mm;
    float h, h1, h2;

    cx = mx/2;
    cy = my/2;

    h1 = 1./(sigmax*sigmax);
    h2 = 1./(sigmay*sigmay);

    /* set up kernel (0,0) */

    for (x=0; x<mx; x++)
      for (y=0; y<my; y++)
      {
        h = (x-cx)*(x-cx)*h1 + (y-cy)*(y-cy)*h2;
        J[y*mx + x] = ampl*exp(-h);
      }

    /* copy kernel (0,0) to other locations */
    mm = mx*my;
    for (i=1; i<nx*ny; i++)
      bcopy( J, &J[i*mm], mm*sizeof(float) );
 }

/* ***************************************************************** */
/* This routine initializes nx*ny kernels of size mx*my in the Array */
/* J such that the probability of creating a synapse follows a Gaus- */
/* sian distribution falling with distance from center with standard */
/* deviations sigmax and sigmay in x and y direction and probability */
/* "prob" for the synapses at the center. If a synapse is present,   */
/* its value will be a random no. in range [0,upper[. Otherwise, the */
/* synaptic value is set to NO_SYNAPSE (indicating a FIXED synapse). */

 static void init_patchy_gauss_kern(
 			int nx, int ny, // IN: area size (1kern/cell)
		        int mx, int my, // IN: kernel size
                              Vector J, // OUT: the actual Kernels
	    float sigmax, float sigmay, // IN: std. deviations
                            float prob, // IN: Gaussian amplitude
                           float upper) // IN: upper synaptic value
 {
   int i;

   /* Checks that max. probability is within bounds                  */
   if (prob < 0.0 || prob > 1.0)
   {
     fprintf(stderr, "ERROR: init_<..>_kernel() probab. not in [0,1]\n");
     exit(-1);
   }

   /* First, we compute the probabilities...                         */
   init_gaussian_kernel( nx, ny, mx, my, J, sigmax, sigmay, prob );

   /* ...then transform them into the requested synaptic values.     */
   for (i=0; i<nx*ny*mx*my; i++)
     J[i] = bool_noise( J[i] ) ? upper*equal_noise() : NO_SYNAPSE;
 }


/* ***************************************************************** */
/* "Train" all the synapses connecting area X to area Y (incl. X==Y) */

 static void train_projection_cyclic(
  	     Vector pre,   // IN: area X cells' firing rates (output)
        Vector post_pot,   // IN: area Y cells' memb. potentials
               Vector J,   // IN/OUT: all the kernels connecting X to Y
         int nx, int ny,   // IN: area dimensions (2 areas of same size)
         int mx, int my,   // IN: kernels' x and y's dimensions
            float hrate,   // IN: learning rate (weight increm/decrem.)
          float* totLTP,   // OUT: tot. amount of LTP
          float* totLTD)   // OUT: tot. amount of LTD
 {
   int i, j, ij, k, l, m;
   int kx2=mx/2, ky2=my/2, mxy = mx*my;
   Vector kern;          // Temp. pointer to 1 synaptic link
   float pre_D, post_D;  // Auxiliary: pre-syn. firing, post-syn. pot.

   kern = J;             // Addr. of 1st (potential) link betw. X and Y

   for (i=0, ij=0; i<ny; i++)       // For all cells in area Y
     for (j=0; j<nx; j++,ij++)      // ("ij" counts tot. # of cells)
       for( k=-ky2; k<=ky2; k++ )          // For all links of 1 kernel
         for( l=-kx2; l<=kx2; l++, kern++) // ("kern" counts tot. #links)
         {
           m = ((i+k+ny)%ny)*nx + (j+l+nx)%nx; // Get index of cell in X

           /* Check if synapse considered "exists" (i.e. is <> 0.0 ) */
           if (*kern != NO_SYNAPSE)
           {
             /* Synapse exists; update its weight using learning rule*/

             pre_D = pre[m];   //  Get pre-synaptic activity (f. rate)

             /* Check if post-synapt. pot. is above LTP threshold    */
             if ( post_pot[ij] > LTP_THRESH )
             {
               if (pre_D > F_THRESH)  // Is there suff. pre-syn. activ.?
               {
                 if (*kern < JMAX)    // Yes; reached MAX syn. weight?..
	         {
                   *kern += hrate;    // Not yet: Homosynaptic LTP
	           *totLTP += hrate;  // Update TOT. amount of LTD
                 }
	       }
               else                   // NO (i.e., pre_D <= F_THRESH)
               if (*kern > JMIN)      // Reached MIN synapt. weight?..
               {
                 *kern -= hrate;      // Not yet: "low"-homo or hetero LTD
		 *totLTD += hrate;    // Update TOT. amount of LTD
                 if (*kern < JMIN)    // Make sure not to go below...
		           *kern = JMIN;
               }
	     }
             else  // IN THIS CASE: post_pot <= LTP_THRESH

    	       /* Are post. pot. & presyn. firing right for LTD?     */
	       if ( (pre_D>F_THRESH) && (post_pot[ij]>LTD_THRESH)
                                     && (*kern > JMIN) )
	       {
                 *kern -= hrate;      // Yes: homosynaptic LTD
	         *totLTD += hrate;    // Update TOT. amount of LTD
                 if (*kern < JMIN)
		           *kern = JMIN;
	       }
           }
         }
 }

/* ***************************************************************** */
/* Visualise (as text output) the links of connectivity matrix K[].  */

 static void display_K ( )
 {
   int i,j;

   printf("\n");
   for (i=0; i<NAREAS; i++)
   {
     printf( "Area %d receives from ", i+1);
     for (j=0; j<NAREAS; j++)
       if ( K[NAREAS*j+i] )
         printf( " %d", j+1);

     printf( "\n");
   }
 }

/* ***************************************************************** */
/* Compute the emerging Cell Assemblies using specified threshold    */

 static void compute_CApatts( float threshold)
 {
  int area, i;
  float max_act;

  for (area=0; area< NAREAS; area++)  // For all areas
    for (i=0; i<P; i++)               // for all input pattern pairs
    {
      /* Get f.rate of maximally responsive cell in current area     */
      max_act = Max_Elem(N1, &avg_patts[N1*(NAREAS*i+area)] );

      /* Is there AT LEAST 1 cell strongly responsive?..         */
      if (max_act >= MIN_CELLRATE)

	/* If cell rate > thresh set cell to 1 in 'ca_patts'     */
	Fire (N1, &avg_patts[N1*(NAREAS*i+area)], threshold*max_act,
	           &ca_patts[N1*(NAREAS*i+area)] );

        /* Else: NO cells are set to 1 in the 'ca_patts' vector  */
    }
 }

/* ***************************************************************** */
/* Write no. of CA-cells of all CA.s to file (for all CA.s & areas). */
/* CAs are computed by the above routine "compute_CApatts(thresh)".  */

static void write_CApatts( )
 {
  int area, i;
  FILE *fiCA;

  fiCA = fopen(CA_WR, "a" );  // Open the file for append (or writing)
  if (fiCA==0)                // Has the file not opened correctly?...
    printf("\n ERROR: Could not open file '%s' for writing.\n", CA_WR);
  else
  {
    for (i=0; i<P; i++)                  // For all CAs (patterns)
	{
	  fprintf (fiCA, " \n CA #%d: ", i+1);
	  for (area=0; area<NAREAS; area++)  // for all areas

	    /* Write to file tot. no. of CA cells for this CA and area   */
 	    fprintf (fiCA, "%d ", bSum(N1, &ca_patts[N1*(NAREAS*i+area)]));
	}
    printf("\n\n");
    fclose(fiCA);
  }
 }

/* ***************************************************************** */
/* Compute the PxP overlaps between the emerging Cell Assemblies     */

 static void compute_CAoverlaps( )
 {
  int area, i, j;

  for (area=0; area<NAREAS; area++)
    for (i=0; i<P; i++)
      for (j=0; j<P; j++)

	  ca_ovlps[ P*(P*area+i) +j] = (float)bbSkalar ( N1,
                        &ca_patts[N1*(NAREAS*i+area)],
                        &ca_patts[N1*(NAREAS*j+area)] ) / (float)NONES;
 }

/* ***************************************************************** */
/* Reset completely the network activity (the synaptic weights are   */
/* left untouched). Recent "history" of TESTING activity is erased.  */

 static void resetNet()
 {
  int i;

  Clear_Vector( NAREAS * N1, pot);
  Clear_Vector( NAREAS * N1, inh);
  Clear_Vector( NAREAS * N1, adapt);
  Clear_Vector( NAREAS * N1, rates);
  Clear_Vector( NAREAS, slowinh );
  Clear_Vector( NAREAS, tot_LTP );
  Clear_Vector( NAREAS, tot_LTD );
  Clear_bVector( NAREAS * N1 * P, above_hstory);

  total_output = 0.0;
 }


/*********************************************************************/
/**********************   INITALISATION CALLS   **********************/
/*********************************************************************/

/* ***************************************************************** */
/* main_init() is called when simulation PROGRAM is started. It does */
/* all initialisations the need to be done only ONCE at startup, eg. */
/* getting memory for data structures, init. random numbers, etc.    */

 int main_init()
 {
   SET_STEPSIZE( STEPSIZE )

   /* Random numbers generation                                      */
   srandom( time(NULL) );
   randomize( time(NULL) );
   noise_fac = sqrt(24.0/STEPSIZE);  // if STEPSIZE=0.5, noise_fac ~= 6.93

   pot = Get_Vector( NAREAS * N1 );  // Membr. pot. of ALL excit. cells
   rates = Get_Vector( NAREAS * N1 );// Firing rates of ALL excit. cells
   inh = Get_Vector( NAREAS * N1 );  // M. potential of ALL inhib. cells
   avg_patts = Get_Vector( NAREAS * N1 * P); // patt.-specific f.rates avg.
   ca_patts = Get_bVector( NAREAS * N1 * P); // emerging Cell Assemblies
   ca_ovlps = Get_Vector( NAREAS * P * P);   // Per-area overlaps betw. CAs
   ovlps = Get_Vector( NAREAS * P);  // Ovlps. betw. CAs & current activity

   slowinh = Get_Vector( NAREAS );      // M. potential of G. Inhib. cells
   adapt = Get_Vector( NAREAS * N1 );   // Adaptation of ALL excit. cells
   diluted = Get_bVector( NAREAS * N1 );// Lesion mask (1 <=> lesioned)

   above_thresh = Get_bVector( NAREAS * N1); // cells CURRENTLY > thresh
   above_hstory = Get_bVector( NAREAS * N1 * P); // above_thresh's history
                                                 // (pattern specific)
   tot_LTP = Get_Vector ( NAREAS );
   tot_LTD = Get_Vector ( NAREAS );

   sensInput = Get_bVector( NYAREAS * N1 );
   motorInput = Get_bVector( NYAREAS * N1 );

   sensPatt = Get_bVector( NYAREAS*P*N1 );
   motorPatt = Get_bVector( NYAREAS*P*N1 );

   freq_distrib = (int*)calloc( P, sizeof(int) ); // array of freq. pres.

   /* Kernels: we allocate bigger arrays than we actually need (each */
   /* el. can contain up to NSQR1 synapses = all-to-all connectivity)*/

   J = Get_Vector( NAREAS * NAREAS * NSQR1 ); // NAREAS*NAREAS couplings
   Jinh = Get_Vector ( N1 );   // 1 inhib. kernel with at most N1 links

   /* Vectors of post-synapt. pot. incoming to each cell of one area */
   linkffb = Get_Vector( N1 );  // EPSPs from OTHER (between-) areas
   linkrec = Get_Vector( N1 );  // EPSPs from THIS area (recurrent)
   linkinh = Get_Vector( N1 );  // Inh.Post-Syn. Pot from inhib. layer
   tempffb = Get_Vector( N1 );  // auxiliary (used for temp. EPSPs)
   clampSMIn = Get_Vector( N1); // "Clamp" input from sensorimotor patt.
 }

/* ***************************************************************** */
/* ***************************************************************** */

/* init() is called whenever "INIT" or "RUN" buttons in the GUI are  */
/* pressed; it initialises individual simulation runs                */

 int init()
 {
   int i,j;

   Clear_Vector (NAREAS * N1, pot);
   Clear_Vector (NAREAS * N1, rates);
   Clear_Vector (NAREAS * N1, adapt);
   Clear_Vector (NAREAS * N1 * P, avg_patts);
   Clear_bVector (NAREAS * N1 * P, ca_patts);
   Clear_Vector (NAREAS * P * P, ca_ovlps);
   Clear_Vector (NAREAS * P, ovlps);
   Clear_bVector (NAREAS * N1, diluted);
   Clear_Vector (NAREAS * N1, inh);
   Clear_Vector (NAREAS, slowinh );
   Clear_bVector (NYAREAS * N1, sensInput);
   Clear_bVector (NYAREAS * N1, motorInput);
   Clear_bVector (NYAREAS * P * N1, sensPatt);   // NYAREAS rows x P col.
   Clear_bVector (NYAREAS * P * N1, motorPatt);  // NYAREAS rows x P col.
//  Clear_bVector (NAREAS * NAREAS, K);
   Clear_bVector (NAREAS * N1, above_thresh);
   Clear_bVector (NAREAS * N1 * P, above_hstory);
   total_output = 0.0;

   for (i=0; i<P; i++)
     freq_distrib[i] = 0;

   /* ************************************************************** */
   /*    Randomly initialise all sensorimotor input patterns         */
   gener_random_bin_patterns( N1, NONES, NYAREAS*P, sensPatt);
   gener_random_bin_patterns( N1, NONES, NYAREAS*P, motorPatt);

   /* ************************************************************** */
   /* **************** INITIALISE ALL THE KERNELS ****************** */

   Clear_Vector (NAREAS * NAREAS * NSQR1, J);

   for (j=0; j<NAREAS; j++)
   {
     for (i=0; i<NAREAS; i++)

       if (j==i && K[(NAREAS+1)*j]) // Does area j have REC. links ?..

         init_patchy_gauss_kern( N11, N12, NREC1, NREC2, &J[ NSQR1*(NAREAS*i+i) ], 
                          SIGMAX_REC, SIGMAY_REC, J_REC_PROB, J_UPPER);
       else

         if (K[NAREAS*j+i])         // Does AREA (j+1) --> (i+1)?...

           init_patchy_gauss_kern( N11, N12, NFFB1, NFFB2, &J[ NSQR1*(NAREAS*j+i) ],
                                   SIGMAX, SIGMAY, J_PROB, J_UPPER);
    }

    /* There is only 1 inhibitory kernel (FIXED & identical for all) */
    init_gaussian_kernel(1, 1, NINH1, NINH2, Jinh,
                         SIGMAX_INH, SIGMAY_INH, J_INH_INIT);

   /* ************************************************************** */
   /* If dilute switch is pressed, "damage" the appropriate area(s)  */
   /* ("sdilutearea" slider indicates area to be lesioned; 0==ALL)   */
   /* NB: this is only executed ONCE, at network INITIALISATION.     */

   if (sdilute)
   {
     int i, area;
     float h;
     bVector pdil;

     for (area=0; area<NAREAS; area++)  // For each area
     {
       h = .01*sdiluteprob;             // sdiluteprob: a slider value
       if(sdilutearea == 0  || (area+1) == sdilutearea)
       {
         pdil = &diluted[N1*area];      // temp. pointer to this area

	 /* A "1" in vector "diluted" will mean that cell is damaged */
         for (i=0; i<N1; i++)
           pdil[i] |= bool_noise(h);
       }
     }
     SET_SWITCH( sdilute, FALSE )
   }

   training_phase = 0;       // Init. training phase (used in TRAINING)
   stps_2b_avgd = 0;         // Reset averaging steps count (4 TRAINING)
   test_phase = 0;           // initialise testing phase (4 TESTING mode)
   stimRepet = 0;            // Counter (no. of stimulation repetitions)

   stp = 0;                  // Initialise simulation-step
 }

/* ***************************************************************** */
/* ******  MAIN  "STEP" FUNCTION, executed at each sim. step  ****** */
/* ***************************************************************** */

int step()
{
  int i,j,k, area;          // counters
  FILE *fi0, *fi1;          // File handlers for saving/loading networks

  float hrate=.0001*slrate; // Get & rescale LEARN. rate specif. by slider
  float gain=.001*sgain;    // Get & rescale GAIN value specif. by slider
  float theta=.001*stheta;  // Get & rescale THRESH. value "    "   " "
  float noise=.0001*snoise; // Get & rescale NOISE (for "input" areas)

  bVector pdil, pinput, pabove;                  // temp. pointers used
  Vector ppot, prates, prates_avg, pinh, padapt; // repeatedly in step()

  /* *************************************************************** */
  /* ***** Save the entire network to file (incl. input patts.) **** */

  if (ssaveNet)
  {
    int elemJ;
    char label[30];

    /* Fill label with NET_WR and tot. no. of patt.#1's presentations */
    sprintf( label, NET_WR, freq_distrib[0]);

    fi0 = fopen( label, "w" ); // Open the file for writing
    if (fi0==0)                // Has the file not opened correctly?...
      printf("\n ERROR: Could not open file '%s' for writing.\n", label);
    else
    {
      fwrite( K, sizeof(char), NAREAS*NAREAS, fi0 );
      fwrite( sensPatt, sizeof(char), (N1*NYAREAS*P), fi0 );
      fwrite( motorPatt, sizeof(char), (N1*NYAREAS*P), fi0 );
      fwrite( avg_patts, sizeof(float), (N1*NAREAS*P), fi0 );

      /* Write only kernels of existing projections (to save memory)   */
      for (i=0; i<NAREAS; i++)   // For all DEST. areas (i+1)
        for (j=0; j<NAREAS; j++)  // For all ORIGIN areas (j+1)
          if ( K[NAREAS*j+i] )     // Does area (j+1)-->(i+1)?
		  {
			elemJ = NSQR1*(NAREAS*j+i); // index of corresp. kern. in J[]
            fwrite( J+elemJ, sizeof(float), NSQR1, fi0 );   // write it
          }

      /* Write patterns' frequencies of presentations                  */
      for (i=0; i<P; i++)
        fwrite( (freq_distrib+i), sizeof(int), 1, fi0);

      fwrite( &stp, sizeof(int), 1, fi0 );     // current sim. time step
      fclose(fi0);
    }
    SET_SWITCH( ssaveNet, FALSE );
  }

  /* *************************************************************** */
  /* ***** Load entire network from file (incl. input patts.)  ***** */

  if (sloadNet)
  {
    int elemJ;

    fi1 = fopen( NET_RD, "r"); // Open the file for reading
    if (fi1==0)                // Has the file not opened correctly?...
      printf("\n ERROR: Cannot open file '%s' for reading.\n", NET_RD);
    else
    {
      fread( K, sizeof(char), NAREAS*NAREAS, fi1 );
      fread( sensPatt, sizeof(char), (N1*NYAREAS*P), fi1);
      fread( motorPatt, sizeof(char), (N1*NYAREAS*P), fi1);
      fread( avg_patts, sizeof(float), (N1*NAREAS*P), fi1 );

      /* Read in only kernels of existing projections (to save mem.) */
      for (i=0; i<NAREAS; i++)   // For all DEST. areas (i+1)
        for (j=0; j<NAREAS; j++)  // For all ORIGIN areas (j+1)
          if ( K[(NAREAS*j+i)] )   // Does area (j+1)-->(i+1)?
		  {
            elemJ = NSQR1*(NAREAS*j+i); // index of corresp. kern. in J[]
            fread( J+elemJ, sizeof(float), NSQR1, fi1 );    // reads it
          }

      /* Read in all patterns' frequencies of presentations          */
      for (i=0; i<P; i++)
        fread( (freq_distrib+i), sizeof(int), 1, fi1);

      fread( &stp, sizeof(int), 1, fi1 );
      printf(" LOADED a NETWORK STATE reached at STEP %d \n", stp);
      for (i=0; i<P; i++)
        printf ("Patt.#%d was presented %d times.\n", i+1, freq_distrib[i]);

      display_K();
      fclose(fi1);
    }
    SET_SWITCH( sloadNet, FALSE );
  }

  /* *************************************************************** */
  /* *******************  MANAGE network TRAINING  ***************** */

   if ( strainNet )       // Is the "network training" switch pressed?

     switch (training_phase) // which TRAINING phase are we in?
     {

       /* ********************************************************** */
       /* PHASE 0: prepare for a "PAUSE" phase                       */
       case 0:
         last_stp = stp;               // record current time step
		 SET_SLIDER( spatno, P+1 );    // pattern no. P+1 == noise
         SET_SWITCH( ssaveNet, TRUE);  // Force writing data (net0.dat)
         training_phase++;             // move to next phase
       break;

       /* ********************************************************** */
       /* PHASE 1: PAUSE -- wait until an "INPUT" phase is due..     */
       case 1:
	 if ( (stp-last_stp) >= PAUSE_TIME // Have enough steps passed
          && slowinh[SLOWAREA1]<MAXINHIB1  // and glob. inhibition
	  && slowinh[SLOWAREA2]<MAXINHIB2 )// levels decayed enough?
	 {
	   int patt_no;                    // auxiliary var.

	   /* Pseudo-randomly select a number betw. 1 and P, ensuring*/
           /* that the patterns freq. distribution is approx. uniform*/
           patt_no = (int)(1234.56*equal_noise());
           do
	     patt_no = (patt_no % P) +1;
           while ( freq_distrib[patt_no-1] > freq_distrib[(patt_no%P)] );

	   SET_SLIDER( spatno, patt_no );

           stps_2b_avgd = AVG_RATES_TIME; // Set averaging steps-counter
	   freq_distrib[patt_no-1]++;     // Update presentation freq.
	   last_stp = stp;                // record current time step
	   training_phase++;
	 }
       break;

       /* ********************************************************** */
       /* PHASE 2: INPUT -- wait until a "PAUSE" phase is due..      */
       case 2:
         if ( (stp-last_stp) >=INPUT_TIME )// Have enough steps passed?
	 {
           int frq;                        // auxiliary var.

	   /* Is it time to save data or stop current simulation?    */
           frq = freq_distrib[0];          // get patt.#1's frequency
	   if (frq > TOT_TRAINING)         // Enough presentations?..
	     training_phase++;             // YES: END OF TRAINING - STOP
	   else
	   {
	     /* If no. presentations is multiple of SAVE_CYCLE OR is*/
	     /* < SAVE_CYCLE && multiple of 100, save the net. data */
	     if ( (frq > 0) &&
		( (frq%SAVE_CYCLE == 0) ||
		( (frq<=50) && (frq%10==0) ) ||
		( (frq<SAVE_CYCLE) && (frq%100==0) ) ) )

		SET_SWITCH( ssaveNet, TRUE); // Will write data to file

		SET_SLIDER( spatno, P+1 );  // spatno==P+1 ==> white noise
		last_stp = stp;             // Record current time
		compute_CApatts(CA_THRESH); // re-compute all CAs
		compute_CAoverlaps( );      // re-compute CA overlaps
		SET_SLIDER(slrate, LEARN_RATE); // Start (or continue) learning
		training_phase = 1;         // GO BACK to PHASE 1
           }
         }
       break;

       /* ********************************************************** */
       /* Otherwise STOP the training (when stp reaches TOT_TRAINING)*/
       default:
         SET_SWITCH( strainNet, FALSE);
         printf("\n End of training phase. \n");
         exit(0);
       break;
     }

  /* **************************************************************** */
  /* ********************  END TRAINING MANAGEMENT  ***************** */
  /* **************************************************************** */


  /* *************************************************************** */
  /* ************* SET UP THE CURRENT SENSORIMOTOR INPUT *********** */

  if (spatno == 0)               // 0 = no input: CLEAR all activity
  {
    Clear_bVector( NYAREAS*N1, sensInput );
    Clear_bVector( NYAREAS*N1, motorInput);
  }
  else                           // patno > 0: SOME input stimulation
  {
    /* ************************************************************* */
    /* Create white noise in ALL sensory & motor input areas (EXCEPT */
    /* if we are TRAINING the netw. AND a stim. is being presented). */
    /* Some areas might be later "overwritten" by "real" s-m. patts. */

    if (!strainNet || training_phase!=2) // If NOT training OR currently
					 // NOT presenting a stimulus..
      for (j=0; j<NYAREAS; j++) // For all "rows" of the net
      {
	/* Get addr. of sens. input area for current netw.'s "row"   */
        pinput = &sensInput[N1*j];

        /* Produce white noise there (noise def. at start of step() )*/
        for (i=0; i<N1; i++)
          pinput[i] = bool_noise( noise );

	/* Get addr. of motor input area for current netw.'s "row"   */
	pinput = &motorInput[N1*j];

	/* Produce white noise there (noise def. at start of step() )*/
	for (i=0; i<N1; i++)
	  pinput[i] = bool_noise( noise );
      }

    /* ******** COPY SENSORY PATTERNS to INPUT AREAS *************** */

    if (sSInp && (spatno<P+1)) // Is there a sens. patt. to be presented?
    {
      // Clear_bVector(NYAREAS*N1, sensInput); // clear all sens. input

      /* Copy the sens. patts. This should be repeated at every step,*/
      /* cause any slider (spatno, input row, etc) might have changed*/

      for (j=0; j<NYAREAS; j++)    // for each "row" of the network
      {
	/* Check whether this "row" of the net should get any input..*/
	if (sSInRow==(j+1) || sSInRow == NYAREAS+1) // NYAREAS+1 == ALL
	{
          /* Get pointer to relevant pattern in "sensPatt" matrix    */
          pinput = &sensPatt[ (P*N1)*j + N1*(spatno-1) ];

	  /* Copy the sensory pattern                                */
          for (i=0; i< N1; i++)
	    sensInput[(N1*j)+i] = pinput[i];
        }
      }
    }

    /* *********** COPY MOTOR PATTERNS to INPUT AREAS ************** */

    if (sMInp && (spatno<P+1)) // Is there a motor patt. to be presented?
    {
      // Clear_bVector(NYAREAS*N1, motorInput); // clear all motor input

      /* Copy the motor patts. This should be repeated at every step,*/
      /* cause any slider (spatno, input row, etc) might have changed*/

      for (j=0; j<NYAREAS; j++)     // for each "row" of the network
      {
	/* Check whether this "row" of the net should get any input..*/
	if (sMInRow == (j+1) || sMInRow == NYAREAS+1) // NYAREAS+1 == ALL
	{
          /* Get pointer to relevant pattern in "motorPatt" matrix   */
          pinput = &motorPatt[ (P*N1)*j + N1*(spatno-1) ];

	  /* Copy the motor pattern                                  */
          for (i=0; i< N1; i++)
	    motorInput[(N1*j)+i] = pinput[i];
        }
      }
    }
  }


  /* *************************************************************** */
  /* *************    COMPUTE NEW MEMBRANE POTENTIALS    *********** */

  for (area=0; area<NAREAS; area++)    // For ALL areas in the network
  {
    /* Define some helpful pointers (mostly for speed)               */
    ppot = &pot[N1*area];     // point to this area's memb. potentials
    pinh = &inh[N1*area];     // point to this area's inhib. cells
    pdil = &diluted[N1*area]; //  "   to this area's lesion "mask"

    /* Clear vectors containing incoming input to current area       */
    Clear_Vector (N1, linkffb );   // From OTHER areas
    Clear_Vector (N1, linkrec );   // From THIS area
    Clear_Vector (N1, linkinh );   // From inhib. layer
    Clear_Vector (N1, tempffb );   // auxiliary (used for OTHER areas)
    Clear_Vector (N1, clampSMIn);  // from sensory/OR/motor inp. patt.

    /* ************************************************************* */
    /* ********************** Sensorimotor input ******************* */

    /* Is this area (possibly) receiving a sensory pattern as input? */
    if (area%NXAREAS == sSInCol-1)
    {
      /* Yes: give any current sens. pattern as input to this area   */
      for(i=0; i<N1; i++)

        /* Note: sensInput[] is a column of NYAREAS elem. of size N1 */
        clampSMIn[i] = sSI0 * sensInput[N1*((int)area/NXAREAS)+i];
    }
    else
    {
      if (area%NXAREAS == sMInCol-1) // Area receiving motor patt.?

        for(i=0; i<N1; i++)

          /* NB: motorInput[] is a column of NYAREAS elem. of size N1*/
	  clampSMIn[i] = sMI0 * motorInput[N1*((int)area/NXAREAS)+i];
    }

    /* ************************************************************* */
    /* ****************  FF/fb (between area) input   ************** */

    for (j=0; j<NAREAS; j++) // Check all areas (column "area" of K[]):

      /* Is "j" NOT same as "area" and does area (j+1)-->(area+1)?.. */
      if ( j!=area && K[NAREAS*j+area] )
      {
        /* Compute area (j+1)'s contrib. to TOT. input to (area+1)   */
	Correlate_2d_cyclic( &rates[N1*j], &J[ NSQR1*(NAREAS*j+area) ],
                                     N11, N12, NFFB1, NFFB2, tempffb );

        /* Add this contribution to the TOTAL EPSP to current area   */
        for (i=0; i<N1; i++)
          linkffb[i] += tempffb[i];

	Clear_Vector (N1, tempffb); // Reset the temp. vector of results
      }

    /* ************************************************************* */
    /* ************** RECurrent (within area) input  *************** */

    /* Calculate linkrec[i] (total pre-synaptic pot. converging from */
    /* within-area cells to cell i) for all cells of area "area+1".  */

    if ( K[ (NAREAS+1) * area ] )   // Does area have REC links?..

      Correlate_2d_cyclic( &rates[N1*area], &J[ NSQR1*(NAREAS+1)*area ],
                                      N11, N12, NREC1, NREC2, linkrec );

    /* ************************************************************* */
    /* ************* INHibitory (within area) input  *************** */

    /* Calculate linkinh[i] (tot. activity from excitat. cells which */
    /* is being projected to each underlying inhibitory cell "i")    */

    Correlate_2d_Uni_cyclic( &rates[N1*area], Jinh,
                             N11, N12, NINH1, NINH2, linkinh );

    /* ************************************************************* */
    /* *****************     LEAKY INTEGRATIONS     **************** */

    /* *****************      Inhibitory cells      **************** */
    /* The total output from excit. cells (linkinh[i]) is now inte-  */
    /* grated (ie, weight=1) into inhib. cell "i"'s membr. potential */

    for(i=0; i<N1; i++)
      leaky_integrate( TAU2, pinh[i], linkinh[i] );

    /* ********  Slow/global inhibition/activity control  ********** */

    leaky_integrate(TAUSLOW, slowinh[area], Sum(N1,&rates[N1*area]));

    /* ****************** Excitatory cells  ************************ */

    for(i=0; i<N1; i++)              // For all cells of current area

      leaky_integrate( TAU1, ppot[i],
                         .01*(   sI0
                               	+ clampSMIn[i]
			   	+ sJffb * linkffb[i]
			   	+ sJrec * linkrec[i]
				- sJinh * FUNCI( pinh[i])
                               	- sJslow * slowinh[area]
                               	- 1000 * pdil[i]
                               	+ snoise*noise_fac*(equal_noise() -.5)
			     )
		     );
  }

  /* *************************************************************** */
  /* ****************** COMPUTE FIRING RATES (OUTPUTS) ************* */

  for(area=0; area<NAREAS; area++)    // For ALL areas in the network
  {
    // Define some helpful pointers (mostly for speed)

    ppot = &pot[N1*area];
    prates = &rates[N1*area];
    padapt = &adapt[N1*area];

    total_output = 0.0;
    for(i=0; i<N1; i++)               // For ALL cells in current area
    {
      prates[i] = FUNC( gain*(ppot[i] - theta - padapt[i]) );
      total_output += prates[i];      // update total network output
    }
  }

  /* *************************************************************** */
  /* ********************  COMPUTE NEW ADAPTATION  ***************** */

  for (area=0; area<NAREAS; area++)
  {
    prates = &rates[N1*area];
    padapt = &adapt[N1*area];

    /* Cell's adaptation = low-pass filter of cell's output (f.rate) */
    for(i=0; i<N1; i++)
      leaky_integrate( TAUADAPT, padapt[i], ADAPTSTRENGTH*prates[i] );
  }

  /* *************************************************************** */
  /* ***************************  LEARNING  ************************ */

  if (slrate>0)   // Is learning ON?
  {
    Clear_Vector( NAREAS, tot_LTP );
    Clear_Vector( NAREAS, tot_LTD );

    for (i=0; i<NAREAS; i++) // For all DEST. areas (col. "i" of J[])
      for (j=0; j<NAREAS; j++) // For all ORIGIN areas (row "j" of J[])

	/* Is ORIGIN == DEST. & does area (j+1) have REC. links?...  */
        if (j==i && K[(NAREAS+1)*j])

	  /* Yes: train RECurrent kernel projections for this area   */
          train_projection_cyclic (
              &rates[N1*j],                // pre-syn. rates
              &pot[N1*i],                  // post-syn. pot.
              &J[NSQR1*(NAREAS+1)*j],      // all (j+1)-->(j+1) kernels
              N11, N12, NREC1, NREC2, hrate, &tot_LTP[i], &tot_LTD[i] );

        else                    // (Destin. area is NOT same as origin)
        if ( K[ NAREAS*j+i ] )  // Does area (j+1) proj. to (i+1)?..

          train_projection_cyclic (
	      &rates[N1*j],               // pre-syn. rates
              &pot[N1*i],                  // post-syn. pot.
              &J[NSQR1*(NAREAS*j+i)],      // all (j+1)-->(i+1) kernels
              N11, N12, NFFB1, NFFB2, hrate, &tot_LTP[i], &tot_LTD[i] );
  }

  /* *************************************************************** */
  /* ********** RECORD AVERAGE RESPONSES DURING TRAINING *********** */

  /* Are we currently averaging netw.'s response to a specific patt? */
  if ( (stps_2b_avgd>0) && (spatno>0) && (spatno<P+1) )
  {
    for (area=0; area<NAREAS; area++)       // For all areas of the net
    {
      /* Get addr. of 1st "cell" of pattern-specific averaging array */
      prates_avg = &avg_patts[ N1*(NAREAS*(spatno-1)+area)];

      prates = &rates[N1*area]; // point to f.rate of 1st cell of area
      for (i=0; i<N1; i++)      // For all cells of this area

        /* Integrate cell's current f. rate into its average f. rate */
        leaky_integrate( TAU_AVG_RATES, prates_avg[i], prates[i] );
    }
    stps_2b_avgd--;      // Averaging is done only for a limited time
  }

  /* *************************************************************** */
  /* *********** COMPUTE EMERGING CAs and their OVERLAPS *********** */

  if (sCA_ovlps)
  {
    compute_CApatts(CA_THRESH); // re-compute all CAs
    compute_CAoverlaps( );      // re-compute CA overlaps
    write_CApatts( ); 		// write CA-cells numbers to file
    SET_SWITCH(sCA_ovlps, FALSE);
  }

  /* *************************************************************** */
  /* ******** COMPUTE OVERLAP BETW. CAs and CURRENT ACTIV. ********* */

  for (i=0; i<P; i++)
    for (area=0; area<NAREAS; area++)
      ovlps[area*P+i]=bSkalar( N1, &rates[area*N1],
			           &ca_patts[N1*(NAREAS*i+area)] );


  /* *************************************************************** */
  /* ********************* AUTOMATED TESTING  ********************** */

  if (TESTING)  // Are we in "automated testing" mode ?
  {
    switch ( test_phase )
    {
      case 0: /* ***** PREPARE TESTING (EXECUTED ONLY ONCE) ******* */
      {
        char filename[50];                // Will contain file name

	/* Prepare to write data: open file for append (or write)   */
	sprintf(filename, DATA_WR);
	fi = fopen (filename, "a");
 	if (fi==0)                        // Has the file opened OK?
	{
	  printf("\n WARNING: Could not open file %s \n", filename);
	  test_phase = STOPTEST_PHASE;    // NO: force end of testing
 	}
	else
	{
	  /* At start of TESTING, write current CA threshold to file*/
	  fprintf (fi, " CA-threshold: %4.2f \n", CA_THRESH);

 	  /* For all CAs, compute and write no. of CA cells/area    */
 	  compute_CApatts( CA_THRESH);
	  for (j=0; j<P; j++)
	  {
	    fprintf (fi, "\n CA#%d:", j+1);
	    for (area=0; area<NAREAS; area++)
	      fprintf(fi," %d", bSum(N1, &ca_patts[N1*(NAREAS*j+area)]));
	  }
	  fprintf (fi, "\n\n\n");
	  stimRepet = 1;                  // Init. stim. rep. counter
	  stimCA = 1;                     // start by stimulating CA#1
	  SET_SLIDER( spatno, 0);         // NO input (not even noise)
	  test_phase++;                   // move to next phase
	}
      }
      break;

      case 1: /* **************** TESTING BEGINS ****************** */
        SET_SLIDER( sJslow, 60);          // set g. inhib. for TESTING
        SET_SLIDER( sI0, 20);             // Get slow inhib. to grow..
        test_phase++;
      break;

      case 2: /* **********  WAIT for HIGH GLOB. INHIB. *********** */
        if ( slowinh[GINHIB_TEST_AREA] > GINHIB_TESTING ) // High enough?
        {
  	  SET_SLIDER( sI0, 0);            // reset baseline input
	  test_phase++;                   // move to next phase
	}
      break;

      case 3: /* **********  WAIT for LOW GLOB. INHIB. ************ */
        if ( slowinh[GINHIB_TEST_AREA] < GINHIB_TESTING)  // Low enough?
        {
	  SET_SLIDER( spatno, stimCA);    // Set input pattern
          SET_SWITCH( sSInp, TRUE);       // Activate sensory input
          SET_SWITCH( sPrintTest, TRUE ); // Start writing data to file

	  /* Clear all activ. history for patt. currently presented */
          Clear_bVector(NAREAS*N1, &above_hstory[NAREAS*N1*(stimCA-1)]);
          last_stp = stp;                 // record current time-step
           test_phase++;                   // move to next phase
        }
      break;

      case 4: /* ******* WAIT for STIMULUS OFFSET TIME ************ */
        if (stp - last_stp > STIM_DURATION )
        {
          SET_SWITCH( sSInp, FALSE);      // Stop sensory stimulation
	  SET_SLIDER( spatno, 0);         // NO input (not even noise)
          last_stp = stp;
          test_phase++;
        }
      break;

      case 5: /* ******* WAIT for END OF RECORDING TIME *********** */
        if (stp - last_stp > PRINTSTEPS ) // Recorded enough steps?..
        {
          SET_SWITCH( sPrintTest, FALSE); // YES: stop writing to file
	  resetNet();                     // Reset network activity
	  fprintf (fi, "\n\n");           // mark end of "ERP" recording
	  test_phase = STARTTEST_PHASE;   // Back to start (by default)
	  stimCA++;                       // Move on to stim. next CA

	  if (stimCA > P)                 // Stimulated ALL CAs?..
	  {                               // YES: end of this stim. series
	    fprintf (fi, "END TRIAL #%d \n\n", stimRepet);
            stimRepet++;

	    if (stimRepet > TOT_REPET)    // Any more stim. repetitions?
	    {
	      fclose(fi);                 // NO: Close the file
	      test_phase = STOPTEST_PHASE;// Stop TESTING
	    }
	    else
	      stimCA = 1;                 // Start again with CA#1
	  }
        }
      break;

      default: /* *************** END OF TESTING ****************** */
        printf( "\n END \n");
        exit(0);

    } // END-Switch

  } // END-If

  /* ************************************************************** */
  /* ***************** ASCII DATA FILE WRITING ******************** */

  if (sPrintTest)
  {
    /* ************************************************************ */
    /* For each CA, find out how many CA cells are CURRENTLY (NOT   */
    /* on average) firing above "CA_THRESH" value. For the CA which */
    /* is being stimulated, cells that reach thresh. are "tracked"  */
    /* OVER different steps (& trials) so as to compute the cumul.  */
    /* no. of CA cells that were EVER re-activated by sensory stim. */

     for (j=0; j<P; j++)                  // for each CA (pattern)
     {
       fprintf (fi, " CA#%d: ", j+1);
       Clear_bVector( N1*NAREAS, above_thresh);

       for (area=0; area<NAREAS; area++)  // for each area
       {
	     float max_act;

         prates = &rates[N1*area];        // pointer 2 current f.rates
         pabove = &above_thresh[N1*area]; // pointer to bVec 2 b filled

         /* Get pointer to avg. firing rates for current CA & area   */
         prates_avg = &avg_patts[N1*(NAREAS*j+area)];

         /* Get max. active CA cell there & threshold its activ. val.*/
         max_act = Max_Elem(N1, prates_avg) * CA_THRESH;

         /* Fill in bVec. "above_thresh" with cells active > thresh. */
         Fire( N1, prates, max_act, pabove);

         /* We don't want to count cells that don't belong to CA #j  */
         for (i=0; i<N1; i++)
         {
           if (prates_avg[i] < max_act)   // Does cell belong to CA #j?

             /* NO: make sure it's not set to "1" in "above_thresh"  */
             pabove[i] = 0;

           else
	   {
 	     /* YES, it does belong to CA#j: leave "pabove[]" as is..*/

             /* .. AND if "j" is the CA currently being stimulated,  */
	     /* record whether this CA cell was (ever) re-actived.   */
	     if (j == (stimCA-1) && pabove[i] )      // Cell is active:
               above_hstory[N1*(NAREAS*j+area)+i]=1; // keep track of it
           }
         }

         /* Print no. of CA cells *CURRENTLY* firing above threshold */
         fprintf(fi, " %d", bSum(N1, pabove) );
       }
     }

     /* ONLY for the CA which is currently being stimulated, write   */
     /* tot. no. of CA cells that were (at some point) reactivated.  */

     fprintf (fi, " Tot. # reactivated cells for CA%d so far:", stimCA);
     for (area=0; area<NAREAS; area++)
       fprintf (fi," %d", bSum(N1,&above_hstory[N1*(NAREAS*(stimCA-1)+area)]) );

     fprintf(fi, " \n"); // Data for next time-step will be on a new line
  }

  stp++;
}