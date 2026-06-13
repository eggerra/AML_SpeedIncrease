# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 06:53:58  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 15, Attempt 1 — **converged**
- Total time: 14.7000  |  Increment size: 0.18750
- Converged increments so far: 31

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
```

## Recent .msg output
```
1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.314e+12
        SOLVER ELAPSED TIME:  30s

                    2 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    2 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     5

   MAX. PENETRATION ERROR 212.118E-03   AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 7.21438E-03 AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.63       TIME AVG. FORCE        3.81    
 LARGEST SCALED RESIDUAL FORCE      9.862E-05   AT NODE      76090   DOF  3
  CORRESPONDING RESIDUAL FORCE      9.862E-05
 LARGEST INCREMENT OF DISP.        -0.188       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.        1.311E-04   AT NODE       2138   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.308e+12
        SOLVER ELAPSED TIME:  30s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1

   MAX. PENETRATION ERROR 108.699E-03   AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 13.4447E-03  AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.63       TIME AVG. FORCE        3.81    
 LARGEST SCALED RESIDUAL FORCE      1.739E-02   AT NODE      63298   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.739E-02
 LARGEST INCREMENT OF DISP.        -0.188       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.        4.750E-05   AT NODE       2141   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.308e+12
        SOLVER ELAPSED TIME:  29s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     2

   MAX. PENETRATION ERROR 39.4389E-03  AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 11.3000E-03  AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.63       TIME AVG. FORCE        3.81    
 LARGEST SCALED RESIDUAL FORCE     -4.801E-04   AT NODE      63298   DOF  3
  CORRESPONDING RESIDUAL FORCE     -4.801E-04
 LARGEST INCREMENT OF DISP.        -0.188       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -1.412E-05   AT NODE      21771   DOF  2
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.308e+12
        SOLVER ELAPSED TIME:  29s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     3

   MAX. PENETRATION ERROR 7.14902E-03 AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 3.01520E-03 AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.63       TIME AVG. FORCE        3.81    
 LARGEST SCALED RESIDUAL FORCE     -2.809E-04   AT NODE      63298   DOF  3
  CORRESPONDING RESIDUAL FORCE     -2.809E-04
 LARGEST INCREMENT OF DISP.        -0.188       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -8.597E-06   AT NODE      21770   DOF  2
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.308e+12
        SOLVER ELAPSED TIME:  29s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     4

   MAX. PENETRATION ERROR 289.732E-06   AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 132.610E-06   AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINTS HAVE CONVERGED.

 AVERAGE FORCE                       4.63       TIME AVG. FORCE        3.81    
 LARGEST SCALED RESIDUAL FORCE     -8.391E-05   AT NODE      63298   DOF  3
  CORRESPONDING RESIDUAL FORCE     -8.391E-05
 LARGEST INCREMENT OF DISP.        -0.188       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -2.533E-06   AT NODE      21770   DOF  2
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   9 TOTAL ITERATIONS, OF WHICH
   5 ARE SEVERE DISCONTINUITY ITERATIONS AND  4 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.188    ,  FRACTION OF STEP COMPLETED  0.681    
 STEP TIME COMPLETED        6.81    ,  TOTAL TIME COMPLETED         14.7    


  INCREMENT    16 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.281
```
