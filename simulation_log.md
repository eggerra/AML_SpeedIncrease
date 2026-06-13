# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 08:27:43  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 20, Attempt 1 — **converged**
- Total time: 16.9000  |  Increment size: 0.50000
- Converged increments so far: 36

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
Abaqus/Standard 2025.HF3                  DATE 13-Jun-2026 TIME 05:18:08
 SUMMARY OF JOB INFORMATION:
 STEP  INC ATT SEVERE EQUIL TOTAL  TOTAL      STEP       INC OF       DOF    IF
               DISCON ITERS ITERS  TIME/    TIME/LPF    TIME/LPF    MONITOR RIKS
               ITERS               FREQ
   1     1   1     3     3     6  0.500      0.500      0.5000    
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
```

## Recent .msg output
```
MAX. CONTACT FORCE ERROR 469.610E-03   AT NODE 27158 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.16       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE     -0.778       AT NODE     121779   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.778    
 LARGEST INCREMENT OF DISP.         0.963       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.        1.529E-02   AT NODE       1274   DOF  2
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.574e+12
        SOLVER ELAPSED TIME:  42s

                  102 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   52 POINTS CHANGED FROM OPEN TO CLOSED
                   50 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    26

   MAX. PENETRATION ERROR 286.139E-03   AT NODE 16362 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -317.735E-03   AT NODE 129468 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.16       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE     -0.685       AT NODE     121779   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.685    
 LARGEST INCREMENT OF DISP.         0.962       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.        1.580E-02   AT NODE       1274   DOF  2
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.772e+12
        SOLVER ELAPSED TIME:  42s

                   86 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   43 POINTS CHANGED FROM OPEN TO CLOSED
                   43 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    27

   MAX. PENETRATION ERROR 185.149E-03   AT NODE 16362 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -319.865E-03   AT NODE 129468 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.17       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE      -5.55       AT NODE      63293   DOF  3
  CORRESPONDING RESIDUAL FORCE      -5.55    
 LARGEST INCREMENT OF DISP.         0.961       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.        1.650E-02   AT NODE       1274   DOF  2
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.686e+12
        SOLVER ELAPSED TIME:  44s

                  117 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   59 POINTS CHANGED FROM OPEN TO CLOSED
                   58 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    28

   MAX. PENETRATION ERROR 171.659E-03   AT NODE 91383 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -326.242E-03   AT NODE 129468 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.17       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE       1.33       AT NODE      63293   DOF  3
  CORRESPONDING RESIDUAL FORCE       1.33    
 LARGEST INCREMENT OF DISP.         0.964       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -1.992E-02   AT NODE       6743   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.926e+12
        SOLVER ELAPSED TIME:  43s

                   98 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   44 POINTS CHANGED FROM OPEN TO CLOSED
                   54 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    29

   MAX. PENETRATION ERROR 102.222E-03   AT NODE 91262 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -382.914E-03   AT NODE 141252 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.17       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE      -4.93       AT NODE      71356   DOF  3
  CORRESPONDING RESIDUAL FORCE      -4.93    
 LARGEST INCREMENT OF DISP.         0.963       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.        1.834E-02   AT NODE       1274   DOF  2
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.028e+12
```
