# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 21:58:25  
**Job status:** FAILED

## Current Progress (.sta)
- Step 2, Increment 26, Attempt 1 — **converged**
- Total time: 17.8000  |  Increment size: 0.02000
- Converged increments so far: 42
- Wall clock: 12613s (210.2 min)
- CPU time: 43800s

## Errors & Warnings
- ***ERROR: TIME INCREMENT REQUIRED IS LESS THAN THE MINIMUM SPECIFIED ***ERROR: THE ANALYSIS HAS BEEN TERMINATED DUE TO PREVIOUS ERRORS. ALL OUTPUT
- ***ERROR: THE ANALYSIS HAS BEEN TERMINATED DUE TO PREVIOUS ERRORS. ALL OUTPUT REQUESTS HAVE BEEN WRITTEN FOR THE LAST CONVERGED INCREMENT.

**Total errors: 2  |  Warnings: 0**

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
Abaqus/Standard 2025.HF3                  DATE 12-Jun-2026 TIME 18:27:05
 SUMMARY OF JOB INFORMATION:
 STEP  INC ATT SEVERE EQUIL TOTAL  TOTAL      STEP       INC OF       DOF    IF
               DISCON ITERS ITERS  TIME/    TIME/LPF    TIME/LPF    MONITOR RIKS
               ITERS               FREQ
   1     1   1     2     1     3  0.500      0.500      0.5000    
   1     2   1     3     1     4  1.00       1.00       0.5000    
   1     3   1     4     0     4  1.50       1.50       0.5000    
   1     4   1     3     0     3  2.00       2.00       0.5000    
   1     5   1     3     0     3  2.50       2.50       0.5000    
   1     6   1     2     1     3  3.00       3.00       0.5000    
   1     7   1     2     0     2  3.50       3.50       0.5000    
   1     8   1     2     0     2  4.00       4.00       0.5000    
   1     9   1     2     0     2  4.50       4.50       0.5000    
   1    10   1     2     0     2  5.00       5.00       0.5000    
   1    11   1     3     0     3  5.50       5.50       0.5000    
   1    12   1     3     0     3  6.00       6.00       0.5000    
   1    13   1     3     0     3  6.50       6.50       0.5000    
   1    14   1     3     0     3  7.00       7.00       0.5000    
   1    15   1     3     0     3  7.50       7.50       0.5000    
   1    16   1     3     0     3  7.90       7.90       0.4000    
   2     1   1     2     1     3  8.40       0.500      0.5000    
   2     2   1     3     0     3  8.90       1.00       0.5000    
   2     3   1     3     0     3  9.40       1.50       0.5000    
   2     4   1     3     0     3  9.90       2.00       0.5000    
   2     5   1     3     0     3  10.4       2.50       0.5000    
   2     6   1     3     0     3  10.9       3.00       0.5000    
   2     7   1     4     0     4  11.4       3.50       0.5000    
   2     8   1     3     0     3  11.9       4.00       0.5000    
   2     9   1     3     0     3  12.4       4.50       0.5000    
   2    10   1     4     0     4  12.9       5.00       0.5000    
   2    11   1     3     0     3  13.4       5.50       0.5000    
   2    12   1     3     0     3  13.9       6.00       0.5000    
   2    13   1     4     0     4  14.4       6.50       0.5000    
   2    14   1     3     0     3  14.9       7.00       0.5000    
   2    15   1     5     0     5  15.4       7.50       0.5000    
   2    16   1     4     0     4  15.9       8.00       0.5000    
   2    17   1     5     0     5  16.4       8.50       0.5000    
   2    18   1     6     0     6  16.9       9.00       0.5000    
   2    19   1    11     0    11  17.4       9.50       0.5000    
   2    20   1U    4     0     4  17.4       9.50       0.5000    
   2    20   2U    5     0     5  17.4       9.50       0.1250    
   2    20   3     6     0     6  17.4       9.53       0.03125   
   2    21   1     5     0     5  17.5       9.58       0.04688   
   2    22   1     5     0     5  17.5       9.65       0.07031   
   2    23   1     5     0     5  17.7       9.75       0.1055    
   2    24   1    11     0    11  17.8       9.91       0.1582    
   2    25   1U   17     0    17  17.8       9.91       0.08789   
   2    25   2    16     0    16  17.8       9.93       0.02197   
   2    26   1     0     0     0  17.8       9.93       0.02000   
                          
 THE ANALYSIS HAS NOT BEEN COMPLETED
