# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 02:26:08  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 32, Attempt 1 — **converged**
- Total time: 17.9000  |  Increment size: 0.00260
- Converged increments so far: 51

## Errors & Warnings
- None recorded yet.

## Run Configuration (fixes applied this run)
| Parameter | Previous | Current |
|-----------|----------|---------|
| Min increment | 0.02 mm | 0.001 mm |
| Initial increment | 0.5 mm | 0.1 mm |
| Contact STABILIZE | 0.0002 | 0.001 |
| Contact type | HARD | HARD |
| Threads | 4 | 4 |

**Root cause of previous failure:** Contact penetration oscillation at coil-binding transition drove increment below minimum (0.02 mm). Nodes 143372 / 27501 showed repeated penetration errors. Fix: 20× finer min increment + 5× higher contact stabilization damping.

## Raw .sta tail
```
Abaqus/Standard 2025.HF3                  DATE 12-Jun-2026 TIME 22:03:04
 SUMMARY OF JOB INFORMATION:
 STEP  INC ATT SEVERE EQUIL TOTAL  TOTAL      STEP       INC OF       DOF    IF
               DISCON ITERS ITERS  TIME/    TIME/LPF    TIME/LPF    MONITOR RIKS
               ITERS               FREQ
   1     1   1     1     1     2  0.100      0.100      0.1000    
   1     2   1     1     1     2  0.200      0.200      0.1000    
   1     3   1     1     1     2  0.350      0.350      0.1500    
   1     4   1     1     1     2  0.575      0.575      0.2250    
   1     5   1     2     1     3  0.913      0.913      0.3375    
   1     6   1     3     0     3  1.41       1.41       0.5000    
   1     7   1     4     0     4  1.91       1.91       0.5000    
   1     8   1     3     0     3  2.41       2.41       0.5000    
   1     9   1     3     0     3  2.91       2.91       0.5000    
   1    10   1     2     0     2  3.41       3.41       0.5000    
   1    11   1     2     0     2  3.91       3.91       0.5000    
   1    12   1     2     0     2  4.41       4.41       0.5000    
   1    13   1     2     0     2  4.91       4.91       0.5000    
   1    14   1     2     0     2  5.41       5.41       0.5000    
   1    15   1     3     0     3  5.91       5.91       0.5000    
   1    16   1     3     0     3  6.41       6.41       0.5000    
   1    17   1     3     0     3  6.91       6.91       0.5000    
   1    18   1     3     0     3  7.41       7.41       0.5000    
   1    19   1     3     0     3  7.90       7.90       0.4875    
   2     1   1     2     0     2  8.00       0.100      0.1000    
   2     2   1     1     1     2  8.10       0.200      0.1000    
   2     3   1     2     0     2  8.25       0.350      0.1500    
   2     4   1     2     0     2  8.47       0.575      0.2250    
   2     5   1     2     0     2  8.81       0.913      0.3375    
   2     6   1     2     0     2  9.31       1.41       0.5000    
   2     7   1     2     0     2  9.81       1.91       0.5000    
   2     8   1     3     0     3  10.3       2.41       0.5000    
   2     9   1     2     0     2  10.8       2.91       0.5000    
   2    10   1     3     0     3  11.3       3.41       0.5000    
   2    11   1     4     0     4  11.8       3.91       0.5000    
   2    12   1     3     0     3  12.3       4.41       0.5000    
   2    13   1     3     0     3  12.8       4.91       0.5000    
   2    14   1     4     0     4  13.3       5.41       0.5000    
   2    15   1     3     0     3  13.8       5.91       0.5000    
   2    16   1     4     0     4  14.3       6.41       0.5000    
   2    17   1     3     0     3  14.8       6.91       0.5000    
   2    18   1     4     0     4  15.3       7.41       0.5000    
   2    19   1     3     0     3  15.8       7.91       0.5000    
   2    20   1     5     0     5  16.3       8.41       0.5000    
   2    21   1     5     0     5  16.8       8.91       0.5000    
   2    22   1     5     0     5  17.3       9.41       0.5000    
   2    23   1    19     0    19  17.8       9.91       0.5000    
   2    24   1U   27     0    27  17.8       9.91       0.08750   
   2    24   2    11     0    11  17.8       9.93       0.02188   
   2    25   1     9     1    10  17.9       9.96       0.02188   
   2    26   1U   13     0    13  17.9       9.96       0.03281   
   2    26   2    10     0    10  17.9       9.96       0.008203  
   2    27   1     3     4     7  17.9       9.97       0.006152  
   2    28   1     5     0     5  17.9       9.98       0.006152  
   2    29   1     5     1     6  17.9       9.99       0.009229  
   2    30   1U   10     0    10  17.9       9.99       0.01384   
   2    30   2     7     1     8  17.9       9.99       0.003461  
   2    31   1     5     1     6  17.9       9.99       0.002596  
   2    32   1     5     2     7  17.9       9.99       0.002596
```

