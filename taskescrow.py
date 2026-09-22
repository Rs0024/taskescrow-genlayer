# v0.3.0
# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }

from genlayer import *
import json


class TaskEscrow(gl.Contract):
    employer: Address
    worker: Address
    task_description: str
    reward_amount: u256
    evidence_url: str
    status: str

    def __init__(
        self,
        employer: Address,
        worker: Address,
        task_description: str,
        reward_amount: u256,
    ):
        self.employer = employer
        self.worker = worker
        self.task_description = task_description
        self.reward_amount = reward_amount
        self.evidence_url = ""
        self.status = "created"

    @gl.public.write
    def mark_funded(self):
        self.status = "funded"

    @gl.public.write
    def submit_work(self, evidence_url: str):
        if self.status != "funded":
            raise Exception("Task must be funded before submitting work")

        self.evidence_url = evidence_url
        self.status = "submitted"

    @gl.public.write
    def verify_task(self):
        if self.status != "submitted":
            raise Exception("Work must be submitted before verification")

        evidence_url = self.evidence_url
        task_description = self.task_description

        def leader_fn():
            page = gl.get_webpage(evidence_url, mode="text")

            prompt = f"""
You are verifying whether evidence proves that a task was completed.

TASK:
{task_description}

EVIDENCE:
{page}

Return ONLY valid JSON in this exact format:
{{"completed": true}}

or

{{"completed": false}}
"""

            result = gl.exec_prompt(prompt)
            return result

        def validator_fn(leader_result):
            page = gl.get_webpage(evidence_url, mode="text")

            prompt = f"""
You are independently verifying whether evidence proves that a task was completed.

TASK:
{task_description}

EVIDENCE:
{page}

Return ONLY valid JSON in this exact format:
{{"completed": true}}

or

{{"completed": false}}
"""

            validator_result = gl.exec_prompt(prompt)

            try:
                leader_data = json.loads(leader_result)
                validator_data = json.loads(validator_result)

                return (
                    leader_data.get("completed")
                    == validator_data.get("completed")
                )
            except Exception:
                return False

        result = gl.vm.run_nondet_default(
            leader_fn,
            validator_fn,
        )

        try:
            result_data = json.loads(result)

            if result_data.get("completed") is True:
                self.status = "approved"
            else:
                self.status = "rejected"

        except Exception:
            self.status = "rejected"

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_evidence_url(self) -> str:
        return self.evidence_url

    @gl.public.view
    def get_task_description(self) -> str:
        return self.task_description

    @gl.public.view
    def get_reward_amount(self) -> u256:
        return self.reward_amount