```

## Recent .msg output
```
SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.943e+12
        SOLVER ELAPSED TIME:  43s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    14

   MAX. PENETRATION ERROR 398.958E-06   AT NODE 123961 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -716.397E-06   AT NODE 60718 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.85       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -6.445E-02   AT NODE        830   DOF  3
  CORRESPONDING RESIDUAL FORCE     -6.445E-02
 LARGEST INCREMENT OF DISP.        -2.745E-02   AT NODE      13635   DOF  1
 LARGEST CORRECTION TO DISP.       -2.887E-04   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.944e+12
        SOLVER ELAPSED TIME:  43s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    15

   MAX. PENETRATION ERROR 138.526E-06   AT NODE 77512 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 420.111E-06   AT NODE 77514 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.85       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -1.974E-03   AT NODE      76394   DOF  3
  CORRESPONDING RESIDUAL FORCE     -1.974E-03
 LARGEST INCREMENT OF DISP.        -2.761E-02   AT NODE      13635   DOF  1
 LARGEST CORRECTION TO DISP.       -2.473E-04   AT NODE       6741   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.944e+12
        SOLVER ELAPSED TIME:  43s

                    2 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM OPEN TO CLOSED
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    16

   MAX. PENETRATION ERROR 119.097E-06   AT NODE 77512 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 360.420E-06   AT NODE 77514 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.85       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -1.657E-03   AT NODE      76394   DOF  3
  CORRESPONDING RESIDUAL FORCE     -1.657E-03
 LARGEST INCREMENT OF DISP.        -2.774E-02   AT NODE      13635   DOF  1
 LARGEST CORRECTION TO DISP.       -2.079E-04   AT NODE       6741   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

          BECAUSE OF INCONSISTENT CONVERGENCE
          THE NEXT TIME INCREMENT WILL BE REDUCED TO    2.000E-02

 ITERATION SUMMARY FOR THE INCREMENT:  16 TOTAL ITERATIONS, OF WHICH
  16 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  2.197E-02,  FRACTION OF STEP COMPLETED  0.993    
 STEP TIME COMPLETED        9.93    ,  TOTAL TIME COMPLETED         17.8    


  INCREMENT    26 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  2.000E-02
 

 ***ERROR: TIME INCREMENT REQUIRED IS LESS THAN THE MINIMUM SPECIFIED

 ***ERROR: THE ANALYSIS HAS BEEN TERMINATED DUE TO PREVIOUS ERRORS. ALL OUTPUT 
           REQUESTS HAVE BEEN WRITTEN FOR THE LAST CONVERGED INCREMENT.



     ANALYSIS SUMMARY:
     TOTAL OF         42  INCREMENTS
                       3  CUTBACKS IN AUTOMATIC INCREMENTATION
                     196  ITERATIONS INCLUDING CONTACT ITERATIONS IF PRESENT
                     196  PASSES THROUGH THE EQUATION SOLVER OF WHICH 
                     196  INVOLVE MATRIX DECOMPOSITION, INCLUDING
                       0  DECOMPOSITION(S) OF THE MASS MATRIX
                       1  REORDERING OF EQUATIONS TO MINIMIZE WAVEFRONT
                       0  ADDITIONAL RESIDUAL EVALUATIONS FOR LINE SEARCHES
                       0  ADDITIONAL OPERATOR EVALUATIONS FOR LINE SEARCHES
                       4  WARNING MESSAGES DURING USER INPUT PROCESSING
                       0  WARNING MESSAGES DURING ANALYSIS
                       0  ANALYSIS WARNINGS ARE NUMERICAL PROBLEM MESSAGES
                       0  ANALYSIS WARNINGS ARE NEGATIVE EIGENVALUE MESSAGES
                       2  ERROR MESSAGES



     JOB TIME SUMMARY
       USER TIME (SEC)      =     4.18E+04
       SYSTEM TIME (SEC)    =     1.91E+03
       TOTAL CPU TIME (SEC) =     4.38E+04
       WALLCLOCK TIME (SEC) =        12613
       MEMORY PEAK (GB)     =            0
```