## Recent .msg output
```
(SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -512.752E-06   AT NODE 79663 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.88       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE      4.162E-03   AT NODE     139987   DOF  3
  CORRESPONDING RESIDUAL FORCE      4.162E-03
 LARGEST INCREMENT OF DISP.        -6.202E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        3.133E-04   AT NODE      11207   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.724e+12
        SOLVER ELAPSED TIME:  41s

                    3 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM OPEN TO CLOSED
                    2 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     4

   MAX. PENETRATION ERROR 110.018E-06   AT NODE 138805 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -287.472E-06   AT NODE 79663 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.88       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE      2.510E-03   AT NODE      63325   DOF  3
  CORRESPONDING RESIDUAL FORCE      2.510E-03
 LARGEST INCREMENT OF DISP.        -6.150E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        1.965E-04   AT NODE      12091   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.725e+12
        SOLVER ELAPSED TIME:  45s

                    2 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM OPEN TO CLOSED
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     5

   MAX. PENETRATION ERROR 70.1321E-06  AT NODE 34338 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -174.209E-06   AT NODE 79663 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.88       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE      1.459E-03   AT NODE      63325   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.459E-03
 LARGEST INCREMENT OF DISP.        -6.115E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        1.332E-04   AT NODE      13322   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.724e+12
        SOLVER ELAPSED TIME:  46s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1

   MAX. PENETRATION ERROR -502.420E-06   AT NODE 5457 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -303.261E-06   AT NODE 5457 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.88       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE      1.584E-02   AT NODE     121782   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.584E-02
 LARGEST INCREMENT OF DISP.        -6.094E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        8.829E-05   AT NODE      13322   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.724e+12
        SOLVER ELAPSED TIME:  43s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     2

   MAX. PENETRATION ERROR 25.4054E-06  AT NODE 138805 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -65.4224E-06  AT NODE 158938 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINTS HAVE CONVERGED.

 AVERAGE FORCE                       4.88       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE      5.442E-04   AT NODE      63325   DOF  3
  CORRESPONDING RESIDUAL FORCE      5.442E-04
 LARGEST INCREMENT OF DISP.        -6.073E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        6.454E-05   AT NODE       9745   DOF  1
 ESTIMATE OF DISP.    CORRECTION    2.407E-05
          FORCE     EQUILIB. ACCEPTED BASED ON SMALL RESIDUAL AND ESTIMATED CORRECTION

          BECAUSE OF INCONSISTENT CONVERGENCE
          THE NEXT TIME INCREMENT WILL BE REDUCED TO    1.947E-03

 ITERATION SUMMARY FOR THE INCREMENT:   7 TOTAL ITERATIONS, OF WHICH
   5 ARE SEVERE DISCONTINUITY ITERATIONS AND  2 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  2.5955200E-03,  FRACTION OF STEP COMPLETED  0.9994638    
 STEP TIME COMPLETED        9.994638    ,  TOTAL TIME COMPLETED         17.89464    


  INCREMENT    33 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  1.947E-03
```
