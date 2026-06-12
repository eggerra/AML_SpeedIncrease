# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 19:46:19  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 15, Attempt 1 — **converged**
- Total time: 15.4000  |  Increment size: 0.50000
- Converged increments so far: 31

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
```

## Recent .msg output
```
LARGEST INCREMENT OF DISP.        -0.501       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -8.783E-02   AT NODE       2109   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.611e+12
        SOLVER ELAPSED TIME:  37s

                  347 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   82 POINTS CHANGED FROM OPEN TO CLOSED
                  265 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 492.269E-03   AT NODE 71358 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -119.680E-03   AT NODE 11270 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.62       TIME AVG. FORCE        3.82    
 LARGEST SCALED RESIDUAL FORCE      0.115       AT NODE      79019   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.115    
 LARGEST INCREMENT OF DISP.        -0.501       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -1.170E-02   AT NODE       2095   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.093e+12
        SOLVER ELAPSED TIME:  59s

                   35 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   11 POINTS CHANGED FROM OPEN TO CLOSED
                   24 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     4

   MAX. PENETRATION ERROR -770.898E-06   AT NODE 25194 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -8.44608E-03 AT NODE 11265 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.62       TIME AVG. FORCE        3.82    
 LARGEST SCALED RESIDUAL FORCE     -2.074E-02   AT NODE     140054   DOF  3
  CORRESPONDING RESIDUAL FORCE     -2.074E-02
 LARGEST INCREMENT OF DISP.        -0.501       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -1.531E-03   AT NODE       2090   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.106e+12
        SOLVER ELAPSED TIME:  140s

                    2 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    2 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     5

   MAX. PENETRATION ERROR -52.8418E-06  AT NODE 136796 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -516.776E-06   AT NODE 79045 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.62       TIME AVG. FORCE        3.82    
 LARGEST SCALED RESIDUAL FORCE      8.733E-04   AT NODE      63298   DOF  3
  CORRESPONDING RESIDUAL FORCE      8.733E-04
 LARGEST INCREMENT OF DISP.        -0.501       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -1.116E-04   AT NODE       9306   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   5 TOTAL ITERATIONS, OF WHICH
   5 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.500    ,  FRACTION OF STEP COMPLETED  0.750    
 STEP TIME COMPLETED        7.50    ,  TOTAL TIME COMPLETED         15.4    


  INCREMENT    16 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.372e+12
        SOLVER ELAPSED TIME:  146s

                 4407 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                 4407 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 541.253E-03   AT NODE 83564 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 371.118E-03   AT NODE 79593 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.68       TIME AVG. FORCE        3.87    
 LARGEST SCALED RESIDUAL FORCE      0.679       AT NODE     141473   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.679    
 LARGEST INCREMENT OF DISP.        -0.502       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.       -0.107       AT NODE       2106   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.522e+12
```
