# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 20:48:02  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 55, Attempt 1 — **converged**
- Total time: 17.9000  |  Increment size: 0.00451
- Converged increments so far: 70

## Errors & Warnings
- None recorded yet.

## Run Configuration (fixes applied this run)
| Parameter | Previous | Current |
|-----------|----------|---------|
| Min increment | 0.02 mm | 0.001 mm |
| Initial increment | 0.5 mm | 0.1 mm |
| Contact STABILIZE | 0.0002 | 0.001 |
| Contact type | LINEAR (50 N/mm³) | EXPONENTIAL (c0=0.1mm, p0=0) |
| Threads | 4 | 4 |

**Root cause of previous failure:** Contact penetration oscillation at coil-binding transition in Step 2 (node 77533, SPRING_SURF self-contact). LINEAR penalty caused abrupt contact stiffness changes driving displacement corrections beyond increment tolerance (16 iterations, no convergence). Fix: EXPONENTIAL pressure-overclosure (c0=0.1mm) provides smooth continuous contact stiffness, avoiding the chattering that caused the minimum increment violation.

## Raw .sta tail
```
1     2   1     5     1     6  1.00       1.00       0.5000    
   1     3   1     6     0     6  1.50       1.50       0.5000    
   1     4   1     4     2     6  2.00       2.00       0.5000    
   1     5   1     4     2     6  2.50       2.50       0.5000    
   1     6   1     2     4     6  3.00       3.00       0.5000    
   1     7   1     2     4     6  3.50       3.50       0.5000    
   1     8   1     3     3     6  4.00       4.00       0.5000    
   1     9   1     4     2     6  4.50       4.50       0.5000    
   1    10   1     1     5     6  5.00       5.00       0.5000    
   1    11   1     2     4     6  5.50       5.50       0.5000    
   1    12   1     4     2     6  6.00       6.00       0.5000    
   1    13   1     5     1     6  6.50       6.50       0.5000    
   1    14   1     4     2     6  7.00       7.00       0.5000    
   1    15   1     5     1     6  7.50       7.50       0.5000    
   1    16   1     5     1     6  7.90       7.90       0.4000    
   2     1   1     3     3     6  8.40       0.500      0.5000    
   2     2   1     2     4     6  8.90       1.00       0.5000    
   2     3   1     3     3     6  9.40       1.50       0.5000    
   2     4   1     3     3     6  9.90       2.00       0.5000    
   2     5   1     6     0     6  10.4       2.50       0.5000    
   2     6   1     4     2     6  10.9       3.00       0.5000    
   2     7   1     6     0     6  11.4       3.50       0.5000    
   2     8   1     6     3     9  11.9       4.00       0.5000    
   2     9   1     6     3     9  12.4       4.50       0.5000    
   2    10   1     6     0     6  12.9       5.00       0.5000    
   2    11   1     6     0     6  13.4       5.50       0.5000    
   2    12   1     6     3     9  13.9       6.00       0.5000    
   2    13   1     6     3     9  14.4       6.50       0.5000    
   2    14   1U    5     0     5  14.4       6.50       0.5000    
   2    14   2     5     4     9  14.5       6.62       0.1250    
   2    15   1     5     4     9  14.7       6.81       0.1875    
   2    16   1     6     3     9  15.0       7.09       0.2812    
   2    17   1     6     3     9  15.4       7.52       0.4219    
   2    18   1     7     8    15  15.9       8.02       0.5000    
   2    19   1     7     5    12  16.4       8.52       0.5000    
   2    20   1    12     0    12  16.9       9.02       0.5000    
   2    21   1U   41     0    41  16.9       9.02       0.5000    
   2    21   2    11     1    12  17.0       9.14       0.1250    
   2    22   1U    8     0     8  17.0       9.14       0.1875    
   2    22   2     6     2     8  17.1       9.19       0.04688   
   2    23   1     9     2    11  17.2       9.26       0.07031   
   2    24   1     9     3    12  17.2       9.33       0.07031   
   2    25   1    16     0    16  17.3       9.43       0.1055    
   2    26   1U   23     0    23  17.3       9.43       0.1582    
   2    26   2     8     2    10  17.4       9.47       0.03955   
   2    27   1    12     1    13  17.4       9.53       0.05933   
   2    28   1    35     0    35  17.5       9.62       0.08899   
   2    29   1U   12     0    12  17.5       9.62       0.06674   
   2    29   2     9     0     9  17.5       9.64       0.01669   
   2    30   1     6     3     9  17.6       9.65       0.01669   
   2    31   1    11     1    12  17.6       9.68       0.02503   
   2    32   1    22     1    23  17.6       9.72       0.03754   
   2    33   1    13     0    13  17.6       9.75       0.02816   
   2    34   1    13     0    13  17.7       9.77       0.02816   
   2    35   1U   17     0    17  17.7       9.77       0.04224   
   2    35   2     6     4    10  17.7       9.78       0.01056   
   2    36   1     5     3     8  17.7       9.79       0.007919  
   2    37   1     5     4     9  17.7       9.80       0.007919  
   2    38   1     9     1    10  17.7       9.81       0.01188   
   2    39   1     5     4     9  17.7       9.82       0.008909  
   2    40   1     6     3     9  17.7       9.83       0.008909  
   2    41   1     9     2    11  17.7       9.84       0.01336   
   2    42   1    12     0    12  17.8       9.86       0.02005   
   2    43   1    11     0    11  17.8       9.89       0.03007   
   2    44   1    16     0    16  17.8       9.92       0.03007   
   2    45   1U    8     0     8  17.8       9.92       0.04510   
   2    45   2    10     0    10  17.8       9.93       0.01128   
   2    46   1    10     0    10  17.8       9.95       0.01128   
   2    47   1    10     0    10  17.9       9.96       0.01691   
   2    48   1U   19     0    19  17.9       9.96       0.02537   
   2    48   2    11     0    11  17.9       9.97       0.006342  
   2    49   1    10     0    10  17.9       9.98       0.006342  
   2    50   1U    8     0     8  17.9       9.98       0.009514  
   2    50   2     4     3     7  17.9       9.98       0.002378  
   2    51   1     6     1     7  17.9       9.98       0.003568  
   2    52   1     8     0     8  17.9       9.99       0.005351  
   2    53   1U    7     0     7  17.9       9.99       0.008027  
   2    53   2     4     4     8  17.9       9.99       0.002007  
   2    54   1     3     4     7  17.9       9.99       0.003010  
   2    55   1     8     3    11  17.9       10.0       0.004515
```

