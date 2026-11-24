# Fig. 7 reproduction workspace

This folder is an isolated copy for an NSFNET Fig. 7 experiment. The original
project, demo outputs, and checkpoints are not modified by this workspace.

## Paper-aligned settings in this copy

- NSFNET: 14 nodes, 44 directed links, 100 frequency slots.
- Uniform source/destination traffic; average request arrival rate 10 and
  average service duration 25.
- DeepRMSA policy: K=5 routes, M=1 first-fit spectrum position, 16 workers,
  5 hidden layers of 128 neurons, gamma 0.95, Adam learning rate 1e-5.
- Training episodes contain 1,000 requests. The training window/batch default
  is set to 50 to align with the paper's stated moderate FLX window N=50.
- Fig. 7 spans up to 5,000,000 requests. At 1,000 requests per episode, that
  requires 5,000 recorded episodes after the three warm-up episodes. `BP.dat`
  stores one point per recorded episode; `DEEPRMSA_LOG_INTERVAL=10` only
  controls how often the accumulated values are flushed to disk.

The source code available here implements the window-based DeepRMSA-FLX path.
It does not contain a separately verified DeepRMSA-EP implementation. The
baseline script can produce SP-FF (K=1) and KSP-FF (K=5) curves. Therefore, a
plot from these scripts must be labelled a partial reproduction, not a full
reproduction of all four curves in paper Fig. 7.

## Results recorded so far

This isolated copy adds a paper-oriented experiment configuration, repeatable
SP-FF/KSP-FF benchmark CSVs, and a plotting script to the original source. It
does not add a new DeepRMSA algorithm. The raw FLX training log and preview PNG
are excluded from Git by the parent `.gitignore`; the FLX figures below are a
snapshot for progress reporting, not a final evaluation.

| Method | Mean blocking probability | Simulation coverage | Status |
| --- | ---: | ---: | --- |
| SP-FF | 0.1282678 | 5,000,000 requests (500 samples) | Complete |
| KSP-FF | 0.0511504 | 5,000,000 requests (500 samples) | Complete |
| DeepRMSA-FLX | Latest logged episode: 0.046; mean of the latest 10 logged episodes: 0.0515 | 270,000 requests logged out of a 5,000,000-request target | In progress; not a final/converged result |
| DeepRMSA-EP | — | — | No separately verified implementation available in this source |

The FLX snapshot is based on `BP.dat` as checked on 2026-11-24 17:37 local
time. Values can change if training continues. The complete SP-FF and KSP-FF
curves are in [`sp_ff_curve.csv`](sp_ff_curve.csv) and
[`ksp_ff_curve.csv`](ksp_ff_curve.csv). Recreate the available-curve plot with
`python plot_fig7.py`; it writes `fig7_reproduction_partial.png` locally.

## Full run commands (PowerShell)

Run from this directory in separate PowerShell sessions. Full training is
expected to be lengthy; the earlier short run took roughly a minute per
1,000-request episode on this machine, so 5,000 episodes may take several
days. Actual time can vary.

```powershell
$env:DEEPRMSA_LAMBDA_REQ = "10"
$env:DEEPRMSA_LAMBDA_TIME = "25"
$env:DEEPRMSA_BATCH_SIZE = "50"
$env:DEEPRMSA_LOG_INTERVAL = "10"
$env:DEEPRMSA_MAX_RECORDED_EPISODES = "5000"
..\.venv\Scripts\python.exe -u .\Deep_RMSA_A3C.py
```

Run each baseline in its own clean output copy/folder so the CSVs do not
overwrite one another:

```powershell
$env:DEEPRMSA_LAMBDA_REQ = "10"
$env:DEEPRMSA_LAMBDA_TIME = "25"
$env:DEEPRMSA_BENCHMARK_REQUESTS = "5000000"
$env:DEEPRMSA_BENCHMARK_INTERVAL = "10000"
$env:DEEPRMSA_BENCHMARK_REPEATS = "1"
$env:DEEPRMSA_BENCHMARK_KPATH = "1"
..\.venv\Scripts\python.exe -u ".\K-SP-FF benchmark_NSFNET.py"
```

Repeat with `DEEPRMSA_BENCHMARK_KPATH = "5"` to create the KSP-FF curve.
After all runs finish, `plot_fig7.py` combines the available project FLX curve
and the two baseline curves. It cannot draw the paper's EP curve until a
validated EP implementation/result is available.

## Important

The number 5,000,000 and the traffic settings follow the paper's NSFNET
simulation description, but an exact reproduction also depends on the paper's
algorithm details, random seeds, and implementation choices. Checkpoint and
`.dat` outputs are stored only in this folder. Do not mix an unfinished run
with prior `.dat` data.
