/*
** gen_sim.h 
*/

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

#ifndef GEN_SIM_H
#define GEN_SIM_H

#include "gen_obj.h"


// Some MACROs that should make programming it easier to write 
// programs that can be compiled serially and parallel
// To use OMP_FOR preFelix has to be run 

# ifdef WITH_OMP
# define OMP_THREADS(_n) omp_set_num_threads(_n);
# define OMP_FOR(_x) ... // this shouldn't occur because preFelix removes OMP_FORs
# define OMP_ONLY(_x) _x
# else
# define OMP_THREADS(_n) 
# define OMP_FOR(_x) for(_x)
# define OMP_ONLY(_x)
# endif


# ifdef WITH_MPI
# define RANK(_x) if(myrank==(_x))
# define COND(_x) if(_x)
# define MPI_ONLY(_x) _x
# else
# define RANK(_x) // if(myrank==(_x))
# define COND(_x) // if(_x)
# define CONNECT(_x1,_x2,_x3,_x4,_x5,_x6)
# define MPI_ONLY(_x) 
# endif

# define NO_FMPI_CONNECTIONS void fmpi_connections(){}


/*
** external functions and variables
*/

extern int myrank;


// EXTERN_FUNCTION ( int main, ( int, char**) );


EXTERN_FUNCTION ( int felix_main, (int , char**) );

EXTERN_FUNCTION ( void init_gen_sim, ( void ) );

EXTERN_FUNCTION ( int main_init, ( void) );
EXTERN_FUNCTION ( int init, (void));
EXTERN_FUNCTION ( int step, (void));

EXTERN_FUNCTION (float get_value, (long, int, int, int, int, int));

EXTERN_FUNCTION (void get_image, (long, int, int, int, int,
                      float, float, char *));
 
EXTERN_FUNCTION (void get_vector, (long, int, int, int, int, int,
                   float, float, char *)); 

EXTERN_FUNCTION (long get_function, (long, int, int, int, int, int, int)); 

EXTERN_FUNCTION (float get_function_value, (long, int, int));


EXTERN_FUNCTION (void get_grey_scale_imagearray, (ImageArray *, int, char*) );

EXTERN_FUNCTION (float get_imagearray_value, (ImageArray *, int, int) );


/* 
EXTERN_FUNCTION ( void Refresh_Function, (Function *) );

EXTERN_FUNCTION (void pack_bit_image_x, (long, short));
EXTERN_FUNCTION (void pack_bit_image_y, (long, short));

*/

# endif /* GEN_SIM_H */
