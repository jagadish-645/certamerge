from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Optional

import typer

from .car import write_json
from .gate import gate_repo
from .recover import recover_repo
from .verifier import explain_car as explain_car_text
from .verifier import verify_car as verify_car_file

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def verify_car(path: Path) -> None:
    result = verify_car_file(path)
    typer.echo(json.dumps(result, indent=2))
    if not result["valid"]:
        raise typer.Exit(code=1)


@app.command()
def explain_car(path: Path) -> None:
    typer.echo(explain_car_text(path))


@app.command()
def recover(repo: Path, output: Optional[Path] = None) -> None:
    snapshot = recover_repo(repo)
    if output:
        write_json(output, snapshot)
    typer.echo(f"Verdict: {snapshot['verdict']}")
    typer.echo("Policy reason: Recover checks basic proof signals without claiming security correctness.")
    if snapshot["missing_proof"]:
        typer.echo("Missing proof: " + ", ".join(item["type"] for item in snapshot["missing_proof"]))
    else:
        typer.echo("Missing proof: No missing proof required by current policy.")
    action = "Review generated repair missions and rerun CertaMerge after evidence is present."
    typer.echo(f"Accountable next action: repo-owner - {action}")
    if output:
        typer.echo(f"Repo Proof Snapshot: {output}")


@app.command()
def gate(
    repo: Annotated[Path, typer.Option("--repo")],
    policy: Annotated[Path, typer.Option("--policy")],
    output: Optional[Path] = None,
) -> None:
    try:
        result = gate_repo(repo, policy, output)
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"Verdict: {result['verdict']}")
    typer.echo(f"Policy reason: {result['policy_reason']}")
    if result["missing_proof"]:
        typer.echo("Missing proof: " + ", ".join(item["type"] for item in result["missing_proof"]))
    else:
        typer.echo("Missing proof: No missing proof required by current policy.")
    next_action = result["accountable_next_action"]
    typer.echo(f"Accountable next action: {next_action['owner']} - {next_action['action']}")
    typer.echo(f"CAR: {result['car_path'] if result['car_path'] else 'not written; pass --output to persist'}")