## Recent .msg output
```
MAX. CONTACT FORCE ERROR 1.72955E-03 AT NODE 140748 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       6.49       TIME AVG. FORCE        5.22    
 LARGEST SCALED RESIDUAL FORCE      2.890E-03   AT NODE      84044   DOF  3
  CORRESPONDING RESIDUAL FORCE      2.890E-03
 LARGEST INCREMENT OF DISP.         2.014E-02   AT NODE       1280   DOF  2
 LARGEST CORRECTION TO DISP.        1.608E-04   AT NODE       6970   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.855e+12
        SOLVER ELAPSED TIME:  155s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1

   MAX. PENETRATION ERROR 553.818E-06   AT NODE 141569 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 1.58358E-03 AT NODE 140748 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       6.49       TIME AVG. FORCE        5.22    
 LARGEST SCALED RESIDUAL FORCE      2.587E-03   AT NODE      84044   DOF  3
  CORRESPONDING RESIDUAL FORCE      2.587E-03
 LARGEST INCREMENT OF DISP.         2.003E-02   AT NODE       1280   DOF  2
 LARGEST CORRECTION TO DISP.        1.423E-04   AT NODE       6970   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.779e+12
        SOLVER ELAPSED TIME:  154s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     2

   MAX. PENETRATION ERROR -4.85652E-03 AT NODE 101530 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -12.1918E-03  AT NODE 94892 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       6.49       TIME AVG. FORCE        5.22    
 LARGEST SCALED RESIDUAL FORCE      9.782E-02   AT NODE     131598   DOF  3
  CORRESPONDING RESIDUAL FORCE      9.782E-02
 LARGEST INCREMENT OF DISP.         1.993E-02   AT NODE       1280   DOF  2
 LARGEST CORRECTION TO DISP.        1.262E-04   AT NODE       6970   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.780e+12
        SOLVER ELAPSED TIME:  153s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     8

   MAX. PENETRATION ERROR 211.289E-06   AT NODE 141569 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -1.15126E-03 AT NODE 5730 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       6.49       TIME AVG. FORCE        5.22    
 LARGEST SCALED RESIDUAL FORCE      2.087E-03   AT NODE      84044   DOF  3
  CORRESPONDING RESIDUAL FORCE      2.087E-03
 LARGEST INCREMENT OF DISP.         1.984E-02   AT NODE       1280   DOF  2
 LARGEST CORRECTION TO DISP.        1.086E-04   AT NODE       6970   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.780e+12
        SOLVER ELAPSED TIME:  153s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     3

   MAX. PENETRATION ERROR 63.0739E-06  AT NODE 141569 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -1.03363E-03 AT NODE 5730 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINTS HAVE CONVERGED.

 AVERAGE FORCE                       6.49       TIME AVG. FORCE        5.22    
 LARGEST SCALED RESIDUAL FORCE      1.859E-03   AT NODE      84044   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.859E-03
 LARGEST INCREMENT OF DISP.         1.976E-02   AT NODE       1280   DOF  2
 LARGEST CORRECTION TO DISP.        9.584E-05   AT NODE       6970   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

          BECAUSE OF INCONSISTENT CONVERGENCE
          THE NEXT TIME INCREMENT WILL BE REDUCED TO    3.386E-03

 ITERATION SUMMARY FOR THE INCREMENT:  11 TOTAL ITERATIONS, OF WHICH
   8 ARE SEVERE DISCONTINUITY ITERATIONS AND  3 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  4.5152607E-03,  FRACTION OF STEP COMPLETED  0.9996331    
 STEP TIME COMPLETED        9.996331    ,  TOTAL TIME COMPLETED         17.89633    


  INCREMENT    56 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  3.386E-03
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.161e+12
        SOLVER ELAPSED TIME:  160s
```
