/* gen_sim.c */

/*
    Copyright (C) 1992/2007  Thomas Wennekers

    This program is part of the simulation tool Felix

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
# include <errno.h>



# include <sys/types.h>
# include <unistd.h>
# include <fcntl.h>
# include <sys/socket.h>
# include <sys/ioctl.h>
# include <netinet/in.h>
# include <arpa/inet.h>
# include <time.h>
# include <math.h>



#include "gen_sim.h"
#ifndef NO_GRAPHICS
  #include "sim_graph.h"
#endif
#include "output.h"



# include "mylan.h"

# define BASENAME "localhost"





#ifdef WITH_MPI 
//#include "fmpi.h"
 // we make these extern because we don't want to include the global mpi.h but compile with gcc
extern void fmpi_connections();
extern void fmpi_init(int argc, char**argv);
extern void fmpi_communicate();
#endif
extern int rank;

int myrank = -1; // if compiled without MPI "rank" wouldn't be defined



#ifdef TIMING
# include <time.h>
# include <sys/time.h>
static struct timeval tv1, tv2;
static struct timezone tz;
#endif 


#ifdef NO_GRAPHICS
int current_step=0;
#endif 

int running=0, do_steps=0, init_flag=0;  // init and run by default // ???? correct?
int timer_secs=0, timer_usecs=400000;    // at max speed 



// TODO 




# define DBUG(x)  x

# define N 512





/*********************/


int handle_steps( int bytes, char *buffer )
{
  long n;
  errno=0;
  n = strtol((char*)&buffer[1], NULL, 10);
  printf("%d %d\n", errno, n );
  if ((errno == ERANGE)
//   if ((errno == ERANGE && (n == LONG_MAX || n == LONG_MIN))
      || ( (errno != 0) && (n == 0)) ) // errno is NOT set for nonsense input??
  {
    perror("strtol");
    n=0;
 //   exit(0);
  }
  if (n<0)
  {
    fprintf(stderr, "negative step number -- IGNORED\n");
    n = 0;
  }
  return n;
}


int handle_set_switch( int bytes, char *buffer )
{
  int n=0, v=0;

  if (sscanf(&buffer[1], "%d %d", &n, &v) != 2)
    return 0;  // ignore
 
  if ( (n<0 || n >= no_of_switches) )
    return 0;

  *switches[n].flag = v ? 1 : 0;

  printf("set switch %d %d\n", n, v);

  return 0;
}


int handle_set_slider( int bytes, char *buffer )
{
  int n=0, v=0;

  if (sscanf(&buffer[1], "%d %d", &n, &v) != 2)
    return 0;  // ignore
 
  if ( n<0 || n >= no_of_sliders )
    return 0;

  *sliders[n].value = v; 

  printf("set slider %d %d\n", n, v);

  return 0;
}


int handle_toggle_output( int bytes, char *buffer )
{

  // no parameter ?  or various files ??

  int v=0;

  if (sscanf(&buffer[1], "%d", &v) != 1)
    return 0;  // ignore

  if (v) 
    SAVE_ON
  else
    SAVE_OFF

  printf("set save mode %d\n", v);

  return 0;
}


int handle_set_timer( int bytes, char *buffer )
{
  //  we don't have itimer / notifier 
  //  we could just set a sleep interval in the main loop
       //  because we dont have other events
       // sleep ... interrupted system call ???
     // not the same as timer as the time for the function adds ...
      // neglectable ??
  // looks like we need a thread ..
    // spawn thread that loops "timer" usecs
    //  set timer; threadsafe as read only 
     // gives us pings ... but do we do with them ??
        // condition variable ?

  float v=0;

  if (sscanf(&buffer[1], "%f", &v) != 1)
    return 0;  // ignore
 
  if ( v < 0. || v > 600. ) // 10 minutes 
    return 0;

  timer_secs = (int)floor(v);
  timer_usecs= (int)(1000000.*(v-timer_secs));

  stimer = timer_usecs; // ???????????????????????????????

  printf("%f %d %d\n", v, timer_secs, timer_usecs);

  return 0;
}


