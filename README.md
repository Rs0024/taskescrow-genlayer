# TaskEscrow

TaskEscrow is an AI-verified task completion workflow built with GenLayer Intelligent Contracts.

It allows a task to move through funding, evidence submission, and AI verification. GenLayer validators evaluate the submitted public evidence and record the final consensus result onchain as either `approved` or `rejected`.

## How It Works

1. The task is created with an employer, worker, task description, and configured reward amount.
2. `mark_funded()` changes the workflow state to `funded`.
3. The worker submits a public evidence URL using `submit_work()`.
4. `verify_task()` uses GenLayer's intelligent execution and validator consensus to evaluate whether the evidence demonstrates task completion.
5. The final result is stored onchain as `approved` or `rejected`.

## GenLayer Deployment

**Network:** GenLayer Studio Dev  
**Chain ID:** 61997

**Contract Address:**

`0x2Ca21453a7454bF1A2Ae5F77c4a83A6aE1A8dED9`

## Contract Functions

### Write
- `mark_funded()`
- `submit_work(evidence_url)`
- `verify_task()`

### Read
- `get_status()`
- `get_evidence_url()`
- `get_task_description()`
- `get_reward_amount()`

## Demo

A working deployment has been tested on GenLayer Studio Dev. The funding, evidence submission, and AI verification transactions finalized successfully, and `get_status()` returned the resulting validator-consensus decision.

## Project Website

https://rs0024.github.io/ai-task-verifier-intelligent-contract/

## Demo Video

https://x.com/ritesharma24/status/2099916094882660833

## Technology

- GenLayer Intelligent Contracts
- Python
- GenLayer Studio Dev
- GenLayer validator consensus
- Web-based project interface

## Purpose

TaskEscrow demonstrates how GenLayer can be used to evaluate real-world task evidence through AI and decentralized validator consensus instead of relying only on a centralized verifier.
