import asyncio
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

console = Console()

sales_tax = 0.0725
PREMIUM_SHIPPING_COST = 120.00


def ground_shipping_cost(weight: float) -> float:
    if weight <= 2:
        cost = weight * 1.50 + 20.00
    elif weight <= 6:
        cost = weight * 3.00 + 20.00
    elif weight <= 10:
        cost = weight * 4.00 + 20.00
    else:
        cost = weight * 4.75 + 20.00
    return cost * (1 + sales_tax)


def drone_shipping_cost(weight: float) -> float:
    if weight <= 2:
        cost = weight * 4.50
    elif weight <= 6:
        cost = weight * 9.00
    elif weight <= 10:
        cost = weight * 12.00
    else:
        cost = weight * 14.25
    return cost * (1 + sales_tax)


async def animate_steps(progress: Progress, task_id: int, total_steps: int, fail_at: int | None = None) -> None:
    for step in range(1, total_steps + 1):
        await asyncio.sleep(0.03)
        progress.advance(task_id, 1)
        if fail_at is not None and step == fail_at:
            raise RuntimeError("Computation error while calculating rates")


async def compute_shipping(weight: float, fail: bool = False) -> tuple[float, float, float]:
    taxed_premium = PREMIUM_SHIPPING_COST * (1 + sales_tax)
    total_steps = 120
    fail_at = 70 if fail else None

    progress = Progress(
        SpinnerColumn(style="yellow"),
        TextColumn("[bold]{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    )

    with progress:
        task_id = progress.add_task("[yellow]Calculating shipping costs[/yellow]", total=total_steps)
        try:
            await animate_steps(progress, task_id, total_steps, fail_at=fail_at)
            progress.update(task_id, description="[green]Calculation complete[/green]")
        except Exception:
            progress.update(task_id, description="[bold red]Calculation failed[/bold red]")
            raise

    ground = ground_shipping_cost(weight)
    drone = drone_shipping_cost(weight)
    return ground, taxed_premium, drone


def read_weight() -> float:
    raw = input("\nPlease enter the weight of your package in lbs: ").strip()
    w = float(raw)
    if w <= 0:
        raise ValueError("Weight must be greater than 0")
    return round(w, 2)


async def main() -> None:
    try:
        weight = read_weight()
    except ValueError:
        raise ValueError("Weight must be a positive number")

    try:
        ground, premium, drone = await compute_shipping(weight, fail=False)
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        return

    console.print(
        "\n"
        "[bold]=============== Shipping Cost Per Tier ===============[/bold]\n\n"
        f"Package weight: [bold]{weight:.2f}[/bold] lbs\n"
        "Prices include sales tax\n\n"
        f"Ground Shipping:         [bold green]${ground:.2f}[/bold green]\n"
        f"Premium Ground Shipping: [bold green]${premium:.2f}[/bold green]\n"
        f"Drone Shipping:          [bold green]${drone:.2f}[/bold green]\n"
    )


if __name__ == "__main__":
    asyncio.run(main())