int handle_dump_sliders( int sock, int bytes, char*buffer )
{
  int i;
  char buf[256];

  for (i=0; i<no_of_switches; i++)
  {
    sprintf( buf, "%2d : %4d -- %s\n", i, *switches[i].flag, switches[i].name );
    write_buffer( sock, buf, strlen(buf) );
  }
  for (i=0; i<no_of_sliders; i++)
  {
    sprintf( buf, "%2d : %4d -- %s \n", i, *sliders[i].value, sliders[i].name );
    write_buffer( sock, buf, strlen(buf) );
  }
  return 0;
}



int handle_message( int sock, int bytes, char *buffer )
{
  switch( buffer[0] )
  {
    case '\r':
    case '\n': 
    case '1': // single step
      running  = 0;
      do_steps = 1;
      break;

    case 'n': // n steps 
      running = 0;
      do_steps=handle_steps( bytes, buffer );
      break;

    case 'b': // break
      running  = 0;
      do_steps = 0;
      break;

    case 'c': // continue
      running  = 1;
      do_steps = 0;
      break;

    case 'i': // init
      current_step = 0;
      init_flag = 1;
      break;

    case 'r': // run
      current_step = 0;
      init_flag    = 1;
      running = 1;
      break;

    case 'q': // quit
      exit(0);

    case 'B':  // set switch/button)
      handle_set_switch( bytes, buffer );
      break;

    case 'S':  // set slider
      handle_set_slider( bytes, buffer );
      break;

    case 'O':  // toggle output
      handle_toggle_output( bytes, buffer );
      break;

    case 'D':  // dump switches and sliders 
      handle_dump_sliders( sock, bytes, buffer );
      break;

    case 'T':  // set timer
      handle_set_timer( bytes, buffer );
      break;

    // ....

    default: // invalid command
     ;
  }
  return 0;
}




/**********************/













static void print_version()
{
  if (0)
  {
    printf("\n\n   This is felix version 1.0beta\n");
    printf("   developed by Thomas Wennekers\n");
    printf("   (http://www.pion.ac.uk/~thomas/felix.htm)\n\n");
 // printf("  (thomas.wennekers@plymouth.ac.uk\n\n");
 // printf("This distribution is for non-commercial use only.\n");
  }
}




void f_atexit(void) 
{
 // printf("We are exiting %d\n", myrank);
#ifdef WITH_MPI 
//  MPI_Finalize();  // causes bunches of errors; however, NOT to Finalize is 
                     // probably also not too good an idea
#endif
}




void init_gen_sim( )
{
  print_version();

DEBUG( 3, printf("main_init();\n"); )

  main_init();

#ifdef WITH_MPI
DEBUG( 3, printf("fmpi_connections();\n"); )

  fmpi_connections();
#endif 

DEBUG( 3, printf("MakeDisplay();\n"); )

  MakeDisplay();	/* build all xview objects */

DEBUG( 3, printf("MakeOutFiles()\n"); )

  MakeOutFiles();      /* Create Output File structures */
}


#ifdef NO_GRAPHICS

static void load_environment_data(char*filename)
{
  FILE *envfile=NULL;
  SimWindow *win;
  int x, y, show, i, j;
  int error = 0;
  char buf[100];

  DEBUG( 2, printf("ENTER load_environment_data: file = %s\n",filename); )

  if(envfile = fopen(filename, "r"))
  {

    /* scan main frame entry */
    if (fscanf(envfile, "MAINFRAME %d %d\n", &x, &y) != 2)
      error = 1;

    DEBUG( 3 , printf(" load_env: load switches\n"); )

    /* load Switches */ 
    for (i=0; i<no_of_switches; i++)
    {
      if( fgets( buf, 100, envfile )!=0 )
      {
        if (sscanf(buf, "SWITCH %d\n", &j) > 0)
          *switches[i].flag = j; 
        else
        {
          error = 1; 
          break; 
        }
      }
      else
      {
        error = 1; 
        break;
      }
    }
 
    DEBUG( 3 , printf(" load_env: load sliders\n"); )

    /* load Sliders */ 
    for (i=0; i<no_of_sliders; i++)
    {
      if( fgets( buf, 100, envfile )!=0 )
      {
        if (sscanf(buf, "SLIDER %d\n", &j) > 0)
          *sliders[i].value = j; 
        else
        {
          error = 1; 
          break; 
        }
      }
      else
      {
        error = 1; 
        break;
      }
    }

    if (error)
      fprintf(stderr, "Error loading environment.\n");

    if (fclose(envfile))
    {
       perror("Error closing environment file in load_environment_data");
    }
  }
  else 
  {
    fprintf(stderr, "No environment file %s\n", filename );
  }
}


