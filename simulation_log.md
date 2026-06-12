# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 20:57:22  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 22, Attempt 1 — **converged**
- Total time: 17.5000  |  Increment size: 0.07031
- Converged increments so far: 38

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
```

## Recent .msg output
```
AVERAGE FORCE                       4.76       TIME AVG. FORCE        4.09    
 LARGEST SCALED RESIDUAL FORCE      0.709       AT NODE      77015   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.709    
 LARGEST INCREMENT OF DISP.        -7.057E-02   AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -7.343E-03   AT NODE      10056   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.833e+12
        SOLVER ELAPSED TIME:  42s

                   18 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    6 POINTS CHANGED FROM OPEN TO CLOSED
                   12 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR 5.82561E-03 AT NODE 111713 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 4.17154E-03 AT NODE 135587 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.76       TIME AVG. FORCE        4.09    
 LARGEST SCALED RESIDUAL FORCE      0.108       AT NODE      63308   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.108    
 LARGEST INCREMENT OF DISP.        -7.058E-02   AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.        2.736E-03   AT NODE      12000   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.893e+12
        SOLVER ELAPSED TIME:  42s

                   16 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   13 POINTS CHANGED FROM OPEN TO CLOSED
                    3 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 787.526E-06   AT NODE 136392 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 1.89393E-03 AT NODE 78463 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.76       TIME AVG. FORCE        4.09    
 LARGEST SCALED RESIDUAL FORCE     -4.164E-02   AT NODE     123916   DOF  3
  CORRESPONDING RESIDUAL FORCE     -4.164E-02
 LARGEST INCREMENT OF DISP.        -7.058E-02   AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.        1.377E-03   AT NODE       7074   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.554e+12
        SOLVER ELAPSED TIME:  46s

                   15 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    7 POINTS CHANGED FROM OPEN TO CLOSED
                    8 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     4

   MAX. PENETRATION ERROR 740.991E-06   AT NODE 142761 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 1.28706E-03 AT NODE 78463 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.76       TIME AVG. FORCE        4.09    
 LARGEST SCALED RESIDUAL FORCE      5.898E-03   AT NODE     139987   DOF  3
  CORRESPONDING RESIDUAL FORCE      5.898E-03
 LARGEST INCREMENT OF DISP.        -7.058E-02   AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.        8.836E-04   AT NODE      13323   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.841e+12
        SOLVER ELAPSED TIME:  42s

                   10 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    4 POINTS CHANGED FROM OPEN TO CLOSED
                    6 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     5

   MAX. PENETRATION ERROR 329.551E-06   AT NODE 161027 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 887.707E-06   AT NODE 78463 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.76       TIME AVG. FORCE        4.09    
 LARGEST SCALED RESIDUAL FORCE      3.250E-03   AT NODE     139987   DOF  3
  CORRESPONDING RESIDUAL FORCE      3.250E-03
 LARGEST INCREMENT OF DISP.        -7.058E-02   AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.        5.607E-04   AT NODE      13323   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   5 TOTAL ITERATIONS, OF WHICH
   5 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  7.031E-02,  FRACTION OF STEP COMPLETED  0.965    
 STEP TIME COMPLETED        9.65    ,  TOTAL TIME COMPLETED         17.5    


  INCREMENT    23 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.105
```
