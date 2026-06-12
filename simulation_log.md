# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 19:36:10  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 14, Attempt 1 — **converged**
- Total time: 14.9000  |  Increment size: 0.50000
- Converged increments so far: 30

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
```

## Recent .msg output
```
FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      6.518e+12
        SOLVER ELAPSED TIME:  31s

                   43 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   10 POINTS CHANGED FROM OPEN TO CLOSED
                   33 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 1.39084E-03 AT NODE 131462 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -10.2054E-03  AT NODE 22784 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.62       TIME AVG. FORCE        3.76    
 LARGEST SCALED RESIDUAL FORCE      1.298E-02   AT NODE      63305   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.298E-02
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -1.079E-03   AT NODE      57626   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   3 TOTAL ITERATIONS, OF WHICH
   3 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.500    ,  FRACTION OF STEP COMPLETED  0.700    
 STEP TIME COMPLETED        7.00    ,  TOTAL TIME COMPLETED         14.9    


  INCREMENT    15 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.241e+12
        SOLVER ELAPSED TIME:  35s

                 5115 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                 5115 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 212.051E-03   AT NODE 4965 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 621.142E-03   AT NODE 70995 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.73       TIME AVG. FORCE        3.82    
 LARGEST SCALED RESIDUAL FORCE      0.486       AT NODE      78562   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.486    
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2583   DOF  3
 LARGEST CORRECTION TO DISP.       -8.060E-02   AT NODE       2007   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.502e+12
        SOLVER ELAPSED TIME:  35s

                 1868 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  997 POINTS CHANGED FROM OPEN TO CLOSED
                  871 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR 936.778E-03   AT NODE 82542 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -234.730E-03   AT NODE 697 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.63       TIME AVG. FORCE        3.82    
 LARGEST SCALED RESIDUAL FORCE      0.707       AT NODE      78960   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.707    
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
```