int felix_main_o(int argc, char**argv)
{
  int i;
  char filename[250]; 

#ifdef WITH_MPI
#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

DEBUG( 3, printf("fmpi_init();\n"); )
  fmpi_init(argc, argv);
  myrank=rank;
#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: fmpi_init %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif


/* leads to errors when processes terminate; 
  // let see wheter we run into trouble if we don't call MPI_Finalize
  if( atexit(f_atexit) != 0)
    printf("error registering f_atexit()\n");
*/


#endif

#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

  init_gen_sim();

#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: init_gen_sim %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

DEBUG( 3, printf("load_environment_data()\n"); )
  
#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

  for (i=strlen(argv[0]); i>0; i-- )
    if (argv[0][i]=='/')
      break; 

  if (myrank!=-1) // each rank can have its own environment file
  {
    FILE*fi1;
    sprintf(filename, "%s/%s-%d", DEFAULT_ENV_DIRECTORY, &(argv[0][i]), myrank );
    if ( (fi1=fopen(filename,"r"))==NULL) // check the specific env file exists
      sprintf(filename, "%s/%s", DEFAULT_ENV_DIRECTORY, &(argv[0][i]) );
    else
      fclose(fi1);
  }
  else
    sprintf(filename, "%s/%s", DEFAULT_ENV_DIRECTORY, &(argv[0][i]) );

DEBUG( 3, printf("%s\n", filename ); )

  load_environment_data( filename );

#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: load_env %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

DEBUG( 3, printf("init\n"); )

#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

  init();

#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: init %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

DEBUG( 3, printf("SaveData()\n"); )

#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

  SAVE_ON  // default with GUI is off 
  SaveData(current_step);

#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: save0 %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

DEBUG( 3, printf("enter main loop\n"); )

  /* main loop */

  while(1)
  {

#ifdef TIMING
    gettimeofday( &tv1, &tz);
#endif

    step();

#ifdef TIMING
    gettimeofday( &tv2, &tz);
    DEBUG(0, printf("timing: step %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
    gettimeofday( &tv1, &tz);
#endif 

    SaveData(++current_step); 

#ifdef TIMING
    gettimeofday( &tv2, &tz);
    DEBUG(0, printf("timing: save %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

#ifdef WITH_MPI
DEBUG(3, printf("enter fmpi_communicate()\n"); )

#ifdef TIMING
    gettimeofday( &tv1, &tz);
#endif

    fmpi_communicate();

#ifdef TIMING  
    gettimeofday( &tv2, &tz);
    DEBUG(0, printf("timing: comm %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

DEBUG(3, printf("exit fmpi_communicate() \n");  )
#endif
  }

  // NEVER REACHED
  return 0;
}




/******************************/


simulator_init()
{

  DEBUG( 1, printf("init\n"); )

#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

  init();

#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: init %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

DEBUG( 3, printf("SaveData()\n"); )

#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

  SaveData(current_step);  // current_step should be zero ...

#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: save0 %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif
}



single_simulator_step()
{ 

  DEBUG( 1, printf("step %d\n", current_step); )


#ifdef TIMING
    gettimeofday( &tv1, &tz);
#endif

    step();

#ifdef TIMING
    gettimeofday( &tv2, &tz);
    DEBUG(0, printf("timing: step %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
    gettimeofday( &tv1, &tz);
#endif 

    SaveData(++current_step); 

#ifdef TIMING
    gettimeofday( &tv2, &tz);
    DEBUG(0, printf("timing: save %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

#ifdef WITH_MPI
DEBUG(3, printf("enter fmpi_communicate()\n"); )

#ifdef TIMING
    gettimeofday( &tv1, &tz);
#endif

    fmpi_communicate();

#ifdef TIMING  
    gettimeofday( &tv2, &tz);
    DEBUG(0, printf("timing: comm %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

DEBUG(3, printf("exit fmpi_communicate() \n");  )
#endif


  return 0;
}






int felix_main(int argc, char**argv)
{
  int i;
  char filename[250]; 

  int sock=-1, res;
  int port=12345;
  struct timeval tv;
  fd_set rfds;
  char buffer[N];
  int bytes;


  if (argc>2) // better check?
  {
    port = atoi(argv[2]);
    sock = connect_tcp_client( argv[1], port );
  }

  DEBUG( 1, printf("start main loop\n"); )



#ifdef WITH_MPI
#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

DEBUG( 3, printf("fmpi_init();\n"); )
  fmpi_init(argc, argv);
  myrank=rank;
#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: fmpi_init %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif


/* leads to errors when processes terminate; 
  // let see wheter we run into trouble if we don't call MPI_Finalize
  if( atexit(f_atexit) != 0)
    printf("error registering f_atexit()\n");
*/


#endif

#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

  init_gen_sim();

#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: init_gen_sim %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif

DEBUG( 3, printf("load_environment_data()\n"); )
  
#ifdef TIMING
  gettimeofday( &tv1, &tz);
#endif

  for (i=strlen(argv[0]); i>0; i-- )
    if (argv[0][i]=='/')
      break; 

  if (myrank!=-1) // each rank can have its own environment file
  {
    FILE*fi1;
    sprintf(filename, "%s/%s-%d", DEFAULT_ENV_DIRECTORY, &(argv[0][i]), myrank );
    if ( (fi1=fopen(filename,"r"))==NULL) // check the specific env file exists
      sprintf(filename, "%s/%s", DEFAULT_ENV_DIRECTORY, &(argv[0][i]) );
    else
      fclose(fi1);
  }
  else
    sprintf(filename, "%s/%s", DEFAULT_ENV_DIRECTORY, &(argv[0][i]) );

DEBUG( 3, printf("%s\n", filename ); )

  load_environment_data( filename );

#ifdef TIMING
  gettimeofday( &tv2, &tz);
  DEBUG(0, printf("timing: load_env %d %d\n", myrank, (tv2.tv_sec - tv1.tv_sec)*1000000 + tv2.tv_usec - tv1.tv_usec );fflush(stdout); )
#endif


DEBUG( 3, printf("enter main loop\n"); )

  /* main loop */

  if (sock>0)
  {

    SAVE_OFF   // init() should set it on

    while(1)
    {
      FD_ZERO(&rfds);
      FD_SET( sock, &rfds );
      tv.tv_sec  = timer_secs;
      tv.tv_usec = stimer;           // timer_usecs; // ???????????????????

      res = select( sock+1, &rfds, NULL, NULL, &tv);
      if (res == -1)
      {
        perror("select()");
          // error handling  ?????????????????
      }

      else if (res) // asynch event on sock

      {
        if ( ioctl( sock, FIONREAD, &bytes ) == -1 )
        {
          perror("error reading bytes on socket\n");
          // error handling  ?????????????????
        }

        // printf("bytes: %d\n", bytes );

        while (bytes)  // this is not really what we need ......
                       // could be more than 1 message ?
                       // could be larger than buffer ...??
        {
          if ( bytes > N )          // ?????????????????????????
            res = read_buffer( sock, buffer, N );
          else
            res = read_buffer( sock, buffer, bytes );

          handle_message( sock, res, buffer );

          bytes -= res;
        }
      }

      else  // we timed out .. next step 

      {
        if (init_flag)
        {
          simulator_init();
          init_flag=0;
        }
        else if ( do_steps > 0 )
        {
          single_simulator_step();
          do_steps--;
        }
        else if (running) // full speed
        {
          single_simulator_step(); 
        }
        else // we could be in a break with timer at 0
          usleep( 500000 );
      }
    }
  }

  else // no remote 

  {
    SAVE_ON
    simulator_init();
    while (1) 
      single_simulator_step(); 
  }

  // NEVER REACHED
  return 0;
}


/******************************/






#else  /* GRAPHICS VERSION */


int felix_main( int argc, char*argv[] )
{
  extern void simulator();

// Graphics version doesn't have MPI ...
//#ifdef WITH_MPI 
//DEBUG( 3, printf("enter fmpi_init();\n"); )
//  fmpi_init(argc, argv);
//#endif

  winargc = argc;
  winargv = argv;

  simulator();  // in sim_graph.c

  return 0;
}





/*
** get_value:
** get the value of a variable (uni or multi) at position x, y.
**
*/
float get_value( data, type, dimx, dimy, x, y)
long data;
int type, dimx, dimy, x, y;
{
  float ret = 0.0;

  if (type & POINTER)
    data = (long)(*(void**)data);

    switch(type & TYPE_BITS)
    {
      case ARRAY_BIT_TYPE:  /* PACKED with padding */

        ret = ( *( ((unsigned char *)data) + ((dimx+7)>>3)*y+(x>>3) )
                & bit_mask[ x&7 ] ) ? 1.0 : 0.0;
        break;

      case ARRAY_CHAR_TYPE:

        ret = *(((char *)data)+dimx*y+x);
         break;

      case ARRAY_INT_TYPE:

         ret = *(((int *)data)+dimx*y+x);
         break;

      case ARRAY_FLOAT_TYPE:

         ret = *(((float *)data)+dimx*y+x);
         break;

      case BIT_TYPE:

        ret = *(unsigned char *)data & bit_mask[7] ? 1.0 : 0.0 ;
        break;

      case CHAR_TYPE:

        ret = *(char *)data;
        break;

      case INT_TYPE:

        ret = *(int *)data;
        break;

      case FLOAT_TYPE:

        ret = *(float *)data;
        break;

      default:

        fprintf(stderr, "get_value warning: data type conflict\n");
        break;
    }


    return(ret);
}



/*
** get_vector:
*/
void get_vector( long data, int type, int dim, int pos, int skip, int bpp, float min, float max, char*buffer)
{
    float value;
    int i, xvcolor_index;
    float scale = (float) MAX_COLORS / (max - min);
    char black, white,bitmask;

    if (type & POINTER)
      data =  (long)(*(void**)data );

    switch(type & TYPE_BITS)
    {
      int * idata;
      float * fdata;

      case ARRAY_BIT_TYPE:  /* PACKED FORMAT : no padding in 2d-arrays !! */

      printf("ARRAY_BIT_TYPE NOT SUPPORTED !!! \n");

       buffer += pos>>3;
       bitmask = bit_mask[pos&7];
       skip = (skip+7)>>3;  /* bytes_per_line */

       for (i=0; i<dim; i++, buffer+=skip)
         if ( *((char*)data+(i>>3)) & bit_mask[i&7] )
           *buffer |= bitmask;
         else
           *buffer &= ~bitmask;


/*     if XImage is Bitmap :

       black = color_pixel_table[0];
       white = color_pixel_table[MAX_COLORS-1];

       for (i=0; i<dim; i++, buffer+=skip)
         *buffer =  *((char*)data+(i/8)) & bit_mask[i%8] ? black : white ;
*/

        break;


      case ARRAY_CHAR_TYPE:

        buffer += pos;
        for (i=0; i<dim; i++, buffer+=skip, data++)
        {
          value = *(char*)data;

          /* calculate color num */

          if (value <= min)
            xvcolor_index = 0;
          else if (value >= max)
            xvcolor_index = MAX_COLORS-1;
          else
	    xvcolor_index = (value - min)*scale;
          mybcopy( &color_pixel_table[xvcolor_index], buffer, bpp);
        }
        break;

      case ARRAY_INT_TYPE:

        buffer += pos;
        idata = (int *)data;
        for (i=0; i<dim; i++, buffer+=skip, idata++)
        {
          value = *idata;

          /* calculate color num */

          if (value <= min)
            xvcolor_index = 0;
          else if (value >= max)
            xvcolor_index = MAX_COLORS-1;
          else
	    xvcolor_index = (value - min)*scale;
          mybcopy( &color_pixel_table[xvcolor_index], buffer, bpp);
        }
        break;

      case ARRAY_FLOAT_TYPE:

        buffer += pos;
        fdata = (float *)data;
        for (i=0; i<dim; i++, buffer+=skip, fdata++)
        {
          value = *fdata;

          /* calculate color num */

          if (value <= min)
            xvcolor_index = 0;
          else if (value >= max)
            xvcolor_index = MAX_COLORS-1;
          else
	    xvcolor_index = (value - min)*scale;
          mybcopy( &color_pixel_table[xvcolor_index], buffer, bpp);
        }
        break;

      default:

        fprintf(stderr,
          "get_vector warning: data type conflict\n");
        break;
    }

} /* END get_vector */


/*
**  get_image
*/


void get_image(long data, int type, int dimx, int dimy, int bpp, float min, float max, char*buffer)
{
  float value;
  unsigned long *colors;
  float scale = (float) MAX_COLORS / (max - min);
  int i, xvcolor_index;

  DEBUG( 4, printf("get image : %x %x %d %d %d %f %f %x\n",
             data, type, dimx, dimy, bpp, min, max, buffer); )

  if (dimx <= 0 || dimy <= 0)
    fprintf(stderr,"WARNING:Dimensions <= 0 in get_image.");

  if (type & POINTER)
  {
    DEBUG( 4, printf("  POINTER type\n");)
    data =  (long)(*(void**)data );
  }

  switch( type & TYPE_BITS)
  {
    int * idata;
    float * fdata;


    case ARRAY_BIT_TYPE : /* PACKED FORMAT : padding at row-ends  */

      mybcopy( (char*)data, buffer, dimy*((dimx+7)>>3) );

      break;

    case ARRAY_CHAR_TYPE:

      for (i=0; i<dimx*dimy; i++, buffer+=bpp, data++)
      {
        xvcolor_index = 0;
        if ( (value = *(char*)data) > min)
        {
          if (value >= max)
            xvcolor_index = MAX_COLORS-1;
          else
    	    xvcolor_index = (value - min)*scale;
        }
        mybcopy ( &color_pixel_table[xvcolor_index], buffer, bpp);
      }
      break;

    case ARRAY_INT_TYPE:

      idata = (int *)data;
      for (i=0; i<dimx*dimy; i++, buffer+=bpp, idata++)
      {
        xvcolor_index = 0;
        if ( (value = *(int*)idata) > min)
        {
          if (value >= max)
            xvcolor_index = MAX_COLORS-1;
          else
            xvcolor_index = (value - min)*scale;
        }
        mybcopy ( &color_pixel_table[xvcolor_index], buffer, bpp);
      }
      break;

    case ARRAY_FLOAT_TYPE:

      fdata = (float *)data;
      for (i=0; i<dimx*dimy; i++, buffer+=bpp, fdata++)
      {
        xvcolor_index = 0;
        if ( (value = *(float*)fdata) > min)
        {
          if (value >= max)
            xvcolor_index = MAX_COLORS-1;
          else
	    xvcolor_index = (value - min)*scale;
        }
        mybcopy ( &color_pixel_table[xvcolor_index], buffer, bpp);
      }
      break;


/*  This code hangs up the OMPCC run time libs

    case ARRAY_FLOAT_TYPE:

      fdata = (float *)data;

#pragma omp parallel for default(shared)\
     private(xvcolor_index,i,buffer) \
     schedule(static)

      for (i=0; i<dimx*dimy; i++)
      {
        xvcolor_index = 0;
        if ( (value = fdata[i]) > min )
        {
          if (value >= max)
            xvcolor_index = MAX_COLORS-1;
          else
	    xvcolor_index = (value - min)*scale;
        }
        mybcopy ( &color_pixel_table[xvcolor_index],
                &buffer[i*bpp], bpp );
      }

      break;
*/

    default:

      fprintf(stderr,
        "WARNING: data type conflict in get_image\n");
      break;

  } /* END switch() */

}





/*
** get_function:
** get the pointer to data representing function at position x, y.
**
*/
long get_function(data, type, points, dimx, dimy, x, y)
long data;
int type, points, dimx, dimy, x, y;
{
  if (type & POINTER)
    data = (long)(*(void**)data);

    switch(type & TYPE_BITS)
    {
      case ARRAY_BIT_TYPE:  /* PACKED with padding */
      case BIT_TYPE:

        data = (long)( ((unsigned char *)data) + ((points+7)>>3)*(dimx*y+x));
        break;

      case ARRAY_CHAR_TYPE:
      case CHAR_TYPE:

         data = (long)(((char *)data)+points*(dimx*y+x));
         break;

      case ARRAY_INT_TYPE:
      case INT_TYPE:

         data = (long)(((int *)data)+points*(dimx*y+x));
         break;

      case ARRAY_FLOAT_TYPE:
      case FLOAT_TYPE:

         data = (long)(((float *)data)+points*(dimx*y+x));
         break;

      default:

        fprintf(stderr, "get_function warning: data type conflict\n");
        break;
    }

    return(data);
}


/*
** get_function_value:
**
*/
float get_function_value(data, type, index)
long data;
int type, index;
{
    float ret;

    /* POINTER TYPE possible ??????? */

    switch(type & TYPE_BITS)
    {
      case ARRAY_BIT_TYPE:  /* PACKED with padding */
      case BIT_TYPE:

        ret =  (   *(  (unsigned char *)data + ((index+7)>>3)  )
                & bit_mask[ index&7 ] ) ? 1.0 : 0.0;
        break;

      case ARRAY_CHAR_TYPE:
      case CHAR_TYPE:

         ret = (float)( *((char *)data+index) );
         break;

      case ARRAY_INT_TYPE:
      case INT_TYPE:

         ret = (float) *((int *)data+index);
         break;

      case ARRAY_FLOAT_TYPE:
      case FLOAT_TYPE:

         ret = *((float *)data+index);
         break;

      default:

        fprintf(stderr, "get_function warning: data type conflict\n");
        break;
    }

    return(ret);
}



/* void get_image(data, type, dimx, dimy, bpp, min, max, buffer) */


/*
** get_grey_scale_imagearray:  returns a 2d-subarray of an array of arrays
*/
void get_grey_scale_imagearray(mi, bpp, buffer)
ImageArray *mi;
int bpp;
char*buffer;
{
  long data, masksize, skip;

  DEBUG( 3, printf("get_grey_scale_imagearray\n");)

  if (mi->type & POINTER)
    data = (long)(*(void**)(mi->data));
  else
    data = mi->data;

  /* how many data points to be skipped ? */

  skip = mi->y*mi->dx + mi->x;

  DEBUG( 3, printf("skip: %d\n", skip);)

  switch(mi->type & TYPE_BITS)
  {
      case ARRAY_BIT_TYPE:  /* PACKED with padding */

        masksize = ((mi->dim_x+7)>>3)*mi->dim_y;
        data = (long)( (unsigned char *)data + masksize*skip );
        break;

    case ARRAY_CHAR_TYPE:

         masksize = mi->dim_x*mi->dim_y;
         data = (long)( (char *)data + masksize*skip );
         break;

      case ARRAY_INT_TYPE:

         masksize = mi->dim_x*mi->dim_y;
         data = (long)( (int *)data + masksize*skip );
         break;

      case ARRAY_FLOAT_TYPE:

         masksize = mi->dim_x*mi->dim_y;
         data = (long)( (float *)data + masksize*skip );
         break;

      default:

        fprintf(stderr, "get_grey_scale_imagearray warning: data type conflict\n");
        break;
    }

  /* switch POINTER flag OFF! POINTER TYPE data already de-referenced above */

  /* void get_image(data, type, dimx, dimy, bpp, min, max, buffer) */

  DEBUG( 4, printf("masksize %d\n", masksize);)

  (void) get_image( data , (mi->type) & ~POINTER, mi->dim_x, mi->dim_y, bpp,
                                                  mi->min, mi->max, buffer);
}


/*
** get_imagearray_value
** get float value of an element of the currently displayed
** array of an imagearray
*/


float get_imagearray_value(mi, x, y)
ImageArray *mi;
int x, y;
{
  long data, masksize, skip;
  float ret;

  if (mi->type & POINTER)
    data = (long)(*(void**)(mi->data));
  else
    data = mi->data;

  /* get the sub-array skip */

  skip = mi->y*mi->dx + mi->x;

  switch(mi->type & TYPE_BITS)
  {
      case ARRAY_BIT_TYPE:  /* PACKED with padding */

        masksize = ((mi->dim_x+7)>>3)*mi->dim_y;
        data = (long)( (unsigned char *)data + masksize*skip );
        break;

    case ARRAY_CHAR_TYPE:

         masksize = mi->dim_x*mi->dim_y;
         data = (long)( (char *)data + masksize*skip );
         break;

      case ARRAY_INT_TYPE:

         masksize = mi->dim_x*mi->dim_y;
         data = (long)( (int *)data + masksize*skip );
         break;

      case ARRAY_FLOAT_TYPE:

         masksize = mi->dim_x*mi->dim_y;
         data = (long)( (float *)data + masksize*skip );
         break;

      default:

        fprintf(stderr, "get_imagearray_value warning: data type conflict\n");
        break;
    }

  /* switch POINTER flag OFF! POINTER TYPE data already de-referenced above */

  ret = get_value( data, mi->type & ~POINTER, mi->dim_x, mi->dim_y, x, y);

  return ret;
}



#endif

